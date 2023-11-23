from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Generator


@contextmanager
def create_database_session(user: str, password: str, host: str, port: str, database: str) -> Generator[Session, None, None]:
    """
    Context manager to create a SQLAlchemy database session.

    Args:
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        host (str): The hostname or IP address of the database server.
        port (str): The port on which the database server is listening.
        database (str): The name of the database.

    Yields:
        Session: An SQLAlchemy database session.
    """
    connection_str = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_str, pool_size=5, max_overflow=10)
    session = Session(engine)

    try:
        yield session
    finally:
        session.close()
