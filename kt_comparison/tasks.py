import sys

from celery import shared_task

sys.path.append('C:\Maki\WWL\\financial-daily-report')

from kt_comparison.services.traff_manager import TraffManager
from kt_comparison.services.traff_world import WWLTraffWorld


@shared_task
def run_script():
    tm = TraffManager('2022-05-01', '2023-10-31')
    tm.download_file()

    tw = WWLTraffWorld('2023-01-01', '2023-10-31')
    tw.download_file()