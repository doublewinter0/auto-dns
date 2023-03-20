import decimal
from decimal import Decimal
from typing import Union

from src.constant import NumberConstant


def get_round(num: Union[int, float], precision: int = NumberConstant.TWO) -> Decimal:
    decimal.getcontext().rounding = 'ROUND_HALF_UP'
    prefix = '0.'
    return decimal.Decimal(num).quantize(decimal.Decimal(prefix.ljust(precision + len(prefix), '0')))
