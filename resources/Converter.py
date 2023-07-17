import csv
import json

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r',  encoding="UTF-8") as f:
        data = json.load(f)

    with open(csv_file, 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['key', 'en', 'ru', 'comment'])

        en = data["en"]

        for key, values in en.items():
            writer.writerow([key,values, data['ru'][key], ''])

def csv_to_json(csv_filePath, json_filePath):
    data = {"en": {}, "ru": {}}

    with open(csv_filePath, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';')

        header = next(reader)

        for row in reader:
            key = row[0]
            en = row[1]
            ru = row[2]

            data["en"][key] = en
            data["ru"][key] = ru

    with open(json_filePath, 'w', encoding='UTF-8') as f:
        json.dump(data, f)

if __name__ == '__main__':
    #json_to_csv("translations.json", "translations.csv")
    csv_to_json("translator.csv", "translations.json")