from csv import reader, writer
from contextlib import contextmanager
from datetime import timedelta
from sys import argv
from os import path


class Race:
	""" Race object. Defined by race factor and race minimum penalty
	
	Attributes:
		res_path	: string of absolute path to result folder
		infile		: string repr filename of where to read data
		outfile		: string repr filename of where to write data
		mp			: integer for minimum penalty (see README)
		F			: integer for race factor (see README)
	"""
	def __init__(self, infile: str, outfile: str, factor: int, min_penalty: int) -> None:
		

		self.res_path = 'results'

		self.infile = infile
		self.outfile = outfile
		self.mp = min_penalty
		self.F = factor

		with self.open_w_error(self.infile) as (f, err):
			if err:
				print(f'IOError: {err}')
				print(f'\033[091mFile: "{self.infile}" not found\033[0m')
				exit(-1)
			else:
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


		self.racedata_nohead = self.racedata[1:].copy()
		self.racedata_nohead.sort(key=lambda x: x[3])

		for idx, row in enumerate(self.racedata_nohead):
			row.insert(0, idx+1)
		self.racedata[0].insert(0,'rnk')

		# Sorted list of dictionaries. Sorted based on finish time.
		# Every dictionary represents its own racer
		self.raced = [{self.racedata[0][idx]:ath[idx] for idx in range(len(self.racedata_nohead[0]))} for ath in self.racedata_nohead]

	def calculate(self):
		# Run all functions to edit the race-list
		self.add_diff()
		self.calc_fis_points(self.penalty())
		self.write_output(self.outfile)



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
		""" Calculates and adds fis-points to every athlete. Takes race penalty and returns none
		   See README->penalty for more information """

		for ath in self.raced:
			fisp = (self.F*ath['time'])/self.raced[0]['time'] - self.F
			ath.pop('fislist-points')
			ath['fis-points'] = round(fisp + penalty, 2)

	@contextmanager
	def open_w_error(self, filename: str, mode="r", encoding="utf-8"):
		""" Context manager for opening file and catch err.

		Joins path to result dir and open file. Will yield 
		either file or error as tuple.

		Args:
			filename: A string repr filename
			mode	: Mode for opening file (r, w, rb, etc.)
			encoding: Read/write encoding.
		Yields:
			A tuple (fp, err). If an exception is catched, 
			fp will be None and vice versa.
		"""
		
		filename_path = path.join(self.res_path, filename)

		try:
			f = open(file=filename_path, mode=mode, encoding=encoding)
		except IOError as err:
			yield None, err
		else:
			try:
				yield f, None
			finally:
				f.close()

	def write_output(self, outfile: str) -> bool:
		""" Writes results to output file. Takes outfile-path and returns none

		Args:
			outfile	: A string repr filename
		Raises:
			IOError: An error occured accessing the file
		"""
		for ath in self.raced:
			ath['time'] = str(timedelta(seconds=ath['time']))

		with self.open_w_error(outfile, 'w+', encoding="utf-8") as (f, err):
			if err:
				print(f'IOerror: {err}')
			else:
				w = writer(f, delimiter='\t')
				w.writerow(self.raced[0].keys())
				for ath in self.raced:
					w.writerow(ath.values())
				print(f'\033[92mResults successfully written to "{self.outfile}"\033[0m')


if __name__ == '__main__':
	# Defines race values and in file
	# See README->factor and ->Minimum penalty for explanation
	try:
		infile = argv[1]
		outfile = argv[2]
	except IndexError:
		print('\033[91mIncorrect usage. Use the program as follows:\033[0m')
		print('python3 fispoints.py <infile.csv> <outfile.csv>')
	finally:
		r = Race(infile, outfile, factor=800, min_penalty=20)
		print(f'\033[92mResults successfully written to "{argv[2]}"\033[0m')