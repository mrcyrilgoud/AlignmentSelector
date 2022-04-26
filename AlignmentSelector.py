from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os

#the Tkinter root window
#First window that the user will see
root = tkinter.Tk()
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

    aV = Toplevel(root)
    aV.title("Viewing Alignment")
    aV.geometry('800x600')

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

#allows user to view more information about the program
def readme():
    # variables must be declared global to properly function with Tkinter
    global infoBox
    global button

    #establishes the infoView window
    infoView = Toplevel(root)
    infoView.title("Viewing Alignment")
    infoBox = Text(infoView)

    readMe = ("This program is designed to allow users to take fasta files and trim alignments to their desired columns."
              + "/n" + "It additionally allows users to view an alignment.")
    infoBox.insert(tkinter.END,readMe)
    infoBox.pack()
    button = Button(infoView, text="Exit",command=infoView.destroy)
    button.pack()

    infoView.mainloop()

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

    counter = 0
    numSeqsTraining = round(numSeqs * 0.8)


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

    newFile.close()
    testFile.close()
    tkinter.messagebox.showinfo("Complete","Files " + nFname + " and " + testFname + " have been created.")
    tkinter.messagebox.showinfo("Complete", str(counter) + " seqs for training set" + "\n" + str(numSeqs)
                                           + " seqs for testing set")

#submission button
submitButton = Button(root, text="Begin Trimming", command=submissionAl, pady=10)
submitButton.place(x=150, y=225)

#Viewer button
ViewerButton = Button(root, text="View alignment", command=AlignViewer, pady=10)
ViewerButton.place(x=300,y=225)

#Button to view more info
InfoButton = Button(root, text="Info", command=readme, pady=10)
InfoButton.place(x=0,y=225)

#runs the program
root.mainloop()