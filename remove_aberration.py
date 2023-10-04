import csv

class CSVRow:
    def __init__(self, size, m_rate, max_gen, time, gen) -> None:
        self.size = int(size)
        self.m_rate = float(m_rate)
        self.max_gen = int(max_gen)
        self.time = float(time)
        self.gen = int(gen)

    def __str__(self):
        return f"{self.size},{self.m_rate},{self.max_gen},{self.time},{self.gen}\n"

list = []

with open("stats.csv", newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if len(row) == 5 and float(row[3]) < 120:
            list.append(CSVRow(row[0], row[1], row[2], row[3], row[4]))

with open("without_abberation_stats.csv", "a") as file:
    for i in range(len(list)):
        file.write(str(list[i].size) + "," + str(list[i].m_rate) + "," + str(list[i].max_gen) + "," + str(list[i].time) + "," + str(list[i].gen) + '\n')