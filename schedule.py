import csv


def import_csv(csv):
  data = []
  with open(csv) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      data.append(row)
      
      
if __name__ == "__main__":
  import_csv('171schedule.csv')