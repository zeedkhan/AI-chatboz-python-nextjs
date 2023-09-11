import os
from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine
import json
import googleapiclient.discovery
import re
from google.oauth2.service_account import Credentials

# lib - auth
# https://google-auth.readthedocs.io/en/master/user-guide.html
# lib - sql
# https://github.com/GoogleCloudPlatform/cloud-sql-python-connector
# env:
# https://stackoverflow.com/questions/35159967/setting-google-application-credentials-for-bigquery-python-cli


def get_key_value_pairs(input_string, keys):
    pairs = re.split(r', (?=\w+:)', input_string)

    result = {}

    for pair in pairs:
        key, value = map(str.strip, pair.split(':', 1))
        if key in keys:
            if value.startswith('[') and value.endswith(']'):
                value = [item.strip()
                         for item in value[1:-1].split(',') if item.strip()]
            result[key] = value

    return result


# set env["key"] = "path_to_json.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"


class GoogleCloudSetting:
    """
    Class to hold Google Cloud settings.
    """

    project_id = "sigma-composite-393005"

    SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin',
              "https://www.googleapis.com/auth/cloud-platform"]

    SERVICE_ACCOUNT_FILE = "application_default_credentials.json"

    AI_DB_USER = "seed-jr"
    AI_DB_PASS = "seed-jr"


def auth():
    service_account_info = json.load(
        open(GoogleCloudSetting.SERVICE_ACCOUNT_FILE))
    # Append the target directory path to the current directory
    credentials = Credentials.from_service_account_info(
        service_account_info, scopes=GoogleCloudSetting.SCOPES)
    return credentials


# helper function to return SQLAlchemy connection pool
connector = Connector()


def getconn(connection: str, user: str, password: str, db: str):
    # function used to generate database connection
    conn = connector.connect(
        connection,  # Cloud SQL Instance Connection Name
        "pg8000",
        user=user,
        password=password,
        db=db,
    )

    return conn


async def get_db(input_str, *args, **kwargs):
    cred = auth()
    sqladmin = googleapiclient.discovery.build(
        'sqladmin', 'v1beta4', credentials=cred)

    # selected_keys = ['project', 'instance', "database"]
    # keys = get_key_value_pairs(input_string=input_str, keys=selected_keys)
    keys = json.loads(input_str)

    try:
        request = sqladmin.databases().get(
            project=keys["project"],
            instance=keys["instance"],
            database=keys["database"]
        ).execute()

        return {
            "answerBox": {
                "answer": f"Database detail: \n{request}"
            }
        }
    except ValueError as e:
        return {
            "answerBox": {
                "answer": f"{e.message | e}"
            }
        }


async def get_databases(input_str, *args, **kwargs):
    cred = auth()
    sqladmin = googleapiclient.discovery.build(
        'sqladmin', 'v1beta4', credentials=cred)

    # selected_keys = ['project', 'instance']
    # keys = get_key_value_pairs(input_string=input_str, keys=selected_keys)

    keys = json.loads(input_str)

    try:
        request = sqladmin.databases().list(
            project=keys["project"],
            instance=keys["instance"]
        ).execute()

        return {
            "answerBox": {
                "answer": f"Database list: \n{request}"
            }
        }
    except ValueError as e:
        return {
            "answerBox": {
                "answer": f"{e.message}"
            }
        }


async def get_instances(input_str: str, *args, **kwargs):
    cred = auth()
    sqladmin = googleapiclient.discovery.build(
        'sqladmin', 'v1beta4', credentials=cred)

    # selected_keys = ["project"]
    # values = get_key_value_pairs(input_string=input_str, keys=selected_keys)
    # project = values["project"]
    input_str.replace("'", '"')
    project = json.loads(input_str)

    if project:
        try:
            request = sqladmin.instances().list(
                project=project["project"]).execute()
            items = request["items"]
            return {
                "answerBox": {
                    "answer": f"All instances: \n {items}"
                }
            }
        except ValueError as e:
            return {
                "answerBox": {
                    "answer": f"{e.message}"
                }
            }

    return {
        "answerBox": {
            "answer": "Failed, missing project=projectId"
        }
    }


def connect_db(connection: str, user: str, password: str, db: str):
    # initialize Cloud SQL Python Connector as context manager
    # initialize connection pool
    pool = create_engine(
        "postgresql+pg8000://",
        creator=getconn(
            connection=connection,
            user=user,
            password=password,
            db=db
        ),
    )

    return pool
