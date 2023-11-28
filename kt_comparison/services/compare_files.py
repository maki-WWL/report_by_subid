import pandas as pd
import os
import numpy as np

from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter


def should_be_deleted(row):
    for item in row:
        if pd.notna(item) and item != 0:
            return False
        elif pd.notna(item) and item == 0:
            return True
    return True


def create_excel(dates_of_files: str, first_date_str: str, second_date_str: str, folder_path: str) -> None:
    base_dir = os.path.join(folder_path)
    excel_writer = pd.ExcelWriter(f'result_{folder_path}.xlsx', engine='openpyxl')

    for date_of_file in dates_of_files:
        file_name = f"{date_of_file.split('-')[0]}-{date_of_file.split('-')[1]}.csv"

        first_file_path = os.path.join(base_dir, first_date_str, file_name)
        second_file_path = os.path.join(base_dir, second_date_str, file_name)

        df1 = pd.read_csv(first_file_path, quotechar='"', sep=';')
        df2 = pd.read_csv(second_file_path, quotechar='"', sep=';')

        df1.set_index('SubId', inplace=True)
        df2.set_index('SubId', inplace=True)

        combined = pd.merge(df1.reset_index(), df2.reset_index(), on='SubId', how='outer', suffixes=('_file1', '_file2'))

        only_in_df1 = combined[combined['Доход_file2'].isna()]
        only_in_df2 = combined[combined['Доход_file1'].isna()]

        combined['Доход_file1'] = pd.to_numeric(combined['Доход_file1'], errors='coerce')
        combined['Доход_file2'] = pd.to_numeric(combined['Доход_file2'], errors='coerce')

        diff = combined[(~combined['Доход_file1'].isna() & ~combined['Доход_file2'].isna()) & (combined['Доход_file1'] != combined['Доход_file2'])]

        diff['Різниця'] = diff['Доход_file2'].fillna(0) - diff['Доход_file1'].fillna(0)

        first_column_name = combined.columns[0]

        empty_row_1 = pd.DataFrame(np.nan, index=[0], columns=combined.columns)
        empty_row_1[first_column_name] = 'Є у першому файлі, немає в другому'
            
        empty_row_2 = pd.DataFrame(np.nan, index=[0], columns=combined.columns)
        empty_row_2[first_column_name] = 'Є у другому файлі, немає в першому'

        result = pd.concat([diff, empty_row_1, only_in_df1, empty_row_2, only_in_df2])

        result.to_csv('result.csv', sep=';', encoding='utf-8', index=False)

        df = pd.read_csv('result.csv', sep=';')

        df = df[~df.apply(should_be_deleted, axis=1)]

        sheet_name = date_of_file

        df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

        os.remove('result.csv')

    excel_writer.close()



def resize_table() -> None:
    wb = load_workbook('result.xlsx')
    ws = wb.active

    # Автоматично налаштовуємо ширину стовпців
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Отримуємо літеру стовпця

        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass

        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    wb.save('result.xlsx')


if __name__ == "__main__":
    create_excel(['5-2023', '6-2023'], '2023-11-21', '2023-11-22')
    # resize_table()