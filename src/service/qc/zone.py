import logging
from datetime import datetime
from typing import Dict
from urllib import parse

from httpx import AsyncClient

from src.enum.http import HttpMethod
from src.helper.qc.http import get_common_headers, get_common_params
from src.util.qc.main import get_auth, get_signature, get_sorted_params

logger = logging.getLogger(__name__)


class Zone:
    def __init__(self):
        self.__api_url = 'http://api.routewize.com/v1/user/zones'
        self.__resource = '/v1/user/zones'

    async def get_zones(self) -> Dict | None:
        async with AsyncClient() as session:
            utc_now = datetime.utcnow()
            params = get_sorted_params(get_common_params())
            url_encoded = parse.urlencode(params)
            sign = get_signature(HttpMethod.GET, utc_now,
                                 f'{self.__resource}?{url_encoded}')
            headers = get_common_headers(get_auth(sign), utc_now)

            resp = await session.get(f'{self.__api_url}{self.__resource}',
                                     headers=headers, params=params)
            resp_json = resp.json()
            if not resp_json['code']:
                return resp_json

            logger.error('zone 查询失败: %s', resp_json['message'])
            return None
