from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

from resources.reddit import Reddit
import threading



class GUI():

    def __init__(self):

        self.window = Tk()
        self.progress = lambda n: Progressbar(self.window ,orient=HORIZONTAL,length=n,mode='determinate')
        self.scraping = False
        
        self.csvPath = False

    def main(self):
        insert_default_text = lambda varname, key : varname.insert(0, key) 

        GreetingLabel = Label(self.window, text="RIS Reddit Image Scraper", font=("Arial", 15))
        GreetingLabel.grid(row=0, columnspan=2, sticky="W")

        clientIDText = Label(self.window, text="CLIENTID       : ", font=("Arial", 11))
        clientIDText.grid(column=0, row=1, sticky="W")

        clientSeText = Label(self.window, text="CLIENTPSK   : ", font=("Arial", 11))
        clientSeText.grid(column=0, row=2, sticky="W")

        self.clientIDEntry = Entry(self.window, width=60)
        self.clientIDEntry.grid(column=1, row=1, sticky="W", columnspan=3)

        self.clientSeEntry = Entry(self.window, width=60)
        self.clientSeEntry.grid(column=1, row=2, sticky="W", columnspan=3)

        self.numberEntry = Entry(self.window)
        self.numberEntry.grid(column=3, row=3, sticky="news")
        insert_default_text(self.numberEntry, 1000)

        csvButton = Button(self.window, text="Choose CSV File", command=self.__csvFile)
        csvButton.grid(column=0, row=3, sticky="news")

        

        outputButton = Button(self.window, text="outputFolder", command=self.__SelectOutputFolder)
        outputButton.grid(column=1, row=3, sticky="news")

        runButton = Button(self.window, text="RUN", command=self.__startScrape)
        runButton.grid(column=2, row=3, sticky="news")

        self.window.mainloop()

    

    def __SelectOutputFolder(self):
        self.output = filedialog.askdirectory(title="Choose Export Folder WARNING FILE EXPLOSION", initialdir='/')

    def __csvFile(self):
        self.csvPath = filedialog.askopenfilename(title="Choose Subreddit CSV File", initialdir='/', filetypes=(('csv File', '*.csv'), ('All files', '*.*')))

    def __startScrape(self):
        

        self.scraping = True
        self.Reddit = Reddit(self.clientIDEntry.get(), self.clientSeEntry.get())
        self.Reddit.getSubreddit(csvFile=self.csvPath)
        n = self.numberEntry.get()
        self.window.destroy()
        self.Reddit.run(n, self.output)
        

        

    def run(self):
        self.main()

