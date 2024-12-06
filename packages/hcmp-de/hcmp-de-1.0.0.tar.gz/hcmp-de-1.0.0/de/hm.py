import configparser
import json
from datetime import datetime
from random import randrange
from loguru import logger
from de.utils.hm_utils import send_to_kafka


def print_debug(message, debug):
    if debug:
        logger.debug(message)


class HealthMonitoring:
    def __init__(self, config, job_instance_id, app_name, debug=False, start_time=None):
        self.job_instance_id = job_instance_id
        self.start_time = start_time or datetime.now()
        self.config = config
        self.debug = debug
        self.common_fields = {
            "Tech": "Application",
            "SubTech": "Application",
            "appId": "app-"
                     + datetime.now().strftime("%Y%m%d%H%M%S")
                     + "-"
                     + str(randrange(1000)),
            "appName": f"{app_name}-{job_instance_id}",
            "job_instance_id": job_instance_id,
            "COMMNT": "Job successfully completed",
        }

    def log_success(self, executors=0, memory=0, cores=0, totaltimetaken=None):
        totaltimetaken = totaltimetaken or (datetime.now().timestamp() - self.start_time.timestamp())
        end_time = datetime.now()
        success_log = {
            **self.common_fields,
            "startTime": self.start_time.strftime("%d-%b-%Y %I:%M.%S %p"),
            "endtime": end_time.strftime("%d-%b-%Y %I:%M.%S %p"),
            "deploymode": "driver",
            "master": "",
            "executors": executors,
            "memory": memory,
            "cores": cores,
            "MAXTIMESTAMP": end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "TIMESTAMP": end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "totaltimetaken": int(totaltimetaken),
            "AVERAGETIME": 20,
            "status": "completed",
            "RUNNINGINTERVAL": 0,
            "CONCURRENCY": 0,
            "MEMORYOVERHEAD": 0,
            "AVGTIME": 20,
            "type": "healthmonitoring"
        }
        print_debug(f"Success Log JSON: {success_log}", self.debug)
        send_to_kafka(self.config, success_log)

    def log_failure(self, error):
        failure_log = {
            "Technology": self.common_fields["Tech"],
            "SubTech": self.common_fields["SubTech"],
            "appId": self.common_fields["appId"],
            "appName": self.common_fields["appName"],
            "insert_timestamp": datetime.now().strftime("%d-%b-%Y %I:%M.%S %p"),
            "error": f"{error}",
            "errorData": str(error),
            "type": "error",
            "job_instance_id": self.job_instance_id
        }
        print_debug(f"Failure Log JSON: {failure_log}", self.debug)
        send_to_kafka(self.config, failure_log)
