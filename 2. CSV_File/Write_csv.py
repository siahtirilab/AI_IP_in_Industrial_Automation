import csv

rows = [
    ['name', 'age', 'city'],
    ['Ali', '25', 'Tehran'],
    ['Sara', '30', 'Shiraz']
]

with open('sampel.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)