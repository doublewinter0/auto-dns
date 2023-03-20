from src.constant import PunctuationConstant
from src.helper.singleton import Singleton


@Singleton
class QCloudProperty:
    def __init__(self, config_property: dict = None):
        self.__access_key_id = config_property.get('access_key_id')
        self.__access_key_secret = config_property.get('access_key_secret')

    @property
    def access_key_id(self) -> str:
        return self.__access_key_id

    @property
    def access_key_secret(self) -> str:
        return self.__access_key_secret


@Singleton
class TelegramProperty:
    def __init__(self, config_property: dict = None):
        self.__enabled = config_property.get('enabled')
        self.__telegram_bot_token = config_property.get('telegram_bot_token')
        self.__telegram_chat_id = config_property.get('telegram_chat_id')

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @property
    def telegram_bot_token(self) -> str:
        return self.__telegram_bot_token

    @property
    def telegram_chat_id(self) -> str:
        return self.__telegram_chat_id


@Singleton
class ForceProperty:
    def __init__(self, config_property: dict = None):
        self.__enabled = config_property.get('enabled')
        self.__interval = config_property.get('interval')

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @property
    def interval(self) -> int:
        return self.__interval


@Singleton
class ClashProperty:
    def __init__(self, config_property: dict = None):
        self.__enabled = config_property.get('enabled')
        self.__host = config_property.get('host')
        self.__port = config_property.get('port')
        self.__user = config_property.get('user')
        self.__passwd = config_property.get('passwd')

    def __str__(self) -> str:
        return str(self.__dict__)

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> int:
        return self.__port

    @property
    def user(self) -> str:
        return self.__user

    @property
    def passwd(self) -> str:
        return self.__passwd


@Singleton
class RecordProperty:
    def __init__(self, config_property: dict = None):
        self.__ids = config_property.get('ids')

    @property
    def ids(self) -> list[int]:
        return list(map(int, self.__ids.split(PunctuationConstant.COMMA)))


@Singleton
class PropertyConfig:
    def __init__(self, config_dict: dict = None):
        self.__config_dict = config_dict

        self.__qc = QCloudProperty(self.__config_dict.get('qcloud'))
        self.__rp = RecordProperty(self.__config_dict.get('record'))
        self.__fp = ForceProperty(self.__config_dict.get('force_update'))
        self.__cp = ClashProperty(self.__config_dict.get('clash'))
        self.__tp = TelegramProperty(self.__config_dict.get('notify').get('telegram'))

    @property
    def qc(self) -> QCloudProperty:
        return self.__qc

    @property
    def rp(self) -> RecordProperty:
        return self.__rp

    @property
    def fp(self) -> ForceProperty:
        return self.__fp

    @property
    def cp(self) -> ClashProperty:
        return self.__cp

    @property
    def tp(self) -> TelegramProperty:
        return self.__tp
