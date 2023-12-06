from json import JSONDecodeError
import os
import sys
import time
import requests

from datetime import datetime
from dotenv import load_dotenv

sys.path.append('C:\Maki\WWL\\report_by_subid')

from kt_comparison.utils import get_date_list, get_week_list

load_dotenv()


class WWLTraffWorldChecker:
    def __init__(self):
        self.session = self._login()

    @staticmethod
    def _login():
        session = requests.Session()
        headers = {
            'authority': 'wwltraffworld.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'states=v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6ImJmOTVkN2VjNDUzZTE2Mzc0NDcxZWNhZGI0NWM4YjE4IiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0Lk5XQUY3Qkp4VmlrMlhzJTJGN1VuJTJGWWVnbjFRVDFuRE1LdlBvcGhGYzR5YnJ2ai54V0NIdyUyRmEiLCJ0aW1lc3RhbXAiOjE2ODc4NDk2Njd9.NTI66Xsltu0Cn9KaOS14O8WqXKf3z5dclOcGPSqT5fI; keitaro=fcuavlar3iju8gm09aelfd20hm',
            'origin': 'https://wwltraffworld.com',
            'referer': 'https://wwltraffworld.com/admin/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        params = {
            'object': 'auth.login',
        }

        json_data = {
            'login': os.environ.get('KEITARO_LOGIN'),
            'password': os.environ.get('KEITARO_PASSWORD'),
        }

        session.post('https://wwltraffworld.com/admin/', params=params, headers=headers, json=json_data)
        return session

    @staticmethod
    def _get_headers():
        return {
            'authority': 'wwltraffworld.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'states=v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjkyYWJiNTNmODM1YTZmMWM2YzM5YWI5YzliNzU3ZGU2IiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0WU9pLlU5dFRMZE5RQml4ejR4WVhLdThNR1ozdmZxdEM1akRLbTVJRE5COVJwenFuU2NJcXkiLCJ0aW1lc3RhbXAiOjE2OTkyNjk4MzV9.p6WfUzGm0rbf1h3b-Ymx1mr_o6Gs0Ij62Wiit6PMRbs; keitaro=rsoro11u9e93qhvkfgsj251hnj',
            'is-moder': 'true',
            'origin': 'https://wwltraffworld.com',
            'referer': 'https://wwltraffworld.com/admin/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

    def _get_cookies(self):
        return self.session.cookies.get_dict()

    def check_if_exist(self, subid: list[str]):
        session = self._login()
        params = {
            'object': 'reports.build',
        }

        json_data = {
            'range': {
                'interval': 'all_time',
                'timezone': 'Europe/Kyiv',
            },
            'columns': [],
            'metrics': [
                'clicks',
                'campaign_unique_clicks',
                'revenue',
                'profit',
                'sale_revenue',
            ],
            'grouping': [
                'campaign',
                'day',
                'sub_id',
                'campaign_id',
                'offer',
                'affiliate_network',
                'ts',
                'datetime',
            ],
            'filters': [
                {
                    'name': 'campaign_group_id',
                    'operator': 'IN_LIST',
                    'expression': [
                        12,
                        6,
                        7,
                        4,
                        16,
                        5,
                        65,
                        9,
                        63,
                        64,
                        62,
                        161,
                        175,
                        176,
                        155,
                        77,
                        78,
                        79,
                        80,
                        81,
                        82,
                        83,
                        86,
                        87,
                        85,
                        84,
                        144,
                    ],
                },
                {
                    'name': 'sub_id',
                    'operator': 'IN_LIST',
                    'expression': subid,
                },
            ],
            'sort': [
                {
                    'name': 'sub_id',
                    'order': 'asc',
                },
            ],
            'summary': True,
            'offset': 0,
        }

        response = session.post('https://wwltraffworld.com/admin/', params=params, cookies=self._get_cookies(), headers=self._get_headers(), json=json_data)
        return response.json()['rows']

    def get_delete_list(self, list_of_subid):
        subid_data = self.check_if_exist(list_of_subid)
        delete_subid = []
        for subid in subid_data:
            if '23:59' in subid.get('datetime'):
                delete_subid.append(subid.get('sub_id'))
        
        return delete_subid


class TraffManagerChecker:
    def __init__(self) -> None:
        self.session = self._login()

    @staticmethod
    def _login():
        session = requests.Session()
        headers = {
            'authority': 'traff-manager.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://traff-manager.com',
            'pragma': 'no-cache',
            'referer': 'https://traff-manager.com/admin/?return=',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        }

        params = {
            'object': 'auth.login',
        }

        json_data = {
            'login': os.environ.get('KEITARO_LOGIN'),
            'password': os.environ.get('KEITARO_PASSWORD'),
        }

        session.post('https://traff-manager.com/admin/', params=params, headers=headers, json=json_data)
        return session

    def check_if_exist(self, subid: list[str]) -> list[str]:
        session = self.session

        cookies = {
            'states': 'v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjkyYWJiNTNmODM1YTZmMWM2YzM5YWI5YzliNzU3ZGU2IiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0RXBrand0WklkQW5HbmFvRXZwRHdqLlFvJTJGR0ptS3lhY20wNUxlYTRrcXdpUVVHcmdHUTk4bSIsInRpbWVzdGFtcCI6MTY5OTI2MzU3MX0.259o3FVLewfnPr2vFhm4ywCGmqU4yzyf7x5pxE6fDgA',
            'keitaro': 'su9ds6glabmtkq8anehrcfvfdg',
        }

        headers = {
            'authority': 'traff-manager.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'states=v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjkyYWJiNTNmODM1YTZmMWM2YzM5YWI5YzliNzU3ZGU2IiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0RXBrand0WklkQW5HbmFvRXZwRHdqLlFvJTJGR0ptS3lhY20wNUxlYTRrcXdpUVVHcmdHUTk4bSIsInRpbWVzdGFtcCI6MTY5OTI2MzU3MX0.259o3FVLewfnPr2vFhm4ywCGmqU4yzyf7x5pxE6fDgA; keitaro=su9ds6glabmtkq8anehrcfvfdg',
            'is-moder': 'true',
            'origin': 'https://traff-manager.com',
            'referer': 'https://traff-manager.com/admin/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        params = {
            'object': 'reports.build',
        }

        json_data = {
            'range': {
                'interval': 'all_time',
                'timezone': 'Europe/Kyiv',
            },
            'columns': [],
            'metrics': [
                'clicks',
                'campaign_unique_clicks',
                'sale_revenue',
                'revenue',
                'profit_confirmed',
            ],
            'grouping': [
                'campaign',
                'day',
                'sub_id',
                'campaign_id',
                'ts',
                'datetime',
            ],
            'filters': [
                {
                    'name': 'campaign_group_id',
                    'operator': 'IN_LIST',
                    'expression': [
                        67,
                        38,
                        43,
                        48,
                        2,
                        11,
                        12,
                        1,
                        17,
                        19,
                        56,
                    ],
                },
                {
                    'name': 'sub_id',
                    'operator': 'IN_LIST',
                    'expression': subid,
                },
            ],
            'sort': [
                {
                    'name': 'sub_id',
                    'order': 'asc',
                },
            ],
            'summary': True,
            'offset': 0,
        }

        response = session.post('https://traff-manager.com/admin/', params=params, cookies=cookies, headers=headers, json=json_data)
        return response.json()['rows']
    
    def get_delete_list(self, list_of_subid):
        subid_data = self.check_if_exist(list_of_subid)
        delete_subid = []
        for subid in subid_data:
            if '23:59' in subid.get('datetime'):
                delete_subid.append(subid.get('sub_id'))
        
        return delete_subid
    

class ThirdKtChecker:
    def __init__(self) -> None:
        self.session = self._login()

    @staticmethod
    def _login():
        with requests.Session() as session:
            headers = {
                'authority': 'thirdtrykt.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
                'content-type': 'application/json;charset=UTF-8',
                # 'cookie': 'keitaro=kek1bueuhpnmrgj5afsuoihsds',
                'is-moder': 'true',
                'origin': 'https://thirdtrykt.com',
                'referer': 'https://thirdtrykt.com/admin/?return=',
                'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            }

            params = {
                'object': 'auth.login',
            }

            json_data = {
                'login': os.environ.get('THIRD_KEITARO_LOGIN'),
                'password': os.environ.get('THIRD_KEITARO_PASSWORD'),
            }

            response = session.post('https://thirdtrykt.com/admin/', params=params, headers=headers, json=json_data)
            return session
        
    def _get_cookies(self):
        return {
            'states': 'v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjAwNGFhZmY2ZjA4ZDlmMDcxMDNkM2Y0ZTVkMzJmZTcxIiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0d0lXaEphZ3dyT2dHZFFjaDdKbUVvZWpIcUxVV1N3SUFKMTFtMEVTZDU1Y2VoYVJkVTExaDYiLCJ0aW1lc3RhbXAiOjE3MDE2OTUyNzB9.SQB3RFdhLvFnov-3X_E2uG39CNnESMMDxhKUPw1KQak',
            'keitaro': 'kek1bueuhpnmrgj5afsuoihsds',
        }

    def check_if_exist(self, subid: list[str]) -> list[str]:
        session = self.session

        headers = {
            'authority': 'thirdtrykt.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'states=v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjAwNGFhZmY2ZjA4ZDlmMDcxMDNkM2Y0ZTVkMzJmZTcxIiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0NlRtY3dzSzF6ZUJ3ZmFBSWpXWkx1ZVBKSjJkNTBuS3owZDJ3RmhzVTMyNmoycERXTzhwZWUiLCJ0aW1lc3RhbXAiOjE3MDE2ODE0MTV9.KoHuiIMEZYl8eFn7xMhOlmMud_gJcxM1F8sYr-VfCX0; keitaro=kek1bueuhpnmrgj5afsuoihsds',
            'is-moder': 'true',
            'origin': 'https://thirdtrykt.com',
            'referer': 'https://thirdtrykt.com/admin/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        params = {
            'object': 'reports.build',
        }

        json_data = {
            'range': {
                'interval': 'all_time',
                'timezone': 'Europe/Kyiv',
            },
            'columns': [],
            'metrics': [
                'clicks',
                'campaign_unique_clicks',
                'revenue',
                'profit',
                'sale_revenue',
            ],
            'grouping': [
                'sub_id',
                'datetime',
            ],
            'filters': [
                {
                    'name': 'campaign_group_id',
                    'operator': 'IN_LIST',
                    'expression': [
                        142,
                        162,
                        143,
                        144,
                        146,
                        145,
                        148,
                        147,
                        150,
                        149,
                        152,
                        153,
                        155,
                        154,
                        151,
                        156,
                        157,
                        161,
                        163,
                        164,
                        160,
                        159,
                        165,
                        167,
                        168,
                        166,
                        158,
                    ],
                },
                {
                    'name': 'sub_id',
                    'operator': 'IN_LIST',
                    'expression': subid,
                },
            ],
            'sort': [
                {
                    'name': 'sub_id',
                    'order': 'desc',
                },
            ],
            'summary': True,
            'offset': 0,
        }

        response = session.post('https://thirdtrykt.com/admin/', params=params, cookies=self._get_cookies(), headers=headers, json=json_data)
        return response.json()['rows']
    
    def get_delete_list(self, list_of_subid):
        subid_data = self.check_if_exist(list_of_subid)
        delete_subid = []
        for subid in subid_data:
            if '23:59' in subid.get('datetime'):
                delete_subid.append(subid.get('sub_id'))
        
        return delete_subid


if __name__ == "__main__":
    obj = WWLTraffWorldChecker()
    delete_subid= obj.get_delete_list(['b29ct05hu59', 'rvmuoq60li8'])
    
    print(delete_subid)

