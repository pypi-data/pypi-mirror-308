import logging
from typing import Any, overload

from psycopg import AsyncCursor, sql
from psycopg.rows import class_row

from database_wrapper import DataModelType, DBWrapperAsync

from .db_wrapper_pgsql_mixin import DBWrapperPgSQLMixin
from .connector import (
    # Async
    PgConnectionTypeAsync,
    PgCursorTypeAsync,
    PgSQLWithPoolingAsync,
)


class DBWrapperPgSQLAsync(DBWrapperPgSQLMixin, DBWrapperAsync):
    """
    Async database wrapper for postgres

    This is meant to be used in async environments.
    Also remember to call close() when done as we cannot do that in __del__.
    """

    # Override db instance
    db: PgSQLWithPoolingAsync | None = None
    """ Async PostgreSQL database connector """

    dbConn: PgConnectionTypeAsync | None = None
    """ Async PostgreSQL connection object """

    #######################
    ### Class lifecycle ###
    #######################

    # Meta methods
    # We are overriding the __init__ method for the type hinting
    def __init__(
        self,
        db: PgSQLWithPoolingAsync | None = None,
        dbConn: PgConnectionTypeAsync | None = None,
        logger: logging.Logger | None = None,
    ):
        """
        Initializes a new instance of the DBWrapper class.

        Args:
            db (MySQL): The PostgreSQL database connector.
            dbConn (MySqlConnection, optional): The PostgreSQL connection object. Defaults to None.
            logger (logging.Logger, optional): The logger object. Defaults to None.
        """
        super().__init__(db, dbConn, logger)

    async def close(self) -> None:
        if hasattr(self, "dbConn") and self.dbConn and hasattr(self, "db") and self.db:
            await self.db.returnConnection(self.dbConn)

        await super().close()

    ###############
    ### Setters ###
    ###############

    def setDb(self, db: PgSQLWithPoolingAsync | None) -> None:
        """
        Updates the database backend object.

        Args:
            db (PgSQLWithPoolingAsync | None): The new database backend object.
        """
        super().setDb(db)

    def setDbConn(self, dbConn: PgConnectionTypeAsync | None) -> None:
        """
        Updates the database connection object.

        Args:
            dbConn (PgConnectionTypeAsync | None): The new database connection object.
        """
        super().setDbConn(dbConn)

    ######################
    ### Helper methods ###
    ######################

    @overload
    async def createCursor(self) -> PgCursorTypeAsync: ...

    @overload
    async def createCursor(
        self,
        emptyDataClass: DataModelType,
    ) -> AsyncCursor[DataModelType]: ...

    async def createCursor(
        self,
        emptyDataClass: DataModelType | None = None,
    ) -> AsyncCursor[DataModelType] | PgCursorTypeAsync:
        """
        Creates a new cursor object.

        Args:
            emptyDataClass (DBDataModel | None, optional): The data model to use for the cursor.
                Defaults to None.

        Returns:
            PgCursorTypeAsync | AsyncCursor[DBDataModel]: The created cursor object.
        """
        if self.db is None and self.dbConn is None:
            raise ValueError(
                "Database object and connection is not properly initialized"
            )

        # First we need connection
        if self.dbConn is None and self.db is not None:
            status = await self.db.newConnection()
            if not status:
                raise Exception("Failed to create new connection")

            (pgConn, _pgCur) = status
            self.dbConn = pgConn

        if self.dbConn is None:
            raise Exception("Failed to get connection")

        if emptyDataClass is None:
            return self.dbConn.cursor()

        return self.dbConn.cursor(row_factory=class_row(emptyDataClass.__class__))

    def logQuery(
        self,
        cursor: AsyncCursor[Any],
        query: sql.SQL | sql.Composed,
        params: tuple[Any, ...],
    ) -> None:
        """
        Logs the given query and parameters.

        Args:
            cursor (Any): The database cursor.
            query (Any): The query to log.
            params (tuple[Any, ...]): The parameters to log.
        """
        queryString = query.as_string(self.dbConn)
        logging.getLogger().debug(f"Query: {queryString}")
