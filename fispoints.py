from csv import reader, writer
from datetime import timedelta
from sys import argv


class Race:
    def __init__(self, infile, outfile, Factor, min_penalty):
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

        for idx, row in enumerate(self.racedata_nohead):
            row.insert(0, idx+1)
        self.racedata[0].insert(0,'rnk')

        self.raced = [{self.racedata[0][idx]:ath[idx] for idx in range(len(self.racedata_nohead[0]))} for ath in self.racedata_nohead]

        #Run all functions to edit the race-list
        self.add_diff()
        self.calc_fis_points(self.penalty())
        self.write_output(outfile)


    def penalty(self):
        """Calculates and returns race penalty. See README->penalty for more information"""
        s = 0
        koeff = 3.75
        for ath in self.raced[:5]:
            s += ath['fislist-points']
        penalty = s/koeff

        if penalty > self.mp:
            return penalty
        else:
            return self.mp


    def add_diff(self):
        """Adds difference in time from winner to every athlete. Returns none"""
        for ath in self.raced:
            diff = round(ath['time'] - self.raced[0]['time'])
            fislist_p = ath['fislist-points']
            ath.pop('fislist-points')
            ath['diff'] = str(timedelta(seconds=diff))
            ath['fislist-points'] = fislist_p


    def calc_fis_points(self, penalty):
        """Calculates and adds fis-points to every athlete. Takes race penalty and returns none
           See README->penalty for more information"""
        for ath in self.raced:
            fisp = (self.F*ath['time'])/self.raced[0]['time'] - self.F
            ath.pop('fislist-points')
            ath['fis-points'] = round(fisp + penalty, 2)


    def write_output(self, outfile):
        """Writes results to output file. Takes outfile-path and returns none"""
        for ath in self.raced:
            ath['time'] = str(timedelta(seconds=ath['time']))

        with open(outfile, 'w+', encoding='utf-8') as f:
            w = writer(f, delimiter='\t')
            w.writerow(self.raced[0].keys())
            for ath in self.raced:
                w.writerow(ath.values())


if __name__ == '__main__':
    # Defines race values and in file
    # See README->Factor and ->Minimum penalty for explanation
    r1 = Race(argv[1], argv[2], Factor=800, min_penalty=20)
    
    for d in r.raced:
        print()
    for key, val in d.items():
        print(f'{key} : {val}')