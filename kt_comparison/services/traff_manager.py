import time
import requests
import os
import sys

from json import JSONDecodeError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

sys.path.append('C:\Maki\WWL\\report_by_subid')

from kt_comparison.utils import get_date_list, get_week_list


class TraffManager:
    def __init__(self, date_from, date_to) -> None:
        self.date_from = date_from
        self.date_to = date_to
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

    def get_data(self, date_from, date_to):
        session = self.session
        print(date_from, date_to)

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
                'sale_revenue',
                'revenue',
                'profit_confirmed',
            ],
            'grouping': [
                'campaign',
                'day',
                'sub_id',
                'campaign_id',
                'offer',
                # 'affiliate_network',
                'ts',
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
            ],
            'sort': [
                {
                    'name': 'sub_id',
                    'order': 'asc',
                },
            ],
            'summary': True,
            'offset': 0,
            'format': 'csv',
        }

        if date_from == '2022-12-01':
            json_data['grouping'] = [
                'campaign',
                'day',
                'sub_id',
                'campaign_id',
                'offer',
                'ts',
            ]
        cookies = session.cookies.get_dict()
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

        time.sleep(5)
        print(params, json_data, headers)
        response = session.post('https://traff-manager.com/admin/', params=params, cookies=cookies, headers=headers, json=json_data)
        data = response.json()
        return data


    def download_file(self):
        session = self.session
        
        date_range = get_date_list(self.date_from, self.date_to)
        print(date_range)
        for month in date_range:
            try:
                response = self.get_data(month[0], month[1])
                
                cookies = session.cookies.get_dict()

                headers = {
                    'authority': 'traff-manager.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
                    # 'cookie': 'keitaro=su9ds6glabmtkq8anehrcfvfdg',
                    'is-moder': 'true',
                    'referer': 'https://traff-manager.com/admin/',
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
                    f'https://traff-manager.com/exports/{file_name}',
                    cookies=cookies,
                    headers=headers,
                )

                if response.status_code == 200:
                    date = datetime.strptime(month[0], '%Y-%m-%d')
                    today = datetime.today()
                    today_str = datetime.strftime(today, '%Y-%m-%d')
                    
                    if not os.path.exists(f'./kt_1/{today_str}'):
                        os.mkdir(f'./kt_1/{today_str}')
                    
                    file_path = f'./kt_1/{today_str}/{date.month}-{date.year}.csv'

                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Файл був успішно завантажений та збережений як {file_path}")
                else:
                    print(f"Помилка при завантаженні файлу: {response.status_code}")

            except JSONDecodeError:
                print('exception')
                new_date_range = get_week_list(month[0], month[1], 15)

                for week in new_date_range: 
                    try:
                        response = self.get_data(week[0], week[1])
                    except JSONDecodeError:
                        response = self.get_data(week[0], week[1])
                    print(response)
                
                    cookies = session.cookies.get_dict()

                    headers = {
                        'authority': 'traff-manager.com',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
                        # 'cookie': 'keitaro=su9ds6glabmtkq8anehrcfvfdg',
                        'is-moder': 'true',
                        'referer': 'https://traff-manager.com/admin/',
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
                        f'https://traff-manager.com/exports/{file_name}',
                        cookies=cookies,
                        headers=headers,
                    )                    

                    if response.status_code == 200:
                        date = datetime.strptime(month[0], '%Y-%m-%d')
                        today = datetime.today()
                        today_str = datetime.strftime(today, '%Y-%m-%d')
                        

                        if not os.path.exists(f'./kt_1/{today_str}'):
                            os.mkdir(f'./kt_1/{today_str}')
                        
                        file_path = f'./kt_1/{today_str}/{date.month}-{date.year}.csv'

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
    obj = TraffManager('2022-12-01', '2022-12-31')
    # obj.get_data('2022-12-01', '2022-12-02')
    obj.download_file()