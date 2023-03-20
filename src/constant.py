from dataclasses import dataclass


@dataclass
class ConfigConstant:
    CRON = 'cron'
    ENV = 'env'
    LOG = 'log'
    SCHEDULER = 'apscheduler'
    THREAD = 'thread'


@dataclass
class MainConstant:
    CONFIG = 'config.yml'
    LOG_CONFIG = 'log.yml'
    MAIN = '__main__'
    READ_ONLY = 'r'
    WRITE_BINARY = 'wb'
    TMP_DIR = 'runtime/tmp'
    LOG_DIR = 'runtime/log'
    UTF8 = 'UTF-8'


@dataclass
class NumberConstant:
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    TEN = 10
    THIRTY = 30
    SIXTY = 60
    EIGHTY = 80
    HUNDRED = 100
    TWO_HUNDRED = 200
    SIX_HUNDRED = 600
    THOUSAND = 1000

    HTTP_OK = TWO_HUNDRED


@dataclass
class PunctuationConstant:
    COMMA = ','
    COLON = ':'
    SEMICOLON = ';'
    QUESTION = '?'


@dataclass
class TimeFormatConstant:
    RFC_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    U_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    STANDARD_DATE = '%Y-%m-%d'
    STANDARD_DATE_TIME = '%Y-%m-%d %H:%M:%S'
    HOUR_DATE_TIME = '%Y-%m-%d %H:%M'

    COMPACT_DATE = '%Y%m%d'

    SHORT_STANDARD_DATE = '%Y-%-m-%-d'


@dataclass
class TimeZoneConstant:
    SHANGHAI = 'Asia/Shanghai'
    UTC = 'UTC'
