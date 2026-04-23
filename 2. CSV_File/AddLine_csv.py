import csv

new_row = ['Sara', '30']

with open('sampel.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(new_row)