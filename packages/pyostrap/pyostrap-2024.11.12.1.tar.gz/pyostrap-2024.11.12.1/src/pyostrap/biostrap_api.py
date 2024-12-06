from datetime import date, datetime
import logging
from typing import List

from pyostrap.rest_adapter import RestAdapter
from pyostrap.util import get_rfc3339_str


class BiostrapApi:
    def __init__(
        self,
        api_key: str,
        hostname: str = "api-beta.biostrap.com",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._rest_adapter = RestAdapter(api_key, hostname, ver, ssl_verify, logger)

    # Biometrics
    def get_user_biometrics(
        self, last_timestamp: datetime, limit: int, user_id: str
    ) -> str:
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50, inclusive")

        ep_params = {
            "last-timestamp": int(last_timestamp.timestamp() * 1000),
            "limit": limit,
            "user_id": user_id,
        }
        return self._rest_adapter.get(endpoint="biometrics", ep_params=ep_params)

    # Calories
    def get_calorie_details_granular(
        self,
        user_id: str,
        date: date,
        granularity: str,
        user_timezone_offset_in_mins: int = 0,
    ) -> str:
        ep_params = {
            "user_id": user_id,
            "user_timezone_offset_in_mins": user_timezone_offset_in_mins,
            "date": date.strftime("%Y-%m-%d"),
            "granularity": granularity,
        }
        return self._rest_adapter.get(endpoint="calorie/details", ep_params=ep_params)

    # Device Information
    def get_device_info(self, user_id: str) -> str:
        ep_params = {"user_id": user_id}
        result = self._rest_adapter.get(endpoint="device-info", ep_params=ep_params)
        return result

    # Organizations
    def download_raw_data(
        self,
        target_email: str,
        start_time: datetime,
        end_time: datetime,
        user_ids: List[str],
        data_to_download: List[str],
        output_file_formats: List[str],
        anonymize_ids: bool = False,
    ) -> str:
        json_body = {
            "target_email": target_email,
            "start_time": get_rfc3339_str(start_time),
            "end_time": get_rfc3339_str(end_time),
            "user_ids": user_ids,
            "data_to_download": data_to_download,
            "output_file_formats": output_file_formats,
            "anonymize_ids": anonymize_ids,
        }
        return self._rest_adapter.post(
            endpoint="organizations/data-download/raw/send-request", data=json_body
        )

    def get_job_status(self, job_id: str) -> str:
        ep_params = {"job_id": job_id}
        return self._rest_adapter.get(
            endpoint="organizations/job-status", ep_params=ep_params
        )

    def lock_or_unlock_device_to_user(
        self,
        user_id: str,
        device_type: str,
        device_mac_address_or_id_encoded: str,
        operation: str,
    ) -> str:
        json_body = {
            "user_id": user_id,
            "device_type": device_type,
            "device_mac_address_or_id_encoded": device_mac_address_or_id_encoded,
            "operation": operation,
        }

        return self._rest_adapter.post(
            endpoint="organizations/user-device-lock", data=json_body
        )

    def get_users(self, page: int, items_per_page: int) -> str:
        ep_params = {"page": page, "items_per_page": items_per_page}
        return self._rest_adapter.get(
            endpoint="organizations/users", ep_params=ep_params
        )

    # Scores
    def get_user_scores(self, day: date, user_id: str) -> str:
        ep_params = {"date": day.isoformat(), "user_id": user_id}
        return self._rest_adapter.get(endpoint="scores", ep_params=ep_params)
    
    # Sleep
    def get_user_sleep_stats(self, day: date, user_id: str) -> str:
        ep_params = {"date": day.isoformat(), "user_id": user_id}
        return self._rest_adapter.get(endpoint="sleep", ep_params=ep_params)


    # Users
    def get_user(self, user_id: str) -> str:
        ep_params = {"user_id": user_id}
        return self._rest_adapter.get(endpoint="user", ep_params=ep_params)
