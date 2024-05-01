"""
### The Activity DAG

This DAG will help me decide what to do today. It uses the [BoredAPI](https://www.boredapi.com/) to do so.
"""

# task play the pythonOperator role, here
from airflow.decorators import dag, task
from airflow.models import Variable
from pendulum import datetime

import requests

API = "https://www.boredapi.com/api/activity"


# Dag definition
@dag(
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    tags=["activity"],
    doc_md=__doc__,
    description="Retreive an activity from an API",
    catchup=False,
)
def find_activity():

    # Define the get_activity task
    @task
    def get_activity():
        """Get an activity from an API"""
        r = requests.get(API, timeout=10)

        return r.json()

    @task
    def write_activity_to_file(response):
        """Write an activity to a file"""

        file_path = Variable.get("activity_file")
        with open(file_path, "w") as f:
            f.write(f"Today you will: {response['activity']}\r\n")

        return file_path

    @task
    def read_activity_from_file(file_path):
        """Read an activity from a file"""
        with open(file_path, "r") as f:
            print(f.read())

    # Calling our tasks
    response = get_activity()
    file_path = write_activity_to_file(response)
    read_activity_from_file(file_path)


# Call the dag
find_activity()
