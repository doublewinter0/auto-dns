from typing import Tuple

from pythonping import ping
from tcppinglib import async_tcpping

from src.constant import NumberConstant


def get_ping_info(host: str, count: int = NumberConstant.FOUR) -> Tuple:
    resp_list = ping(host, count=count, verbose=True)

    return resp_list.stats_lost_ratio, resp_list.rtt_avg_ms


async def get_tcpping_info(host: str, port: int = NumberConstant.EIGHTY, timeout: float = NumberConstant.THREE,
                           count: int = NumberConstant.TEN, interval: float = NumberConstant.ZERO) -> Tuple:
    host = await async_tcpping(host, port, timeout, count, interval)

    return host.packet_loss / host.packets_sent, host.avg_rtt
