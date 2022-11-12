import csv, getopt
from sys import argv


def new_racer():
	c = input('continue? (y/n): ')
	if c == 'y':
		return True
	elif c == 'n':
		return False
	else:
		print(f'{c} is not a not valid input')
		new_racer()


def main(file, mode: str):
	form = """
	format:

	bib:            integer
	name:           string
	nsa:            NOR, FIN, etc
	time:           hh:mm:ss.xx
	fislist-points: xx.xx
	"""

	prefix = ['bib','name','nsa','time','fislist-points']
	run = True

	with open(file, mode, encoding='utf-8') as f:
		w = csv.writer(f, delimiter='\t')
		if mode == 'w+':
			w.writerow(prefix)
		while(run):
			print(form)
			# racer = [input(f'{pre}: ') for pre in prefix]
			racer = input('bib, name, nsa, time, fislist-points: ').split(',')
			w.writerow(racer)
			run = new_racer()


if __name__ == '__main__':



	try:
		file = argv[1]
	except IndexError:
		print('\033[91mIncorrect usage. Use the program as follows:\033[0m')
		print('python3 create_race.py <file.csv>')
	finally:
		arglst = [argv[2]]

		options = 'haw'
		long_options = ['help', 'append', 'write_over']

		try:
			args, vals = getopt.getopt(arglst, options, long_options)

			helpmsg = """Options:
			'-a' or '--append' to append racer to file
			'-w' or '--write_over' to write over entire file """

			for currArg, _ in args:
				if currArg in ('-h', '--help'):
					print(helpmsg)

				elif currArg in ('-a', '--append'):
					main(file, mode='a+')
					print(f'\033[92mResults successfully written to "{file}"\033[0m')

				elif currArg in ('-w', '--write_over'):
					main(file, mode='w+')
					print(f'\033[92mResults successfully written to "{file}"\033[0m')

		except getopt.error as err:
			print(err)
