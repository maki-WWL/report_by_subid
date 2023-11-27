import pandas as pd

# Шлях до вашого CSV файлу
file_path = 'report.csv'

# Зчитування CSV файлу
df = pd.read_csv(file_path, delimiter=';')
print(df)

# Перевірка на дублікати в колонці 'sub_id'
duplicate_sub_ids = df[df['SubId'].duplicated(keep=False)]

# Виведення результату
if not duplicate_sub_ids.empty:
    print("Знайдені дублікати sub_id:")
    print(duplicate_sub_ids)
else:
    print("Дублікатів sub_id не знайдено.")
