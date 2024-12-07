import andromeda.logger_function as logger_function
import psycopg2
from config import DefaultConfig
from psycopg2.extras import RealDictCursor
from andromeda.logger_function import get_current_function_name


DB_CONFIG = DefaultConfig()


async def db_connection():
    logger_function.info(
        f"Current function {await get_current_function_name()} Connecting to the database"
    )
    connection = psycopg2.connect(
        host=DB_CONFIG.DB_HOST,
        user=DB_CONFIG.DB_USER,
        password=DB_CONFIG.DB_PASSWORD,
        dbname=DB_CONFIG.DB_NAME,
        port=5432,
    )
    logger_function.info("Connected to the database successfully")
    return connection


async def execute_query(connection, query, params=None):
    """
    This function executes an SQL query on the provided connection.

    Args:
        connection (mysql.connector.connection): The connection object to the database.
        query (str): The SQL query to execute.
        params (list, optional): A list of parameters for the query. Defaults to None.

    Returns:
        object: The result of the query execution,
                or None on error.
    """
    logger_function.info(f"Executing the query: {query}")
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        logger_function.info(f"Query executed successfully with : {params}")
        return cursor, ""
    except Exception as err:
        logger_function.error(f"Error occurred while executing the query: {err}")
        return None, err


async def close_connection(connection, cursor):
    """
    This function closes the connection to the MySQL database server.

    Args:
        connection (mysql.connector.connection): The connection object to close.
    """
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    logger_function.info("Connection closed successfully")
