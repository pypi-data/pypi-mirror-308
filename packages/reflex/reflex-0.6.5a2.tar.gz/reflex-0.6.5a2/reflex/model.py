"""Database built into Reflex."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, ClassVar, Optional, Type, Union

import alembic.autogenerate
import alembic.command
import alembic.config
import alembic.operations.ops
import alembic.runtime.environment
import alembic.script
import alembic.util
import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.orm

from reflex.base import Base
from reflex.config import environment, get_config
from reflex.utils import console
from reflex.utils.compat import sqlmodel, sqlmodel_field_has_primary_key


def get_engine(url: str | None = None) -> sqlalchemy.engine.Engine:
    """Get the database engine.

    Args:
        url: the DB url to use.

    Returns:
        The database engine.

    Raises:
        ValueError: If the database url is None.
    """
    conf = get_config()
    url = url or conf.db_url
    if url is None:
        raise ValueError("No database url configured")
    if not environment.ALEMBIC_CONFIG.get().exists():
        console.warn(
            "Database is not initialized, run [bold]reflex db init[/bold] first."
        )
    # Print the SQL queries if the log level is INFO or lower.
    echo_db_query = environment.SQLALCHEMY_ECHO.get()
    # Needed for the admin dash on sqlite.
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return sqlmodel.create_engine(url, echo=echo_db_query, connect_args=connect_args)


async def get_db_status() -> bool:
    """Checks the status of the database connection.

    Attempts to connect to the database and execute a simple query to verify connectivity.

    Returns:
        bool: The status of the database connection:
            - True: The database is accessible.
            - False: The database is not accessible.
    """
    status = True
    try:
        engine = get_engine()
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text("SELECT 1"))
    except sqlalchemy.exc.OperationalError:
        status = False

    return status


SQLModelOrSqlAlchemy = Union[
    Type[sqlmodel.SQLModel], Type[sqlalchemy.orm.DeclarativeBase]
]


class ModelRegistry:
    """Registry for all models."""

    models: ClassVar[set[SQLModelOrSqlAlchemy]] = set()

    # Cache the metadata to avoid re-creating it.
    _metadata: ClassVar[sqlalchemy.MetaData | None] = None

    @classmethod
    def register(cls, model: SQLModelOrSqlAlchemy):
        """Register a model. Can be used directly or as a decorator.

        Args:
            model: The model to register.

        Returns:
            The model passed in as an argument (Allows decorator usage)
        """
        cls.models.add(model)
        return model

    @classmethod
    def get_models(cls, include_empty: bool = False) -> set[SQLModelOrSqlAlchemy]:
        """Get registered models.

        Args:
            include_empty: If True, include models with empty metadata.

        Returns:
            The registered models.
        """
        if include_empty:
            return cls.models
        return {
            model for model in cls.models if not cls._model_metadata_is_empty(model)
        }

    @staticmethod
    def _model_metadata_is_empty(model: SQLModelOrSqlAlchemy) -> bool:
        """Check if the model metadata is empty.

        Args:
            model: The model to check.

        Returns:
            True if the model metadata is empty, False otherwise.
        """
        return len(model.metadata.tables) == 0

    @classmethod
    def get_metadata(cls) -> sqlalchemy.MetaData:
        """Get the database metadata.

        Returns:
            The database metadata.
        """
        if cls._metadata is not None:
            return cls._metadata

        models = cls.get_models(include_empty=False)

        if len(models) == 1:
            metadata = next(iter(models)).metadata
        else:
            # Merge the metadata from all the models.
            # This allows mixing bare sqlalchemy models with sqlmodel models in one database.
            metadata = sqlalchemy.MetaData()
            for model in cls.get_models():
                for table in model.metadata.tables.values():
                    table.to_metadata(metadata)

        # Cache the metadata
        cls._metadata = metadata

        return metadata


class Model(Base, sqlmodel.SQLModel):  # pyright: ignore [reportGeneralTypeIssues]
    """Base class to define a table in the database."""

    # The primary key for the table.
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    def __init_subclass__(cls):
        """Drop the default primary key field if any primary key field is defined."""
        non_default_primary_key_fields = [
            field_name
            for field_name, field in cls.__fields__.items()
            if field_name != "id" and sqlmodel_field_has_primary_key(field)
        ]
        if non_default_primary_key_fields:
            cls.__fields__.pop("id", None)

        super().__init_subclass__()

    @classmethod
    def _dict_recursive(cls, value):
        """Recursively serialize the relationship object(s).

        Args:
            value: The value to serialize.

        Returns:
            The serialized value.
        """
        if hasattr(value, "dict"):
            return value.dict()
        elif isinstance(value, list):
            return [cls._dict_recursive(item) for item in value]
        return value

    def dict(self, **kwargs):
        """Convert the object to a dictionary.

        Args:
            kwargs: Ignored but needed for compatibility.

        Returns:
            The object as a dictionary.
        """
        base_fields = {name: getattr(self, name) for name in self.__fields__}
        relationships = {}
        # SQLModel relationships do not appear in __fields__, but should be included if present.
        for name in self.__sqlmodel_relationships__:
            try:
                relationships[name] = self._dict_recursive(getattr(self, name))
            except sqlalchemy.orm.exc.DetachedInstanceError:
                # This happens when the relationship was never loaded and the session is closed.
                continue
        return {
            **base_fields,
            **relationships,
        }

    @staticmethod
    def create_all():
        """Create all the tables."""
        engine = get_engine()
        ModelRegistry.get_metadata().create_all(engine)

    @staticmethod
    def get_db_engine():
        """Get the database engine.

        Returns:
            The database engine.
        """
        return get_engine()

    @staticmethod
    def _alembic_config():
        """Get the alembic configuration and script_directory.

        Returns:
            tuple of (config, script_directory)
        """
        config = alembic.config.Config(environment.ALEMBIC_CONFIG.get())
        return config, alembic.script.ScriptDirectory(
            config.get_main_option("script_location", default="version"),
        )

    @staticmethod
    def _alembic_render_item(
        type_: str,
        obj: Any,
        autogen_context: "alembic.autogenerate.api.AutogenContext",
    ):
        """Alembic render_item hook call.

        This method is called to provide python code for the given obj,
        but currently it is only used to add `sqlmodel` to the import list
        when generating migration scripts.

        See https://alembic.sqlalchemy.org/en/latest/api/runtime.html

        Args:
            type_: One of "schema", "table", "column", "index",
                "unique_constraint", or "foreign_key_constraint".
            obj: The object being rendered.
            autogen_context: Shared AutogenContext passed to each render_item call.

        Returns:
            False - Indicating that the default rendering should be used.
        """
        autogen_context.imports.add("import sqlmodel")
        return False

    @classmethod
    def alembic_init(cls):
        """Initialize alembic for the project."""
        alembic.command.init(
            config=alembic.config.Config(environment.ALEMBIC_CONFIG.get()),
            directory=str(environment.ALEMBIC_CONFIG.get().parent / "alembic"),
        )

    @classmethod
    def alembic_autogenerate(
        cls,
        connection: sqlalchemy.engine.Connection,
        message: str | None = None,
        write_migration_scripts: bool = True,
    ) -> bool:
        """Generate migration scripts for alembic-detectable changes.

        Args:
            connection: SQLAlchemy connection to use when detecting changes.
            message: Human readable identifier describing the generated revision.
            write_migration_scripts: If True, write autogenerated revisions to script directory.

        Returns:
            True when changes have been detected.
        """
        if not environment.ALEMBIC_CONFIG.get().exists():
            return False

        config, script_directory = cls._alembic_config()
        revision_context = alembic.autogenerate.api.RevisionContext(
            config=config,
            script_directory=script_directory,
            command_args=defaultdict(
                lambda: None,
                autogenerate=True,
                head="head",
                message=message,
            ),
        )
        writer = alembic.autogenerate.rewriter.Rewriter()

        @writer.rewrites(alembic.operations.ops.AddColumnOp)
        def render_add_column_with_server_default(context, revision, op):
            # Carry the sqlmodel default as server_default so that newly added
            # columns get the desired default value in existing rows.
            if op.column.default is not None and op.column.server_default is None:
                op.column.server_default = sqlalchemy.DefaultClause(
                    sqlalchemy.sql.expression.literal(op.column.default.arg),
                )
            return op

        def run_autogenerate(rev, context):
            revision_context.run_autogenerate(rev, context)
            return []

        with alembic.runtime.environment.EnvironmentContext(
            config=config,
            script=script_directory,
            fn=run_autogenerate,
        ) as env:
            env.configure(
                connection=connection,
                target_metadata=ModelRegistry.get_metadata(),
                render_item=cls._alembic_render_item,
                process_revision_directives=writer,  # type: ignore
                compare_type=False,
                render_as_batch=True,  # for sqlite compatibility
            )
            env.run_migrations()
        changes_detected = False
        if revision_context.generated_revisions:
            upgrade_ops = revision_context.generated_revisions[-1].upgrade_ops
            if upgrade_ops is not None:
                changes_detected = bool(upgrade_ops.ops)
        if changes_detected and write_migration_scripts:
            # Must iterate the generator to actually write the scripts.
            _ = tuple(revision_context.generate_scripts())
        return changes_detected

    @classmethod
    def _alembic_upgrade(
        cls,
        connection: sqlalchemy.engine.Connection,
        to_rev: str = "head",
    ) -> None:
        """Apply alembic migrations up to the given revision.

        Args:
            connection: SQLAlchemy connection to use when performing upgrade.
            to_rev: Revision to migrate towards.
        """
        config, script_directory = cls._alembic_config()

        def run_upgrade(rev, context):
            return script_directory._upgrade_revs(to_rev, rev)

        with alembic.runtime.environment.EnvironmentContext(
            config=config,
            script=script_directory,
            fn=run_upgrade,
        ) as env:
            env.configure(connection=connection)
            env.run_migrations()

    @classmethod
    def migrate(cls, autogenerate: bool = False) -> bool | None:
        """Execute alembic migrations for all sqlmodel Model classes.

        If alembic is not installed or has not been initialized for the project,
        then no action is performed.

        If there are no revisions currently tracked by alembic, then
        an initial revision will be created based on sqlmodel metadata.

        If models in the app have changed in incompatible ways that alembic
        cannot automatically generate revisions for, the app may not be able to
        start up until migration scripts have been corrected by hand.

        Args:
            autogenerate: If True, generate migration script and use it to upgrade schema
                (otherwise, just bring the schema to current "head" revision).

        Returns:
            True - indicating the process was successful.
            None - indicating the process was skipped.
        """
        if not environment.ALEMBIC_CONFIG.get().exists():
            return

        with cls.get_db_engine().connect() as connection:
            cls._alembic_upgrade(connection=connection)
            if autogenerate:
                changes_detected = cls.alembic_autogenerate(connection=connection)
                if changes_detected:
                    cls._alembic_upgrade(connection=connection)
            connection.commit()
        return True

    @classmethod
    def select(cls):
        """Select rows from the table.

        Returns:
            The select statement.
        """
        return sqlmodel.select(cls)


ModelRegistry.register(Model)


def session(url: str | None = None) -> sqlmodel.Session:
    """Get a sqlmodel session to interact with the database.

    Args:
        url: The database url.

    Returns:
        A database session.
    """
    return sqlmodel.Session(get_engine(url))


def sqla_session(url: str | None = None) -> sqlalchemy.orm.Session:
    """Get a bare sqlalchemy session to interact with the database.

    Args:
        url: The database url.

    Returns:
        A database session.
    """
    return sqlalchemy.orm.Session(get_engine(url))
