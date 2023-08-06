import subprocess
from typing import Tuple

from src.constant import MainConstant, NumberConstant


def get_high_quality_ip() -> Tuple:
    with subprocess.Popen([
        'lib/cf/CloudflareST',
        '-url', 'https://cdn.cloudflare.steamstatic.com/steam/apps/256843155/movie_max.mp4',
        '-p', '0',
        '-f', 'lib/cf/ip.txt',
        '-o', 'lib/cf/result.csv'
    ]) as proc:
        stdout, stderr = proc.communicate()

        with open('lib/cf/result.csv', encoding=MainConstant.UTF8) as result:
            r_list = result.readlines()[NumberConstant.ONE:NumberConstant.THREE]

        return proc.returncode, stdout, stderr, r_list
