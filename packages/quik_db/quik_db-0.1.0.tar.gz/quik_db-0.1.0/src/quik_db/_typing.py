# db_connection.pyi

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
)

from sqlalchemy import URL, Engine
from sqlalchemy.engine import Connection, Result
from sqlalchemy.orm import (
    Session,
    scoped_session,
    sessionmaker,
)

from quik_db.model.enums import ExecutionState, QueryType
from quik_db.model.models import (
    DatabaseModel,
    MultiDatabaseModel,
    QuerySettings,
    StateVars,
)


if TYPE_CHECKING:
    from collections.abc import Callable


class Configuration:
    name: str
    result: Optional[Any]
    execution_handler: Optional[Callable[..., Any]]
    result_handlers: List[Callable[..., Any]]
    error_handlers: List[Callable[..., Any]]
    param_handlers: List[Callable[..., Any]]
    _exc: ExecutionState
    vars: StateVars
    config: Union[DatabaseModel, MultiDatabaseModel]
    qs: QuerySettings
    conn_build_type: Literal["url", "params"]

    def __init__(
        self,
        config: Dict[str, Any],
        name: str = "",
        handlers: Optional[
            Dict[str, Union[Callable[..., Any], List[Callable[..., Any]]]]
        ] = None,
    ) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def url_string(self) -> Union[str, URL]: ...

    @property
    def param_url(self) -> URL: ...

    @property
    def url_base(self) -> str: ...

    @property
    def prefix_schema(self) -> str: ...

    @property
    def handler_list(self) -> List[str]: ...

    def set_handlers(
        self,
        handlers: Dict[
            str, Union[Callable[..., Any], List[Callable[..., Any]]]
        ],
    ) -> None: ...


class DatabaseConnection(Configuration, ABC):
    connection: Optional[Any]  # Replace with actual connection type
    _columns: List[Any]
    exit: Optional[Any]

    def __init__(
        self,
        config: Dict[str, Any],
        name: str = "",
        handlers: Optional[
            Dict[str, Union[Callable[..., Any], List[Callable[..., Any]]]]
        ] = None,
    ) -> None: ...

    def __enter__(self) -> DatabaseConnection: ...

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None: ...

    def execute_sp(
        self,
        procedure_name: str,
        params: Optional[Dict[str, Any]] = None,
        fetch: Optional[int] = None,
    ) -> Union[Dict[str, Any], List[Any]]: ...

    def execute(
        self,
        query: str,
        params: Union[
            Dict[str, str], Tuple[Tuple[str, str], ...], Tuple[str, str]
        ] = (),
        fetch: Optional[int] = None,
        offset: int = 0,
        limit: int = 0,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]: ...

    def add_paging(
        self,
        query: str,
        offset: int = 0,
        limit: int = 0,
    ) -> str: ...

    def process_results(
        self,
        result: Union[Dict[str, Any], Result],
        query_type: QueryType = QueryType.QUERY,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]: ...

    def fetch_results(
        self, fetch_size: int
    ) -> Union[Dict[str, Any], List[Any]]: ...

    def add_schema_prefix(
        self,
        query: str,
        query_type: Literal["procedure", "query"] = "query",
    ) -> str: ...

    def limit(self, limit: int) -> DatabaseConnection: ...

    def offset(self, offset: int) -> DatabaseConnection: ...

    def fetch(self, fetch_size: int) -> DatabaseConnection: ...

    def rollback(self) -> None: ...

    def commit(self) -> None: ...

    def close(self) -> None: ...

    def _set_activte_state(self) -> None: ...

    def _get_fetch_value(self, fetch_size: Optional[int]) -> Optional[int]: ...

    @abstractmethod
    def connect(self) -> Union[Connection, Session, scoped_session]: ...


class SqlAlchemyConnection(DatabaseConnection):
    _session_factory: Optional[Union[sessionmaker, scoped_session]]
    connection_type: Literal["scoped", "session", "direct"]

    def __init__(
        self,
        config: Dict[str, Any],
        name: str = "",
        connection_type: Literal["scoped", "session", "direct"] = "direct",
        session: Optional[Session] = None,
    ) -> None: ...

    @property
    def engine(self) -> Engine: ...

    def session(self) -> SqlAlchemyConnection: ...

    def connect(self) -> Union[Connection, Session, scoped_session]: ...

    def _create_session_factory(
        self,
    ) -> Union[sessionmaker, scoped_session]: ...

    def close(self) -> None: ...
