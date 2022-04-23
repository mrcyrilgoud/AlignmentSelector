from tkinter import *
from tkinter import ttk

# import messagebox from tkinter module
import tkinter.messagebox

# create a tkinter root window
root = tkinter.Tk()

# root window title and dimension
root.title("Alignment Selector")
root.geometry('500x300')

firstCol = Entry(root, width= 42)
firstCol.place(relx= .5, rely= .3, anchor= CENTER)

lastCol = Entry(root, width= 42)
lastCol.place(relx= .5, rely= .5, anchor= CENTER)

# Create a messagebox showinfo

def East():
    tkinter.messagebox.showinfo("Welcome to GFG", "East Button clicked")


def West():
    tkinter.messagebox.showinfo("Welcome to GFG", "West Button clicked")


def North():
    tkinter.messagebox.showinfo("Welcome to GFG", "North Button clicked")


def South():
    tkinter.messagebox.showinfo("Welcome to GFG", "South Button clicked")


# Create a Buttons

Button1 = Button(root, text="West", command=West, pady=10)
Button2 = Button(root, text="East", command=East, pady=10)


# Set the position of buttons
Button1.pack(side=LEFT)
Button2.pack(side=RIGHT)


root.mainloop()