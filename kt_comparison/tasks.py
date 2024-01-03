from datetime import datetime, timedelta
import sys

from celery import shared_task

sys.path.append('C:\Maki\WWL\\financial-daily-report')

from kt_comparison.services.traff_manager import TraffManager
from kt_comparison.services.traff_world import WWLTraffWorld
from kt_comparison.services.third_kt import ThirdKt


@shared_task
def run_script():
    today = datetime.now()

    # # Визначаємо перший день попереднього місяця
    # if today.month == 1:
    #     date_from = today.replace(year=today.year - 1, month=12, day=1)
    #     date_to = date_from + timedelta(days=30)
    # else:
    #     date_from = today.replace(month=today.month - 1, day=1)
    #     date_to = date_from.replace(month=date_from.month + 1, day=1) - timedelta(days=1)

    # # Форматування дат
    # date_from_formatted = date_from.strftime('%Y-%m-%d')
    date_to_formatted = today.strftime('%Y-%m-%d')
    
    tm = TraffManager('2022-05-01', date_to_formatted)
    tm.download_file()

    tw = WWLTraffWorld('2023-01-01', date_to_formatted)
    tw.download_file()

    kt_3 = ThirdKt('2023-11-01', date_to_formatted)
    kt_3.download_file()