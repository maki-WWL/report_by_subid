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


class WWLTraffWorld:
    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to
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

    def get_data(self, date_from: str, date_to: str):
        session = self._login()
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
                'revenue',
            ],
            'grouping': [
                'sub_id',
                'day',
                'campaign',
                'offer',
                'affiliate_network',
            ],
            'filters': [
                {
                    'name': 'revenue',
                    'operator': 'NOT_EQUAL',
                    'expression': '0',
                },
                {
                    'name': 'sub_id_30',
                    'operator': 'NOT_EQUAL',
                    'expression': 'TRAFFICBACK',
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

        response = session.post('https://wwltraffworld.com/admin/', params=params, cookies=self._get_cookies(), headers=self._get_headers(), json=json_data)
        return response.json()

    def download_file(self):
        session = self._login()
        date_range = get_date_list(self.date_from, self.date_to)
        for month in date_range:
            try:
                response = self.get_data(month[0], month[1])
                cookies = self._get_cookies()
                headers = {
                    'authority': 'wwltraffworld.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
                    # 'cookie': 'keitaro=rsoro11u9e93qhvkfgsj251hnj',
                    'is-moder': 'true',
                    'referer': 'https://wwltraffworld.com/admin/',
                    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'iframe',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                }
                file_name = response['url'].split('/')[2]
                response = session.get(f'https://wwltraffworld.com/exports/{file_name}', cookies=cookies, headers=headers)

                if response.status_code == 200:
                    date = datetime.strptime(month[0], '%Y-%m-%d')
                    today = datetime.today()
                    today_str = datetime.strftime(today, '%Y-%m-%d')
                    
                    if not os.path.exists(f'./kt_2/{today_str}'):
                        os.mkdir(f'./kt_2/{today_str}')
                    
                    file_path = f'./kt_2/{today_str}/{date.month}-{date.year}.csv'

                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Файл був успішно завантажений та збережений як {file_path}")
                else:
                    print(f"Помилка при завантаженні файлу: {response.status_code}")
            except JSONDecodeError:
                print('exception')
                new_date_range = get_week_list(month[0], month[1], delimiter=10)

                for week in new_date_range: 
                    response = self.get_data(week[0], week[1])
                    print(response)
                    cookies = self._get_cookies()
                    headers = {
                        'authority': 'wwltraffworld.com',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'ru,ru-RU;q=0.9,en;q=0.8',
                        # 'cookie': 'keitaro=rsoro11u9e93qhvkfgsj251hnj',
                        'is-moder': 'true',
                        'referer': 'https://wwltraffworld.com/admin/',
                        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'iframe',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    }
                    file_name = response['url'].split('/')[2]
                    response = session.get(f'https://wwltraffworld.com/exports/{file_name}', cookies=cookies, headers=headers)

                    if response.status_code == 200:
                        date = datetime.strptime(month[0], '%Y-%m-%d')
                        today = datetime.today()
                        today_str = datetime.strftime(today, '%Y-%m-%d')
                        
                        if not os.path.exists(f'./kt_2/{today_str}'):
                            os.mkdir(f'./kt_2/{today_str}')
                        
                        file_path = f'./kt_2/{today_str}/{date.month}-{date.year}.csv'

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
    obj = WWLTraffWorld('2023-06-01', '2023-06-30')
    obj.download_file()
