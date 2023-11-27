import pandas as pd

from datetime import datetime, timedelta


def get_date_list(date_from, date_to):
    start = datetime.strptime(date_from, '%Y-%m-%d')
    end = datetime.strptime(date_to, '%Y-%m-%d')

    months = pd.date_range(start, end, freq='MS').tolist()

    res_list = []

    for i in range(len(months)):
        date_from = months[i]
        if i < len(months) - 1:
            date_to = months[i + 1] - pd.Timedelta(days=1)
        else:
            date_to = end
        res_list.append((date_from.strftime('%Y-%m-%d'), date_to.strftime('%Y-%m-%d')))
    
    return res_list


def get_week_list(date_from, date_to, delimiter=4):
    start = datetime.strptime(date_from, '%Y-%m-%d')
    end = datetime.strptime(date_to, '%Y-%m-%d')

    months = pd.date_range(start, end, freq='MS').tolist()

    res_list = []

    for month_start in months:
        month_end = month_start + pd.offsets.MonthEnd(1)
        part_length = (month_end - month_start + timedelta(days=1)) // delimiter

        for i in range(delimiter):
            part_start = month_start + i * part_length
            part_end = month_start + (i + 1) * part_length - timedelta(days=1)
            part_end = min(part_end, month_end)
            res_list.append((part_start.strftime('%Y-%m-%d'), part_end.strftime('%Y-%m-%d')))

    print(res_list)
    return res_list


if __name__ == "__main__":
    print(get_week_list('2023-02-01', '2023-02-28'))
