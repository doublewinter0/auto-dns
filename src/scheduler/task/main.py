import asyncio
import decimal
import logging
import time
from typing import Dict, List, Tuple

from src.constant import NumberConstant, PunctuationConstant
from src.helper.cf.main import get_high_quality_ip
from src.helper.clash.main import ClashClient
from src.helper.ping.main import get_ping_info
from src.notification.telegram.main import send_nip_info
from src.property import PropertyConfig
from src.service.qc.record import Record
from src.util.main import get_round

logger = logging.getLogger(__name__)


class CDN:
    __last_updated = int(round(time.time()))

    __DAY_IN_SECONDS = 86400
    __pc = PropertyConfig()

    @classmethod
    async def main(cls, record_ids: List[int]) -> None:

        cur_recs = [await cls.__get_cur_record(i) for i in record_ids]
        # 所有记录执行相同操作, 取其中一条获取原记录
        c_ip = cur_recs[NumberConstant.ZERO]['record'][NumberConstant.ZERO]
        logger.info('获取到当前 ip: %s, 对其进行质检...', c_ip)
        check_result = await cls.__check(c_ip, count=NumberConstant.TEN)
        update_interval = int(round(time.time())) - cls.__last_updated

        fp = cls.__pc.fp

        if fp.enabled and update_interval >= cls.__DAY_IN_SECONDS * fp.interval:
            logger.warning('记录距上次更新时间超过 %s 天, 将强制更新记录', fp.interval)
        elif check_result:
            logger.info('质检通过, 不需要更新 ip')
            return
        else:
            logger.warning('质检未通过, 需更新 ip')

        cp = cls.__pc.cp
        if cp.enabled:
            async with ClashClient(cp) as client:
                await client.login()
                flag = await client.switch_clash(False)
                if not flag:
                    return
                await asyncio.sleep(NumberConstant.THIRTY)

                logger.info('开始获取优质 ip...')
                nip_info = await cls.__update_rec(cur_recs)

                await client.switch_clash(True)
                # await asyncio.sleep(NumberConstant.SIXTY)
        else:
            logger.info('开始获取优质 ip...')
            nip_info = await cls.__update_rec(cur_recs)

        if cls.__pc.tp.enabled:
            await asyncio.sleep(NumberConstant.HUNDRED * NumberConstant.THREE)
            logger.info('向电报发送更新通知...')
            await send_nip_info(nip_info)

    @classmethod
    async def __check(cls, host: str, count: int) -> bool:
        loss_ratio, avg_ms = get_ping_info(host, count=count)
        decimal.getcontext().rounding = "ROUND_HALF_UP"
        logger.info('ip: %s, 丢包率: %s, 平均延迟: %s ms',
                    host, get_round(loss_ratio), avg_ms)
        if loss_ratio >= NumberConstant.ONE / NumberConstant.TEN or avg_ms > NumberConstant.THREE * NumberConstant.HUNDRED:
            return False
        return True

    @classmethod
    async def __get_cur_record(cls, record_id: int) -> Dict:
        record = Record()
        record_info = await record.get_record_info(record_id)
        data = record_info['data']
        domain = data['domain_name']
        zone = data['zone_name']
        record = data['record']
        result = []
        for r in record:
            result += [d['value'] for d in r['data']]

        return {'domain': domain, 'zone': zone, 'record_id': record_id, 'record': result}

    @classmethod
    async def __update_rec(cls, cur_recs: List,
                           retry_times: int = NumberConstant.TWO,
                           nip_info=None) -> List[Tuple] | None:
        if nip_info is None:
            nip_info = []
        r = get_high_quality_ip()
        if not r[NumberConstant.ZERO]:
            r_list = r[-NumberConstant.ONE]
            for idx, val in enumerate(r_list):
                x = val.split(PunctuationConstant.COMMA)
                ip = x[NumberConstant.ZERO]
                delay = x[-NumberConstant.TWO]
                dl_rate = float(x[-NumberConstant.ONE])
                nip_info.append((ip, delay, dl_rate))
                if idx == (len(r_list) - NumberConstant.ONE) and nip_info[NumberConstant.ZERO][
                        NumberConstant.TWO] < NumberConstant.TEN and retry_times > NumberConstant.ZERO:
                    logger.warning('下载速率: %s MB/s, 第 %s 次尝试...', dl_rate, NumberConstant.THREE - retry_times)

                    return await cls.__update_rec(cur_recs, retry_times - NumberConstant.ONE, nip_info)

                logger.info('获取到 ip: %s, 延迟: %s ms, 下载速率: %s MB/s',
                            ip, delay, dl_rate)

            nip_info.sort(key=lambda e: e[NumberConstant.TWO], reverse=True)
            nip = [i[NumberConstant.ZERO] for i in nip_info][NumberConstant.ZERO:NumberConstant.TWO]
            logger.info('开始更新 ip...')
            record = Record()
            for r in cur_recs:
                resp = await record.update_record(domain=r['domain'], zone=r['zone'], record_id=r['record_id'],
                                                  records=nip)
                if resp['code']:
                    logger.error('更新 ip 错误: %s', resp['message'])
                    return None

            cls.__last_updated = int(round(time.time()))

            return nip_info

        logger.error('获取优质 ip 失败!')
        return None
