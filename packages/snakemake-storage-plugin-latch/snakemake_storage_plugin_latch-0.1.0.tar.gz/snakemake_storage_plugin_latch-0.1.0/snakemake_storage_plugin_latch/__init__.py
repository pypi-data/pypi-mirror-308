import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import Any, Iterable, List, Optional, cast
from urllib.parse import urlparse

import dateutil.parser as dp
import gql
from gql.transport.requests import RequestsHTTPTransport
from latch_persistence import LatchPersistence
from snakemake_interface_storage_plugins.io import (
    IOCacheStorageInterface,
    Mtime,
    get_constant_prefix,
)
from snakemake_interface_storage_plugins.settings import StorageProviderSettingsBase
from snakemake_interface_storage_plugins.storage_object import (
    StorageObjectGlob,
    StorageObjectRead,
    StorageObjectTouch,
    StorageObjectWrite,
    retry_decorator,
)
from snakemake_interface_storage_plugins.storage_provider import (
    ExampleQuery,
    Operation,
    QueryType,
    StorageProviderBase,
    StorageQueryValidationResult,
)


# Optional:
# Define settings for your storage plugin (e.g. host url, credentials).
# They will occur in the Snakemake CLI as --storage-<storage-plugin-name>-<param-name>
# Make sure that all defined fields are 'Optional' and specify a default value
# of None or anything else that makes sense in your case.
# Note that we allow storage plugin settings to be tagged by the user. That means,
# that each of them can be specified multiple times (an implicit nargs=+), and
# the user can add a tag in front of each value (e.g. tagname1:value1 tagname2:value2).
# This way, a storage plugin can be used multiple times within a workflow with different
# settings.
@dataclass
class StorageProviderSettings(StorageProviderSettingsBase): ...


class LatchPathValidationException(ValueError): ...


@dataclass
class LatchPath:
    domain: str
    path: str

    @classmethod
    def parse(cls, path: str):
        parsed = urlparse(path)
        if parsed.scheme != "latch":
            raise LatchPathValidationException(f"invalid latch path: {path}")

        return cls(parsed.netloc, parsed.path)

    def local_suffix(self) -> str:
        return f"{self.domain}{self.path}"

    def unparse(self) -> str:
        return f"latch://{self.domain}{self.path}"

    def __str__(self):
        return self.unparse()

    def __repr__(self):
        return f"LatchPath({repr(self.domain)}, {repr(self.path)})"


class AuthenticationError(RuntimeError): ...


# Required:
# Implementation of your storage provider
# This class can be empty as the one below.
# You can however use it to store global information or maintain e.g. a connection
# pool.
class StorageProvider(StorageProviderBase):
    # For compatibility with future changes, you should not overwrite the __init__
    # method. Instead, use __post_init__ to set additional attributes and initialize
    # futher stuff.

    def __post_init__(self):
        # This is optional and can be removed if not needed.
        # Alternatively, you can e.g. prepare a connection to your storage backend here.
        # and set additional attributes.

        auth_header: Optional[str] = None

        token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID", "")
        if token != "":
            auth_header = f"Latch-Execution-Token {token}"

        if auth_header is None:
            token_path = Path.home() / ".latch" / "token"
            if token_path.exists():
                auth_header = f"Latch-SDK-Token {token_path.read_text().strip()}"

        if auth_header is None:
            raise AuthenticationError(
                "Unable to find credentials to connect to gql server, aborting"
            )

        url = (
            f"https://vacuole.{os.environ.get('LATCH_SDK_DOMAIN', 'latch.bio')}/graphql"
        )

        self.gql = gql.Client(
            transport=RequestsHTTPTransport(
                url=url, headers={"Authorization": auth_header}, retries=5, timeout=90
            )
        )
        self.lp = LatchPersistence()

    @classmethod
    def example_queries(cls) -> List[ExampleQuery]:
        """Return valid example queries (at least one) with description."""
        return [
            ExampleQuery("latch://123.account/hello", "basic latch path", QueryType.ANY)
        ]

    def rate_limiter_key(self, query: str, operation: Operation) -> Any:
        """Return a key for identifying a rate limiter given a query and an operation.

        This is used to identify a rate limiter for the query.
        E.g. for a storage provider like http that would be the host name.
        For s3 it might be just the endpoint URL.
        """
        # todo(ayush): does this make sense
        return LatchPath.parse(query).domain

    def default_max_requests_per_second(self) -> float:
        """Return the default maximum number of requests per second for this storage
        provider."""
        return 10

    def use_rate_limiter(self) -> bool:
        """Return False if no rate limiting is needed for this provider."""
        # todo(ayush): enable if necessary
        return False

    @classmethod
    def is_valid_query(cls, query: str) -> StorageQueryValidationResult:
        """Return whether the given query is valid for this storage provider."""
        # Ensure that also queries containing wildcards (e.g. {sample}) are accepted
        # and considered valid. The wildcards will be resolved before the storage
        # object is actually used.
        valid: bool
        reason: Optional[str]
        try:
            LatchPath.parse(query)
            valid = True
            reason = None
        except LatchPathValidationException as e:
            valid = False
            reason = str(e)

        return StorageQueryValidationResult(query, valid, reason)


@dataclass
class LatchFileAttrs:
    exists: bool
    type: str
    size: Optional[int]
    modify_time: Optional[datetime]


