import requests
import json
import time
import os
import subprocess

from bs4 import BeautifulSoup

resolution_dict = {'1024x768': 'XGA', '1152x864': 'XGA+',
                   '1280x720': 'HD', '1280x768': 'WXGA', '1280x1024': 'SXGA', '1366x768': 'WXSGA+', '1440x900': 'WXGA+',
                   '1400x1050': 'SXGA+', '1600x1024': 'WSXGA', '1680x1050': 'WSXGA+', '1600x1200': 'UXGA',
                   '1920x1080': 'Full_HD', '1920x1200': 'WUXGA', '2048x1536': 'QXGA', '2560x1440': 'WQHD',
                   '2560x1600': 'WQXGA', '2560x2048': 'QSXGA', '3200x2048': 'WQSXGA', '3200x2400': 'QUXGA',
                   '3840x2160': 'QFHD', '4096x2160': '4K_Ultra_HD', '3840x2400': 'WQUXGA', '5120x4096': 'HSXGA',
                   '6400x4096': 'WHSXGA', '6400x4800': 'HUXGA', '7680x4320': '8K_Ultra_HD', '7680x4800': 'WHUXGA',
                   '4096x3072': '协会标准(4k)',
                   }

bing_url = 'http://cn.bing.com'

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""


def get_wallpaper():
    get_params = {
        'format': 'js',
        'idx': 0,
        'n': 1,
        'nc': int(time.time() * 1000),
        'pid': 'hp',
        'video': 1
    }
    r = requests.get(f'{bing_url}/HPImageArchive.aspx', get_params)
    last_image = str()
    if r.ok:
        data = r.content.decode()
        j = json.loads(BeautifulSoup(data, 'lxml').text)
        for image in j['images']:
            for resolution, declare in resolution_dict.items():
                r2 = requests.get(f'{bing_url}{image["urlbase"]}_{resolution}.jpg')
                if r2.ok:
                    path = f'{src}image/{resolution}'
                    if not os.path.exists(path):
                        os.mkdir(path)
                    with open(f'{path}/{os.path.basename(r2.url)}', 'wb') as jpg:
                        jpg.write(r2.content)
                        last_image = f'{os.getcwd()}/{jpg.name}'
    if last_image is None or len(last_image) == 0:
        return None
    else:
        return last_image


def set_wallpaper(s):
    subprocess.Popen(SCRIPT % s, shell=True)


if __name__ == '__main__':
    src = '/Users/eindex/PycharmProjects/bing-wallpaper/'
    if not os.path.exists(src + 'image'):
        os.mkdir(src + 'image')
    img = get_wallpaper()
    if img:
        set_wallpaper(img)
