import andromeda.logger_function as logger_function
from connect_db import db_connection, execute_query


class TenantDetails:
    """Storing the temporary testing data"""

    async def get_db_details(self, user_id, querys):
        connection_db = await db_connection()
        params = (user_id,)
        cursor, err = await execute_query(
            connection=connection_db, query=querys, params=params
        )
        logger_function.info(f"DB query executed successfully with : {cursor}")
        if cursor:
            db_response = cursor.fetchone()
            if db_response:
                return dict(db_response), None
        else:
            logger_function.warning(
                f"couldn't find the teams in DB for this User ID: {user_id}")
        return None, err

    async def get_db_activity_details(self, params, query_data):
        """

        Args:
            params:
            querys:

        Returns:

        """
        connection_db = await db_connection()
        cursor, err = await execute_query(
            connection=connection_db, query=query_data, params=params
        )
        logger_function.info(f"DB query executed successfully with : {cursor}")
        if cursor:
            db_response = cursor.fetchone()
            if db_response:
                return dict(db_response), None
        else:
            logger_function.warning(f"couldn't find the teams in DB for this User ID:")
        return None, err

    async def insert_db_activity_details(self, params, query_data):
        """

        Args:
            query_data:
            params:

        Returns:

        """
        connection_db = await db_connection()
        _, err = await execute_query(
            connection=connection_db, query=query_data, params=params
        )
        if err:
            logger_function.error(f"Error in inserting the db activity details {err}")
        connection_db.commit()
        connection_db.close()
        return None, err
