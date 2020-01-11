#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from configparser import ConfigParser
import os
import re
import time
import sys
from lxml import etree

config_file = 'config.ini'
config = ConfigParser()

if os.path.exists(config_file):
    try:
        config.read(config_file, encoding='UTF-8')
    except:
        print('[-]Config.ini read failed! Please use the offical file!')
else:
    print('[+]config.ini: not found, creating...', end='')
    with open("config.ini", "wt", encoding='UTF-8') as code:
        print("[common]", file=code)
        print("main_mode = 1", file=code)
        print("failed_output_folder = failed", file=code)
        print("success_output_folder = JAV_output", file=code)
        print("", file=code)
        print("[proxy]", file=code)
        print("proxy=", file=code)
        print("timeout=10", file=code)
        print("retry=3", file=code)
        print("", file=code)
        print("[Name_Rule]", file=code)
        print("location_rule=actor+'/'+number", file=code)
        print("naming_rule=number+'-'+title", file=code)
        print("", file=code)
        print("[update]", file=code)
        print("update_check=1", file=code)
        print("", file=code)
        print("[media]", file=code)
        print("media_warehouse=emby", file=code)
        print("#emby plex kodi", file=code)
        print("", file=code)
        print("[escape]", file=code)
        print("literals=\\", file=code)
        print("", file=code)
        print("[movie_location]", file=code)
        print("path=", file=code)
        print("", file=code)
        print('.', end='')
    time.sleep(2)
    print('.')
    print('[+]config.ini: created!')
    print('[+]Please restart the program!')
    time.sleep(4)
    os._exit(0)
    try:
        config.read(config_file, encoding='UTF-8')
    except:
        print('[-]Config.ini read failed! Please use the offical file!')


def getDataState(json_data):  # 元数据获取失败检测
    if json_data['title'] == '' or json_data['title'] == 'None' or json_data['title'] == 'null':
        return 0
    else:
        return 1


def ReadMediaWarehouse():
    return config['media']['media_warehouse']


def UpdateCheckSwitch():
    check = str(config['update']['update_check'])
    if check == '1':
        return '1'
    elif check == '0':
        return '0'
    elif check == '':
        return '0'


def getXpathSingle(htmlcode, xpath):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result1 = str(html.xpath(xpath)).strip(" ['']")
    return result1


def get_html(url, cookies=None):  # 网页请求核心
    try:
        proxyflag = config['proxy']['proxy_enable']
        proxy = ''
        if proxyflag == 1:
            proxy = config['proxy']['proxy']
        timeout = int(config['proxy']['timeout'])
        retry_count = int(config['proxy']['retry'])
    except:
        print('[-]Proxy config error! Please check the config.')
    i = 0
    while i < retry_count:
        try:
            if proxy != '':
                proxies = {"http": "http://" + proxy,
                           "https": "https://" + proxy}
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'}
                getweb = requests.get(
                    str(url), headers=headers, timeout=timeout, proxies=proxies, cookies=cookies, verify=False)
                getweb.encoding = 'utf-8'
                return getweb.text
            else:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
                getweb = requests.get(
                    str(url), headers=headers, timeout=timeout, cookies=cookies, verify=False)
                getweb.encoding = 'utf-8'
                return getweb.text
        except requests.exceptions.RequestException:
            i += 1
            print('[-]Connect retry '+str(i)+'/'+str(retry_count))
        except requests.exceptions.ConnectionError:
            i += 1
            print('[-]Connect retry '+str(i)+'/'+str(retry_count))
        except requests.exceptions.ProxyError:
            i += 1
            print('[-]Connect retry '+str(i)+'/'+str(retry_count))
        except requests.exceptions.ConnectTimeout:
            i += 1
            print('[-]Connect retry '+str(i)+'/'+str(retry_count))
    print('[-]Connect Failed! Please check your Proxy or Network!')
