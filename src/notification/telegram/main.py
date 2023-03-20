import asyncio
import logging
from typing import List, Tuple, Union

import prettytable as pt
import telegram
from prettytable import ALL
from telegram.constants import ParseMode

from src.constant import NumberConstant
from src.property import TelegramProperty

tp = TelegramProperty()
BOT_TOKEN = tp.telegram_bot_token
CHAT_ID = tp.telegram_chat_id

logger = logging.getLogger(__name__)


async def __send_text(chat_id: Union[int, str], text: str, parse_mode: str,
                      try_num: int = NumberConstant.THREE) -> None:
    bot = telegram.Bot(token=BOT_TOKEN)
    tried_num = NumberConstant.ONE
    while tried_num < try_num:
        try:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
            return
        except Exception:
            logger.error('发送通知失败, 异常栈如下:', exc_info=True)
            logger.warning('开始第 %s 次尝试...', tried_num)

            await asyncio.sleep(NumberConstant.SIXTY * tried_num)
            tried_num += NumberConstant.ONE


async def send_nip_info(nip_info: List[Tuple]) -> None:
    header = ['IP_ADDR', 'DELAY(ms)', 'DOWNLOAD(MB/s)']
    table = pt.PrettyTable(header, border=True, hrules=ALL)
    for h in header:
        table.align[h] = 'c'

    if nip_info:
        for ip, delay, dl_rate in nip_info:
            table.add_row([ip, delay, dl_rate])

        txt = 'CDN 记录已更新, 详情见表格'
        logger.info('%s\n%s', txt, table)

        await __send_text(CHAT_ID, f"<b>{txt}</b>", parse_mode=ParseMode.HTML)
        await __send_text(CHAT_ID, f'```\n{table}```', parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await __send_text(CHAT_ID, '<b>CDN 记录更新失败, 详情见日志</b>', parse_mode=ParseMode.HTML)
