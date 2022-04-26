#Importing Tkinter - Python GUI library

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os

#the Tkinter root window
#First window that the user will see
root = tkinter.Tk()

#Specifies basic aspects of the main window
root.title("Alignment Selector")
root.geometry('500x300')

#Label and text entry for the beginning column
Label(root, text="Enter the beginning column", font=('Calibri 10')).place(x=150,y=0)
firstCol = Entry(root, width= 12)
firstCol.place(x=150,y=25)

#Label and text entry for the ending column
Label(root, text="Enter the ending column", font=('Calibri 10')).place(x=150,y=50)
lastCol = Entry(root, width= 12)
lastCol.place(x=150, y=75)

#Label and text entry for the name of the to-be-created training set
Label(root, text="Enter the name of the training alignment file", font=('Calibri 10')).place(x=150,y=100)
outputName = Entry(root, width= 40)
outputName.place(x=75, y=125)

#Label and text entry for the name of the to-be-created testing set
Label(root, text="Enter the name of the testing data file", font=('Calibri 10')).place(x=150,y=150)
toTest = Entry(root, width= 40)
toTest.place(x=75, y=175)

#allows user to see the alignment in a fasta file
def AlignViewer():
    #variables must be declared global to properly function with Tkinter
    global alignBox
    global button

    #file path for the FASTA file
    toSeePath = filedialog.askopenfilename()

    #Checks to see if user has pressed cancel button on the file dialog
    #Checks to see if user has inputted improper file type
    if not toSeePath:
        tkinter.messagebox.showerror("Canceled", "operation canceled")
        return
    elif toSeePath.lower().endswith(('.fasta', '.fa', '.txt')):
        pass
    else:
        tkinter.messagebox.showerror("File error", "Improper file type")
        return

    #Creates the secondary window where the alignment is displayed
    aV = Toplevel(root)
    aV.title("Viewing Alignment")
    aV.geometry('800x600')
    aV.configure(bg='green')

    #text box to show the alignment
    alignBox = Text(aV)

    #reads the inputted file and stores all the strings in a giant string
    allSeqs = ""
    seqLine = ""
    with open(toSeePath, 'r') as reader:
        for lineRed in reader:
            if (lineRed.count(">") != 0):
                allSeqs += seqLine
                allSeqs += "\n"
                seqLine = ""
            else:
                seqLine += (lineRed)

    if (seqLine != ""):
        allSeqs += seqLine

    alignBox.insert(tkinter.END,allSeqs)
    alignBox.pack(expand=True,fill=BOTH)
    button = Button(aV, text="Exit",command=aV.destroy)
    button.pack()

    aV.mainloop()

#allows user to see all the sequences in a fasta file
def SeqViewer():
    #variables must be declared global to properly function with Tkinter
    global alignBox
    global button

    #file path for the FASTA file
    toSeePath = filedialog.askopenfilename()

    #Checks to see if user has pressed cancel button on the file dialog
    #Checks to see if user has inputted improper file type
    if not toSeePath:
        tkinter.messagebox.showerror("Canceled", "operation canceled")
        return
    elif toSeePath.lower().endswith(('.fasta', '.fa', '.txt')):
        pass
    else:
        tkinter.messagebox.showerror("File error", "Improper file type")
        return

    #Creates the secondary window where the alignment is displayed
    seqView = Toplevel(root)
    seqView.title("Viewing Alignment")
    seqView.geometry('800x600')
    seqView.configure(bg='green')

    #text box to show the alignment
    alignBox = Text(seqView)

    #reads the inputted file and stores all the strings in a giant string
    allSeqs = ""
    with open(toSeePath, 'r') as reader:
        for lineRed in reader:
            if (lineRed.count(">") != 0):
                allSeqs += lineRed
                allSeqs += "\n"
            else:
                pass

    alignBox.insert(tkinter.END,allSeqs)
    alignBox.pack(expand=True,fill=BOTH)
    button = Button(seqView, text="Exit",command=seqView.destroy)
    button.pack()

    seqView.mainloop()

