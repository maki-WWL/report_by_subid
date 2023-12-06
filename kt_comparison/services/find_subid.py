from pprint import pprint
import sys

sys.path.append('C:\Maki\WWL\\report_by_subid')

from kt_comparison.services.checkers import TraffManagerChecker, WWLTraffWorldChecker, ThirdKtChecker


def find_subid(subid: str):
    tm = TraffManagerChecker()
    wt = WWLTraffWorldChecker()
    third_keitaro = ThirdKtChecker()

    res_tm = tm.check_if_exist([subid])
    res_wt = wt.check_if_exist([subid])
    res_third_kt = third_keitaro.check_if_exist([subid])

    if len(res_tm) > 0:
        selected_tm = res_tm[0]
        selected_tm['kt'] = 'kt_1'
        return selected_tm
    if len(res_wt) > 0:
        selected_wt = res_wt[0]
        selected_wt['kt'] = 'kt_2'
        return selected_wt
    if len(res_third_kt) > 0:
        selected_third_kt = res_third_kt[0]
        selected_third_kt['kt'] = 'kt_3'
        return selected_third_kt


if __name__ == "__main__":
    print(find_subid('101jf9f4e')) # 102g0ph740iu a6sib85llm0