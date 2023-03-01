from csv import reader, writer
from datetime import timedelta
from sys import argv


class Race:
    def __init__(self, infile: str, outfile: str, factor: int, min_penalty: int) -> None:
        """Race object. Defined by race factor and race minimum penalty"""
        print(f'infile: {infile}')
        print(f'outfile: {outfile}')
        print(f'factor: {factor}')
        print(f'penalty: {min_penalty}')
        self.mp = min_penalty
        self.F = factor
        try:
            with open(infile, 'r', encoding='utf-8') as f:
                data = reader(f, delimiter=',')
                self.racedata = list(data)

            # Strip whitespace and remove empty lines
            for line in self.racedata:
                if line:
                    for i in range(len(line)):
                        line[i] = line[i].strip()
                else:
                    self.racedata.remove(line)

            # convert time and fis points to float
            for line in self.racedata[1:]:
                line[3] = line[3].split(':')
                line[3] = int(line[3][0])*60*60 + int(line[3][1])*60 + float(line[3][2])
                line[4] = float(line[4])
        except FileNotFoundError:
            print(f'\033[091mFile: "{infile}" not found\033[0m')
            exit(-1)

        self.racedata_nohead = self.racedata[1:].copy()
        self.racedata_nohead.sort(key=lambda x: x[3])

        for idx, row in enumerate(self.racedata_nohead):
            row.insert(0, idx+1)
        self.racedata[0].insert(0,'rnk')

        # Sorted list of dictionaries. Sorted based on finish time.
        # Every dictionary represents its own racer
        self.raced = [{self.racedata[0][idx]:ath[idx] for idx in range(len(self.racedata_nohead[0]))} for ath in self.racedata_nohead]


        # Run all functions to edit the race-list
        self.add_diff()
        self.calc_fis_points(self.penalty())
        self.write_output(outfile)


    def penalty(self) -> int:
        """Calculates and returns race penalty. See README->penalty for more information"""
        koeff = 3.75

        # top five from race results
        top5 = []
        for ath in self.raced[:5]:
            top5.append(ath['fislist-points'])
        top5.sort()

        # the three with the best fis-list points among the top 5 finishers
        top3 = top5[:3]
        penalty = sum(top3)/koeff

        if penalty > self.mp:
            return penalty
        else:
            return self.mp


    def add_diff(self) -> None:
        """Adds difference in time from winner to every athlete. Returns none"""
        for ath in self.raced:
            diff = round(ath['time'] - self.raced[0]['time'])
            fislist_p = ath['fislist-points']
            ath.pop('fislist-points')
            ath['diff'] = str(timedelta(seconds=diff))
            ath['fislist-points'] = fislist_p


    def calc_fis_points(self, penalty: int) -> None:
        """Calculates and adds fis-points to every athlete. Takes race penalty and returns none
           See README->penalty for more information"""
        for ath in self.raced:
            fisp = (self.F*ath['time'])/self.raced[0]['time'] - self.F
            ath.pop('fislist-points')
            ath['fis-points'] = round(fisp + penalty, 2)


    def write_output(self, outfile: str) -> None:
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
    # See README->factor and ->Minimum penalty for explanation
    print(argv[1])
    try:
        infile = argv[1]
        outfile = argv[2]
    except IndexError:
        print('\033[91mIncorrect usage. Use the program as follows:\033[0m')
        print('python3 fispoints.py <infile.csv> <outfile.csv>')
    finally:
        r = Race(infile, outfile, factor=800, min_penalty=20)
        print(f'\033[92mResults successfully written to "{argv[2]}"\033[0m')