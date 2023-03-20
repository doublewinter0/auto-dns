import logging

import requests
from lxml import etree

from src.constant import MainConstant, NumberConstant
from src.property import ClashProperty

logger = logging.getLogger(__name__)


# @Singleton
class ClashClient:
    def __init__(self, cp: ClashProperty):
        self.__host = cp.host
        self.__port = cp.port
        self.__user = cp.user
        self.__passwd = cp.passwd

        self.__session = requests.session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()

    def login(self) -> bool:
        logger.info('用户 %s 尝试登录 OpenWrt...', self.__user)
        url = f'http://{self.__host}:{self.__port}/cgi-bin/luci'

        data = {
            'luci_username': self.__user,
            'luci_password': self.__passwd
        }

        with self.__session.post(url, data=data) as resp:
            if resp.status_code == 200:
                logger.info('用户 %s 登录成功!', self.__user)
                return True

            logger.error('用户 %s 登录失败!', self.__user, exc_info=True)
            return False

    def switch_clash(self, flag: bool) -> bool:
        url = f'http://{self.__host}:{self.__port}/cgi-bin/luci/admin/services/openclash'
        url_status = f'{url}/status'

        with self.__session.get(url_status) as status_resp:
            if status_resp.status_code == NumberConstant.HTTP_OK:
                resp_json = status_resp.json()
                if resp_json.get('clash') is flag:
                    logger.warning('open-clash 已经是 %s 状态!', flag)

                    return True

                logger.info('尝试切换 open-clash 状态...')
                data = {
                    'cbi.submit': NumberConstant.ONE
                }
                if flag:
                    data['cbid.table.1.enable'] = 'start'
                else:
                    data['cbid.table.1.disable'] = 'stop'

                # get token
                with self.__session.get(url) as clash_resp:
                    if clash_resp.status_code == NumberConstant.HTTP_OK:
                        html = etree.HTML(clash_resp.content.decode(MainConstant.UTF8))
                        token_ele = html.xpath('//input[@name="token" and @type="hidden"]')
                        data['token'] = token_ele[NumberConstant.ZERO].get('value')
                    else:
                        logger.error('获取 token 失败!', exc_info=True)
                        return False

                with self.__session.post(url, data=data) as clash_resp:
                    if clash_resp.status_code == NumberConstant.HTTP_OK:
                        logger.info('open-clash 状态切换成功!')
                        return True

                    logger.error('open-clash 状态切换失败, 状态码: %s', clash_resp.status_code)
                    return False

            logger.error('查询 open-clash 状态失败, 状态码: %s', status_resp.status_code)
            return False
