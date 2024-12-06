from typing import Callable

import google.auth
import pymysql.connections

from google.cloud.sql.connector import Connector

def cloudsql_mysql_getconn(instance: str, database: str) -> Callable[[], pymysql.connections.Connection]:
    # Default configuration to use Google Cloud SQL with MySQL
    # Initialize Python Cloud SQL Connector object
    connector = Connector()

    credentials, _ = google.auth.default()
    credentials.refresh(request=google.auth.transport.requests.Request())
    cloudsql_user = credentials.service_account_email.replace('.gserviceaccount.com', '')

    # Python Cloud SQL Connector database connection function
    def getconn() -> pymysql.connections.Connection:
        return connector.connect(
            instance,
            'pymysql',  # Use pymysql to connect to MySQL
            db=database,
            user=cloudsql_user,
            enable_iam_auth=True,
        )

    return getconn
