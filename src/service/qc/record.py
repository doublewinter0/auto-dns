import json
import logging
from datetime import datetime
from typing import Dict, List

import aiohttp

from src.constant import NumberConstant
from src.enum.http import HttpMethod
from src.helper.qc.http import get_common_headers
from src.util.qc.main import get_auth, get_signature

logger = logging.getLogger(__name__)


class Record:
    def __init__(self):
        self.__api_url = 'http://api.routewize.com'
        self.__resource = '/v1/dr_id'

    async def get_record_info(self, record_id: int) -> Dict:
        async with aiohttp.ClientSession() as session:
            utc_now = datetime.utcnow()
            sign = get_signature(HttpMethod.GET, utc_now,
                                 f'{self.__resource}/{record_id}')
            headers = get_common_headers(get_auth(sign), utc_now)

            async with session.get(f'{self.__api_url}{self.__resource}/{record_id}', headers=headers) as resp:
                return await resp.json()

    async def update_record(self, domain: str, zone: str, record_id: int, records: List[str], rd_class: str = 'IN',
                            rd_type: str = 'A', view_id: int = NumberConstant.THREE,
                            ttl: int = NumberConstant.SIX_HUNDRED,
                            mode: int = NumberConstant.TWO) -> Dict:
        async with aiohttp.ClientSession() as session:
            utc_now = datetime.utcnow()
            sign = get_signature(HttpMethod.POST, utc_now,
                                 f'{self.__resource}/{record_id}')
            headers = get_common_headers(get_auth(sign), utc_now)
            records = [{'weight': NumberConstant.ZERO,
                        'values': [{'value': i, 'status': NumberConstant.ONE} for i in records]}]
            data = {
                'domain_name': domain.replace(zone, ''),
                'view_id': view_id,
                'type': rd_type,
                'ttl': ttl,
                'class': rd_class,
                'record': json.dumps(records),
                'mode': mode
            }
            async with session.post(f'{self.__api_url}{self.__resource}/{record_id}',
                                    headers=headers, data=data) as resp:
                resp_json = await resp.json()
                if not resp_json['code']:
                    logger.info('域名 %s 记录更新成功!', domain)
                else:
                    logger.error('域名 %s 记录更新失败: %s', domain,
                                 resp_json['message'])

                return resp_json
