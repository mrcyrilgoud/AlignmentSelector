from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os

#tkinter root window
root = tkinter.Tk()
root.title("Alignment Selector")
root.geometry('500x300')

Label(root, text="Enter the beginning column", font=('Calibri 10')).pack()
firstCol = Entry(root, width= 12)
firstCol.place(x=200,y=100)

Label(root, text="Enter the ending column", font=('Calibri 10')).pack()
lastCol = Entry(root, width= 12)
lastCol.place(x=200, y=150)

Label(root, text="Enter the name of the trimmed alignment file", font=('Calibri 10')).pack()
outputName = Entry(root, width= 60)
outputName.place(x=200, y=175)

def submissionAl():
    beginCol = int(firstCol.get())
    endCol = int(lastCol.get());

    if (beginCol >= endCol):
        tkinter.messagebox.showerror("Error", "Improper numerical inputs")
        return

    filePath = filedialog.askopenfilename()

    if filePath.lower().endswith(('.fasta', '.fa', '.txt')):
        tkinter.messagebox.showinfo("File accepted", "Conducting trimming")
    else:
        tkinter.messagebox.showerror("File error", "Improper file type")
        return

    with open(filePath, 'r') as reader:
        linesFile = []
        seqLine = ""

        for lineRed in reader:
            if (lineRed.count(">") != 0):
                linesFile.append(seqLine)
                linesFile.append(lineRed)
                seqLine = ""
            else:
                seqLine += lineRed
                
    tkinter.messagebox.showinfo("Choose directory", "Choose directory to place output file in")
    folderDir = filedialog.askdirectory()
    os.chdir(folderDir)

    nFname = outputName.get() + ".txt"
    newFile = open(nFname, "x")
    for evLine in linesFile:
        if (evLine.count(">") != 0):
            newFile.write(evLine)
        else:
            lineTr = evLine[beginCol:endCol]
            newFile.write(lineTr)

    newFile.close()
    tkinter.messagebox.showinfo("Complete","File " + nFname + " has been created.")

submitButton = Button(root, text="Begin Trimming", command=submissionAl, pady=10)
submitButton.place(x=200, y=200)

root.mainloop()