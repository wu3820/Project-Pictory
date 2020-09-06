import csv

# TODO: Also switch Selected for Not Selected and vice versa, before doing this.
with open('test32.csv') as f:
    with open('new_results.csv') as f1:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(f1, reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row['Label'] == "":
                row['Label'] = "Not Selected"
            writer.writerow(row)