#allows user to view more information about the program
def readme():
    # variables must be declared global to properly function with Tkinter
    global infoBox
    global button

    #establishes the infoView window
    infoView = Toplevel(root)
    infoView.title("Viewing Alignment")
    infoView.geometry('500x400')
    infoView.configure(bg='green')

    #Text box to display the information
    infoBox = Text(infoView)

    readMe = ("This program is designed to allow users to take fasta files and trim alignments to their desired columns."
              + "\n" + "It additionally allows users to view an alignment.")
    infoBox.insert(tkinter.END,readMe)
    infoBox.pack()
    button = Button(infoView, text="Exit",command=infoView.destroy)
    button.pack()

    #runs the infoView window
    infoView.mainloop()

#closes the program - destroys everything
def close():
    root.destroy()

#this function takes the input file and processes it
def submissionAl():
    #variables to store the beginning and ending columns
    beginCol = int(firstCol.get())
    endCol = int(lastCol.get());

    #Checks if the beginning col is located before the ending column
    if (beginCol >= endCol):
        tkinter.messagebox.showerror("Error", "Improper numerical inputs")
        return

    #opens the file dialog and gets the filepath of the input file
    filePath = filedialog.askopenfilename()

    #Checks if the file is existent and in the correct format
    if not filePath:
        tkinter.messagebox.showerror("Canceled","operation canceled")
        return
    elif filePath.lower().endswith(('.fasta', '.fa', '.txt')):

        tkinter.messagebox.showinfo("File accepted", "Conducting trimming")
    else:
        tkinter.messagebox.showerror("File error", "Improper file type")
        return

    #reads the inputted file and stores all the strings in a list
    with open(filePath, 'r') as reader:
        linesFile = []
        seqLine = ""
        numSeqs = 0

        for lineRed in reader:
            if (lineRed.count(">") != 0):
                linesFile.append(seqLine)
                linesFile.append(lineRed)
                seqLine = ""
                numSeqs += 1
            else:
                seqLine += lineRed

    #takes care of certain edge case issues in the loop
    if(seqLine != ""):
        linesFile.append(seqLine)

    if (linesFile[0].count(">") == 0):
        linesFile.pop(0)

    #Ask for the directory where the user wishes to store the output files
    tkinter.messagebox.showinfo("Choose directory", "Choose directory to place output files in")
    folderDir = filedialog.askdirectory()

    #Checks if user canceled
    if not folderDir:
        tkinter.messagebox.showerror("Canceled","operation canceled")
        return
    os.chdir(folderDir)

    #creates the training and testing output files
    try:
        nFname = outputName.get() + ".txt"
        newFile = open(nFname, "x")

        testFname = toTest.get() + ".txt"
        testFile = open(testFname, "x")
    except FileExistsError:
        tkinter.messagebox.showerror("Error", "The file that you want already exists")
        return
    #If the file already exists,the code catches the error and informs the user

    #counter variable checks how many seqs go into training set
    counter = 0
    numSeqsTraining = round(numSeqs * 0.8) #number of seqs that should go to training set

    #Creates the new output testing and training files
    for evLine in linesFile:
        if (counter >= numSeqsTraining):
            if (evLine.count(">") != 0):
                testFile.write(evLine)

            else:
                lineTr = evLine[beginCol:endCol]
                testFile.write(lineTr + "\n")
        else:

            if (evLine.count(">") != 0):
                newFile.write(evLine)
                counter+=0.5

            else:
                lineTr = evLine[beginCol:endCol]
                newFile.write(lineTr + "\n")
                counter+=0.5

    #closes the output files
    newFile.close()
    testFile.close()

    #informs user that the process is complete
    tkinter.messagebox.showinfo("Complete","Files " + nFname + " and " + testFname + " have been created.")
    tkinter.messagebox.showinfo("Complete", str(counter) + " seqs for training set" + "\n" + str(numSeqs)
                                           + " seqs total")

#submission button
submitButton = Button(root, text="Begin Trimming", command=submissionAl, pady=10)
submitButton.place(x=150, y=225)

#Viewer button
ViewerButton = Button(root, text="View alignment", command=AlignViewer, pady=10)
ViewerButton.place(x=300,y=225)

#Button to view more info
InfoButton = Button(root, text="Info", command=readme, pady=10)
InfoButton.place(x=0,y=225)

#Button to quite the program
ExitButton = Button(root, text="Exit", command=close, pady=10)
ExitButton.place(x=0,y=0)

#Button to get a list of the sequneces
ListButton = Button(root, text="List sequences", command=SeqViewer, pady=10)
ListButton.place(x=350,y=0)

#runs the program
root.mainloop()