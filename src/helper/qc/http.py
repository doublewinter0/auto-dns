from datetime import datetime
from typing import Dict

from src.constant import NumberConstant as Number, TimeFormatConstant as TimeFormat


def get_api_base() -> str:
    return 'https://api.qingcloud.com/iaas/'


def get_common_headers(auth: str, time_stamp: datetime = None) -> Dict:
    now = time_stamp or datetime.utcnow()
    headers = {
        'Authorization': auth,
        'Date': now.strftime(TimeFormat.RFC_FORMAT)
    }

    return headers


def get_common_params() -> Dict:
    params = {
        'limit': Number.TEN,
        'offset': Number.ZERO,
        # 'refresh': Number.ZERO
    }

    return params
