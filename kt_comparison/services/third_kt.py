import requests
import os
import sys

from json import JSONDecodeError
from datetime import datetime
sys.path.append('C:\Maki\WWL\\report_by_subid')
from kt_comparison.utils import get_date_list, get_week_list


class ThirdKt:
    def __init__(self, date_from, date_to) -> None:
        self.date_from = date_from
        self.date_to = date_to
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

            response = requests.post('https://thirdtrykt.com/admin/', params=params, headers=headers, json=json_data)
            return session
        
    def _get_cookies(self):
        return {
            'states': 'v1eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6IjAwNGFhZmY2ZjA4ZDlmMDcxMDNkM2Y0ZTVkMzJmZTcxIiwicGFzc3dvcmQiOiIlMjQyeSUyNDEwJTI0d0lXaEphZ3dyT2dHZFFjaDdKbUVvZWpIcUxVV1N3SUFKMTFtMEVTZDU1Y2VoYVJkVTExaDYiLCJ0aW1lc3RhbXAiOjE3MDE2OTUyNzB9.SQB3RFdhLvFnov-3X_E2uG39CNnESMMDxhKUPw1KQak',
            'keitaro': 'kek1bueuhpnmrgj5afsuoihsds',
        }

    def get_data(self, date_from, date_to):
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
                'interval': 'custom_date_range',
                'timezone': 'Europe/Kyiv',
                'from': f'{date_from} 00:00',
                'to': f'{date_to} 23:59',
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
                'day',
                'campaign',
                'sub_id',
                'campaign_id',
                'offer',
                'affiliate_network',
                'ts',
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
            ],
            'sort': [
                {
                    'name': 'sub_id',
                    'order': 'desc',
                },
            ],
            'summary': True,
            'offset': 0,
            'format': 'csv',
        }

        response = session.post('https://thirdtrykt.com/admin/', cookies=self._get_cookies(), params=params, headers=headers, json=json_data)
        return response.json()

    def download_file(self):
        session = self.session
        
        date_range = get_date_list(self.date_from, self.date_to)
        print(date_range)
        for month in date_range:
            try:
                response = self.get_data(month[0], month[1])
                
                cookies = {
                    'keitaro': 'kek1bueuhpnmrgj5afsuoihsds',
                }

                headers = {
                    'authority': 'thirdtrykt.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
                    # 'cookie': 'keitaro=kek1bueuhpnmrgj5afsuoihsds',
                    'is-moder': 'true',
                    'referer': 'https://thirdtrykt.com/admin/',
                    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'iframe',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                }
                file_name = response['url'].split('/')[2]

                response = session.get(
                    f'https://thirdtrykt.com/exports/{file_name}',
                    cookies=cookies,
                    headers=headers,
                )

                if response.status_code == 200:
                    date = datetime.strptime(month[0], '%Y-%m-%d')
                    today = datetime.today()
                    today_str = datetime.strftime(today, '%Y-%m-%d')
                    
                    if not os.path.exists(f'./kt_3/{today_str}'):
                        os.mkdir(f'./kt_3/{today_str}')
                    
                    file_path = f'./kt_3/{today_str}/{date.month}-{date.year}.csv'

                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Файл був успішно завантажений та збережений як {file_path}")
                else:
                    print(f"Помилка при завантаженні файлу: {response.status_code}")

            except JSONDecodeError:
                print('exception')
                new_date_range = get_week_list(month[0], month[1], 8)

                for week in new_date_range: 
                    response = self.get_data(week[0], week[1])
                    print(response)
                
                    cookies = {
                        'keitaro': 'kek1bueuhpnmrgj5afsuoihsds',
                    }

                    headers = {
                        'authority': 'thirdtrykt.com',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
                        # 'cookie': 'keitaro=kek1bueuhpnmrgj5afsuoihsds',
                        'is-moder': 'true',
                        'referer': 'https://thirdtrykt.com/admin/',
                        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'iframe',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    }
                    file_name = response['url'].split('/')[2]

                    response = session.get(
                        f'https://thirdtrykt.com/exports/{file_name}',
                        cookies=cookies,
                        headers=headers,
                    )

                    if response.status_code == 200:
                        date = datetime.strptime(month[0], '%Y-%m-%d')
                        today = datetime.today()
                        today_str = datetime.strftime(today, '%Y-%m-%d')
                        

                        if not os.path.exists(f'./kt_3/{today_str}'):
                            os.mkdir(f'./kt_3/{today_str}')
                        
                        file_path = f'./kt_3/{today_str}/{date.month}-{date.year}.csv'

                        with open(file_path, 'ab') as file:
                            file.write(response.content)
                        print(f"Файл був успішно завантажений та збережений як {file_path}")

                        new_content = []

                        with open(file_path, 'r', encoding='utf-8') as file:
                            lines = file.readlines()

                        skip_next = False
                        for i in range(len(lines)):
                            if skip_next:
                                skip_next = False
                                continue

                            if lines[i].startswith(';;;0;;;;0;'):
                                skip_next = True
                            else:
                                new_content.append(lines[i])

                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.writelines(new_content)
                    else:
                        print(f"Помилка при завантаженні файлу: {response.status_code}")


if __name__ == "__main__":
    obj = ThirdKt('2023-11-01', '2023-11-30')
    # obj.get_data('2022-12-01', '2022-12-31')
    obj.download_file()