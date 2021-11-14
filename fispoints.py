from csv import reader, writer
from datetime import timedelta
from sys import argv


#Hello
class Race:
    def __init__(self, infile, Factor, min_penalty):
        """Race object. Defined by race factor and race minimum penalty"""
        self.mp = min_penalty
        self.F = Factor
        with open(infile, 'r', encoding='utf-8') as f:
            data = reader(f, delimiter=',')
            self.racedata = list(data)
            for line in self.racedata[1:]:
                line[3] = line[3].split(':')
                line[3] = int(line[3][0])*60*60 + int(line[3][1])*60 + float(line[3][2])
                line[4] = float(line[4])
        self.racedata_nohead = self.racedata[1:].copy()
        self.racedata_nohead.sort(key=lambda x: x[3])

    def calculate(self, outfile):
        """Takes output file as single argument. Returns none. Writes race data
           with calculated fis-points to output file"""
        
        # Calculates penalty. See README->penalty for explanation
        s = 0
        koeff = 3.75
        for row in self.racedata_nohead[:5]:
            s += row[4]
        penalty = s/koeff

        # Appends ranks to sorted list
        for idx, row in enumerate(self.racedata_nohead):
            row.insert(0, idx+1)

        # Calculates diff time to race winner and appends new column; diff
        for row in self.racedata_nohead:
            diff = round(row[4] - self.racedata_nohead[0][4])
            row.insert(-1,str(timedelta(seconds=diff)))

        # Calculates race-points and adds penalty depending on penalty value
        # See README->minimum penalty for explanation
        for row in self.racedata_nohead:
            fisp = (self.F*row[4])/self.racedata_nohead[0][4] - self.F
            row.pop()
            if penalty > self.mp:
                row.append(round(fisp+penalty, 2))
            else:
                row.append(round(fisp+self.mp, 2))

        # Convers time from seconds to hh:mm:ss.
        for row in self.racedata_nohead:
            row[4] = str(timedelta(seconds=row[4]))

        with open(outfile, 'w+', encoding='utf-8') as f:
            w = writer(f, delimiter='\t')

            # Writes header to the out file
            header = ['rnk','bib','name','nsa','time','diff','fis-points']
            w.writerow(header)

            # Writes every row in race data list without header
            for row in self.racedata_nohead:
                w.writerow(row)

    def __str__(self, idx):
        """Takes index as single argument. Returns indexed racer."""
        return str(self.racedata_nohead[idx])



if __name__ == '__main__':
    # Defines race values and in file
    # See README->Factor and ->Minimum penalty for explanation
    r1 = Race(argv[1], Factor=800, min_penalty=20)
    r1.calculate('results.csv')

    for i in r1.racedata_nohead:
        print(i)