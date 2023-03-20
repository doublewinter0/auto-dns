import base64
import hmac
import operator
from datetime import datetime
from hashlib import sha256
from typing import Dict

from src.constant import MainConstant, NumberConstant, TimeFormatConstant
from src.enum.http import HttpMethod
from src.property import QCloudProperty

qc = QCloudProperty()
QY_ACCESS_KEY_ID = qc.access_key_id
QY_ACCESS_KEY_SECRET = qc.access_key_secret


def get_signature(verb: HttpMethod, time_stamp: datetime, resource: str) -> str:
    now = time_stamp or datetime.utcnow()
    string_to_sign = f'{verb.name}\n{now.strftime(TimeFormatConstant.RFC_FORMAT)}\n{resource}'

    h = hmac.new(key=QY_ACCESS_KEY_SECRET.encode(
        encoding=MainConstant.UTF8), digestmod=sha256)
    h.update(msg=string_to_sign.encode(encoding=MainConstant.UTF8))

    return base64.b64encode(h.digest()).strip().decode(MainConstant.UTF8)


def get_auth(sign: str) -> str:
    return f'QC-HMAC-SHA256 {QY_ACCESS_KEY_ID}:{sign}'


def get_iaas_url(url: str, resource: str, signature: str) -> str:
    return f'{url}?{resource}&signature={signature}'


def get_sorted_params(_old: Dict) -> Dict:
    return dict(sorted(_old.items(), key=operator.itemgetter(NumberConstant.ZERO)))
