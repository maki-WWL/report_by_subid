import requests

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
        'interval': 'custom_date_range',
        'timezone': 'Europe/Kyiv',
        'from': '2023-01-01 00:00',
        'to': '2023-01-31 23:59',
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
            'order': 'desc',
        },
    ],
    'summary': True,
    'offset': 0,
}

response = requests.post('https://traff-manager.com/admin/', params=params, cookies=cookies, headers=headers, json=json_data)

import csv


# Переконайтеся, що запит виконаний успішно
if response.status_code == 200:
    data = response.json()

    rows = data['rows']

    # Визначення заголовків для CSV на основі ключів першого об'єкта в списку 'rows'
    headers = rows[0].keys() if rows else []

    # Запис у CSV файл
    with open('res.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        if rows:
            writer.writerows(rows)
else:
    print("Помилка при виконанні запиту:", response.status_code)

