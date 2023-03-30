import tkinter as tk

from glob import glob
from os import listdir

from create_race import CreateRace
from fispoints import Race



class App:
	""" Tkniter application for creating race file and calculating FIS race points 

		Attributes:
			root    - Tkinter master
			outfile - Tkinter StringVar object holding output file name
			infile  - Tkinter StringVar object holding input file name
			factor  - Tkinter StringVar object holding race factor value
			penalty  - Tkinter StringVar object holding race minimum penalty
	"""
	def __init__(self) -> None:
		""" Initializes tkinter window and declaring attributes """

		# Tkinter initialization
		self.root = tk.Tk()
		self.root.geometry('400x400')

		# Define values for race initialization
		self.infile = str
		self.outfile = str
		self.factor = str
		self.penalty = str

		# Transfer control to main function
		self.main()


	def main(self) -> None:
		self.set_outfile()
		self.set_factor()
		self.set_penalty()

		self.choose_infile_method()

		btn = tk.Button(self.root, text='Calculate', command=self.calculate)
		btn.pack()

		self.root.mainloop()

	def choose_infile_method(self) -> None:
		tk.Label(self.root, text='Select method for input file')
		self.create_btn = tk.Button(self.root, text='Create race', command=self.create_infile)
		self.create_btn.pack()
		self.choose_btn = tk.Button(self.root, text='Choose race', command=self.existing_infile)
		self.choose_btn.pack()

	def create_infile(self):
		c = CreateRace()
		c.create(self.outfile, mode='w+')

	def existing_infile(self):

		# List csv files in current directory
		csv_files = glob('results/*.csv')
		# csv_files = listdir('results/')

		# Listbox object will display csv files
		listbox = tk.Listbox(self.root, width=100)
		listbox.pack()

		for file in csv_files:
			listbox.insert(tk.END, file)

		def onselect(event):
			# Note here that Tkinter passes an event object to onselect()
			w = event.widget
			index = int(w.curselection()[0])
			value = w.get(index)
			self.infile = str(value)
			# print(f'Selected item {index}: "{value}"')
			listbox.forget()

		listbox.bind("<<ListboxSelect>>", onselect)
		self.create_btn.forget()
		self.choose_btn.forget()

	def set_outfile(self) -> None:
		def store():
			self.outfile = entry.get()
			label.forget()
			entry.forget()
			btn.forget()

		label = tk.Label(self.root, text='Provide output file name <filename.csv>')
		label.pack()

		entry = tk.Entry(self.root)
		entry.pack()

		btn = tk.Button(self.root, text='Store entry', command=store)
		btn.pack()
		return

	def set_factor(self) -> None:
		def store():
			self.factor = int(entry.get())
			label.forget()
			entry.forget()
			btn.forget()

		label = tk.Label(self.root, text='Provide race factor. See README for more info')
		label.pack()

		entry = tk.Entry(self.root)
		entry.pack()

		btn = tk.Button(self.root, text='Store entry', command=store)
		btn.pack()
		return

	def set_penalty(self) -> None:
		def store():
			self.penalty = int(entry.get())
			label.forget()
			entry.forget()
			btn.forget()

		label = tk.Label(self.root, text='Provide race penalty. See README for more info')
		label.pack()

		entry = tk.Entry(self.root)
		entry.pack()

		btn = tk.Button(self.root, text='Store entry', command=store)
		btn.pack()
		return self.penalty

	def calculate(self):
		print("Values for race:")
		print(f'infile: {self.infile}')
		print(f'outfile: {self.outfile}')
		print(f'factor: {self.factor}')
		print(f'penalty: {self.penalty}')

		try:
			assert(self.infile.endswith('.csv'))
		except AssertionError:
			self.root.quit()

		r = Race(str(self.infile), str(self.outfile), int(self.factor), int(self.penalty))
		r.calculate()


app = App()