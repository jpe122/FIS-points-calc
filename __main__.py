import tkinter as tk

from glob import glob

from .create_race import CreateRace
from .fispoints import Race



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
        self.infile = None
        self.outfile = None
        self.factor = None
        self.penalty = None

        # Transfer control to main function
        self.main()


    def main(self) -> None:
        self.set_outfile()
        self.set_factor()
        self.set_penalty()

        # self.calculate()
        self.root.mainloop()

    def choose_infile_method(self) -> None:
        tk.Label(self.root, text='Select method for input file')
        create_btn = tk.Button(self.root, text='Create race', command=self.create_infile).pack()
        choose_btn = tk.Button(self.root, text='Choose race', command=self.existing_infile).pack()

    def create_infile(self):
        c = CreateRace()
        c.create(self.outfile, mode='w+')

    def existing_infile(self):

        # List csv files in current directory
        csv_files = glob('*.csv')

        # Listbox object will display csv files
        listbox = tk.Listbox(self.root, width=100)
        listbox.pack()

        for file in csv_files:
            listbox.insert(tk.END, file)

        listbox.bind("<<ListboxSelect>>", on_select)

        def on_select(self, event):
            selected = event.widget.curselection()
            if selected:
                index = selected[0]
                self.infile = event.widget.get(index)


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

    def set_factor(self) -> None:
        def store():
            self.factor = entry.get()
            label.forget()
            entry.forget()
            btn.forget()

        label = tk.Label(self.root, text='Provide race factor. See README for more info')
        label.pack()

        entry = tk.Entry(self.root)
        entry.pack()

        btn = tk.Button(self.root, text='Store entry', command=store)
        btn.pack()

    def set_penalty(self) -> None:
        def store():
            self.penalty = entry.get()
            label.forget()
            entry.forget()
            btn.forget()

        label = tk.Label(self.root, text='Provide race penalty. See README for more info')
        label.pack()

        entry = tk.Entry(self.root)
        entry.pack()

        btn = tk.Button(self.root, text='Store entry', command=store)
        btn.pack()

    def calculate(self):
        print("values for race obj:")
        print(f'infile: {self.infile}')
        print(f'outfile: {self.outfile}')
        print(f'factor: {self.factor}')
        print(f'penalty: {self.penalty}')
        # r = Race(str(self.infile), str(self.outfile), int(self.factor), int(self.penalty))

app = App()