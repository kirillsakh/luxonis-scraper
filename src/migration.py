import logging
import psycopg
from sqlalchemy import create_engine

from config_manager import Config, ConfigManager
from database.models import Base
from logging_config import configure_logging


configure_logging()

logger = logging.getLogger(__name__)

cfg: Config = ConfigManager.initialize_from_env().config


def initialize_database(user: str, password: str, host: str, port: str, database: str):
    """
    Initialize the PostgreSQL database if it does not exist.

    Args:
        user (str): PostgreSQL user.
        password (str): PostgreSQL password.
        host (str): PostgreSQL host.
        port (str): PostgreSQL port.
        database (str): PostgreSQL database name.
    """
    connection_str = f'postgresql://{user}:{password}@{host}:{port}'
    try:
        with psycopg.connect(connection_str, autocommit=True) as conn:
            cursor = conn.cursor()
            logger.info('Connected to PostgreSQL.')

            # Check if the database already exists
            cursor.execute(
                psycopg.sql.SQL("SELECT datname FROM pg_database WHERE datname = {}").format(
                    psycopg.sql.Literal(cfg.psql_database)
                )
            )
            existing_databases = cursor.fetchall()

            if not existing_databases:
                # Create the database
                create_database_statement = psycopg.sql.SQL("CREATE DATABASE {}").format(
                    psycopg.sql.Identifier(cfg.psql_database)
                )

                cursor.execute(create_database_statement)
                logger.info(f'Created "{database}" database.')
            else:
                logger.info(f'"{database}" database already exists.')

    except Exception as e:
        logger.error(f'Error while initializing the database: {e}', exc_info=True)


def initialize_tables(user: str, password: str, host: str, port: str, database: str):
    """
    Initialize tables in the specified PostgreSQL database.

    Args:
        user (str): PostgreSQL user.
        password (str): PostgreSQL password.
        host (str): PostgreSQL host.
        port (str): PostgreSQL port.
        database (str): PostgreSQL database name.
    """
    logger.info(f'Initializing tables in "{database}" database.')
    connection_str = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_str)
    Base.metadata.create_all(engine)
    logger.info(f'Table initialization completed.')


def main():
    kwargs = dict(
        user=cfg.psql_user,
        password=cfg.psql_password,
        host=cfg.psql_host,
        port=cfg.psql_port,
        database=cfg.psql_database
    )
    # Initialize the database if it does not exist
    initialize_database(**kwargs)

    # Initialize tables if they do not exist
    initialize_tables(**kwargs)


if __name__ == '__main__':
    main()