# Required:
# Implementation of storage object. If certain methods cannot be supported by your
# storage (e.g. because it is read-only see
# snakemake-storage-http for comparison), remove the corresponding base classes
# from the list of inherited items.
class StorageObject(
    StorageObjectRead,
    StorageObjectWrite,
    StorageObjectGlob,
    # StorageObjectTouch, # todo(ayush): do we need this?
):
    # For compatibility with future changes, you should not overwrite the __init__
    # method. Instead, use __post_init__ to set additional attributes and initialize
    # futher stuff.

    def _get_file_attrs(self) -> LatchFileAttrs:
        res = self.provider.gql.execute(
            gql.gql(
                """
                query GetFileAttrs($argPath: String!) {
                    ldataResolvePathToNode(path: $argPath) {
                        path
                        ldataNode {
                            finalLinkTarget {
                                id
                                type
                                pending
                                removed
                                ldataObjectMeta {
                                    contentSize
                                    modifyTime
                                }
                            }
                        }
                    }
                }
                """
            ),
            {"argPath": str(self.path)},
        )["ldataResolvePathToNode"]

        if res is None or res["ldataNode"] is None:
            raise AuthenticationError(
                f"latch path {self.path} either does not exist or signer lacks permission to view it"
            )

        flt = res["ldataNode"]["finalLinkTarget"]

        exists = (
            not flt["removed"]
            and not flt["pending"]
            and (res["path"] is None or res["path"] == "")
        )

        size = None
        modify_time = None

        meta = flt["ldataObjectMeta"]
        if meta is not None:
            size = meta["contentSize"]
            if size is not None:
                size = int(size)

            modify_time = meta["modifyTime"]
            if modify_time is not None:
                modify_time = dp.isoparse(modify_time)

        return LatchFileAttrs(exists, flt["type"].lower(), size, modify_time)

    def __post_init__(self):
        # This is optional and can be removed if not needed.
        # Alternatively, you can e.g. prepare a connection to your storage backend here.
        # and set additional attributes.
        self.provider = cast(StorageProvider, self.provider)
        self.path = LatchPath.parse(self.query)

        self.successfully_stored = False

    async def inventory(self, cache: IOCacheStorageInterface):
        """From this file, try to find as much existence and modification date
        information as possible. Only retrieve that information that comes for free
        given the current object.
        """
        # This is optional and can be left as is

        # If this is implemented in a storage object, results have to be stored in
        # the given IOCache object, using self.cache_key() as key.
        # Optionally, this can take a custom local suffix, needed e.g. when you want
        # to cache more items than the current query: self.cache_key(local_suffix=...)

        attrs = self._get_file_attrs()

        cache.exists_in_storage[self.cache_key()] = attrs.exists

        if attrs.size is not None:
            cache.size[self.cache_key()] = attrs.size

        if attrs.modify_time is not None:
            cache.mtime[self.cache_key()] = Mtime(storage=attrs.modify_time.timestamp())

    def get_inventory_parent(self) -> Optional[str]:
        """Return the parent directory of this object."""
        # this is optional and can be left as is
        return None

    def local_suffix(self) -> str:
        """Return a unique suffix for the local path, determined from self.query."""
        # s3 just does bucket/key so im not sure what the point of this method is
        return self.path.local_suffix()

    def cleanup(self):
        """Perform local cleanup of any remainders of the storage object."""
        # self.local_path() should not be removed, as this is taken care of by
        # Snakemake.
        pass

    # Fallible methods should implement some retry logic.
    # The easiest way to do this (but not the only one) is to use the retry_decorator
    # provided by snakemake-interface-storage-plugins.

    def exists(self) -> bool:
        # return True if the object exists
        if self.successfully_stored:
            return True

        return self._get_file_attrs().exists

    def mtime(self) -> float:
        # return the modification time
        mtime = self._get_file_attrs().modify_time
        if mtime is not None:
            return mtime.timestamp()

        return 0

    def size(self) -> int:
        # return the size in bytes
        size = self._get_file_attrs().size
        if size is not None:
            return size

        return 0

    def retrieve_object(self):
        # Ensure that the object is accessible locally under self.local_path()
        local = self.local_path().resolve()
        if self._get_file_attrs().type != "obj":
            self.provider.lp.download_directory(self.query, str(local))
            return

        self.provider.lp.download(self.query, str(local))

    # The following two methods are only required if the class inherits from
    # StorageObjectReadWrite.

    def store_object(self):
        self._store_object()
        self.successfully_stored = True

    def _store_object(self):
        # Ensure that the object is stored at the location specified by
        # self.local_path().
        local = self.local_path().resolve()
        if local.is_dir():
            self.provider.lp.upload_directory(str(local), self.query)
            return

        self.provider.lp.upload(str(local), self.query)

    def remove(self):
        # Remove the object from the storage.

        # todo(ayush): not implementing for now bc idk how i feel about letting snakemake kill things
        ...

    # The following method is only required if the class inherits from
    # StorageObjectGlob.

    def list_candidate_matches(self) -> Iterable[str]:
        """Return a list of candidate matches in the storage for the query."""
        # This is used by glob_wildcards() to find matches for wildcards in the query.
        # The method has to return concretized queries without any remaining wildcards.
        # Use snakemake_executor_plugins.io.get_constant_prefix(self.query) to get the
        # prefix of the query before the first wildcard.
        res = self.provider.gql.execute(
            gql.gql(
                """
                query SnakemakeGlobs($argPath: String!) {
                    ldataGetDescendants(argPath: $argPath) {
                        nodes {
                            id
                            path
                        }
                    }
                }
                """,
            ),
            {"argPath": get_constant_prefix(self.query)},
        )["ldataGetDescendants"]

        if res is None:
            raise AuthenticationError(
                f"latch path {self.path} either does not exist or signer lacks permission to view it"
            )

        for node in res["nodes"]:
            yield node["path"]

    # # The following method is only required if the class inherits from
    # # StorageObjectTouch
    # @retry_decorator
    # def touch(self):
    #     """Touch the object, updating its modification date."""
    #     ...
