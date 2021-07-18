import os
import tkinter.messagebox as tmsg
from tkinter import *
from tkinter.filedialog import *


def checkSave():
    global file
    global isSaved

    head = ""
    if file is None:
        head = "Untitled"
    else:
        head = f"{os.path.basename(file)}"

    if isSaved:
        root.title(f"{head} - Notepad")
    else:
        root.title(f"{head} - Notepad *")


def statusUpdate():
    global cursorPos
    global cursorPosList
    cursorPos = TextArea.index('insert')
    cursorPosList = cursorPos.split(".")
    statusVar.set(f"Row {cursorPosList[0]} Column {int(cursorPosList[1]) + 1}")
    statusBar.update()


def inputSome(event):
    global isSaved
    keyList = [16, 17, 18, 20, 27, 91, 144]
    for i in range(112, 124):
        keyList.append(i)
    for i in range(33, 41):
        keyList.append(i)
    if event.keycode not in keyList:
        isSaved = False
        checkSave()
    statusUpdate()


# Keyboard Shortcuts
def newFileShortcut(event):
    newFile()


def openFileShortcut(event):
    openFile()


def saveFileShortcut(event):
    saveFile()


def quitAppShortcut(event):
    quitApp()


def helpShortcut(event):
    about()


# FileMenu Functions
def newFile():
    global file
    global isSaved
    if isSaved:
        TextArea.delete(1.0, END)
        file = None
        checkSave()
        statusUpdate()
    else:
        ans = tmsg.askyesnocancel("Save", "Do you want to save this file")
        if ans:
            saveFile()
        elif ans is None:
            return
        else:
            isSaved = True
        newFile()


def openFile():
    global file
    global isSaved

    if isSaved:
        file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                                                   ("Text Files", "*.txt")])
        if file == "":
            file = None
        else:
            isSaved = True
            checkSave()
            TextArea.delete(1.0, END)
            f = open(file, "r")
            TextArea.insert(1.0, f.read())
            f.close()
    else:
        ans = tmsg.askyesnocancel("Save", "Do you want to save this file")
        if ans:
            saveFile()
        elif ans is None:
            return
        else:
            isSaved = True
        openFile()


def saveFile():
    global file
    global isSaved
    if file is None:
        file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                                                                                 ("Text Files",
                                                                                                  "*.txt")])
        if file == "":
            file = None
        else:
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()
            isSaved = True
    else:
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()
        isSaved = True
    checkSave()


def quitApp():
    global isSaved
    if not isSaved:
        ans = tmsg.askyesnocancel("Save", "Do you want to save this file")
        if ans:
            saveFile()
        elif ans is None:
            return
    root.destroy()


# EditMenu Functions
def cut():
    TextArea.event_generate(("<<Cut>>"))


def copy():
    TextArea.event_generate(("<<Copy>>"))


def paste():
    TextArea.event_generate(("<<Paste>>"))


# HelpMenu Functions
def about():
    tmsg.showinfo("Notepad", "This is a simple notepad made by Saksham Bindal in tkinter GUI.")


# MoreMenu Functions
def changeTheme():
    global i
    bg, fg = theme[i][0], theme[i][1]
    TextArea.config(bg=bg, fg=fg, insertbackground=fg)
    statusBar.config(bg=bg, fg=fg)
    if i < len(theme) - 1:
        i += 1
    else:
        i = 0


if __name__ == '__main__':
    root = Tk()
    root.geometry(f"{800}x{500}")

    file = None
    isSaved = True
    checkSave()

    # Creating Menu-bar
    MenuBar = Menu(root)

    # FileMenu
    FileMenu = Menu(MenuBar, tearoff=0)

    # Open new file
    FileMenu.add_command(label=f"New{'Ctrl+N'.rjust(20, ' ')}", command=newFile)

    # Open existing file
    FileMenu.add_command(label=f"Open{'Ctrl+O'.rjust(18, ' ')}", command=openFile)

    # Save file
    FileMenu.add_command(label=f"Save{'Ctrl+S'.rjust(20, ' ')}", command=saveFile)

    FileMenu.add_separator()
    FileMenu.add_command(label=f"Exit{'Ctrl+Q'.rjust(21, ' ')}", command=quitApp)

    # Packing
    MenuBar.add_cascade(label="File", menu=FileMenu)

    # EditMenu
    EditMenu = Menu(MenuBar, tearoff=0)

    # Cut, Copy & Paste
    EditMenu.add_command(label="Cut", command=cut)
    EditMenu.add_command(label="Copy", command=copy)
    EditMenu.add_command(label="Paste", command=paste)

    MenuBar.add_cascade(label="Edit", menu=EditMenu)

    # HelpMenu
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="About Notepad     Ctrl+H", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    # More Menu
    i = 1
    theme = [['white', 'black'], ['black', 'white'], ['red', 'white'], ['green', 'white']]
    MoreMenu = Menu(MenuBar, tearoff=0)
    MoreMenu.add_cascade(label="Change", command=changeTheme)
    MenuBar.add_cascade(label="Theme", menu=MoreMenu)

    root.config(menu=MenuBar)

    # Creating TextArea
    TextArea = Text(root, font="Consolas 11 bold", undo=True)
    TextArea.pack(fill=BOTH, expand=True)

    # Binding Events
    TextArea.bind("<KeyRelease>", inputSome)
    TextArea.bind("<Control-n>", newFileShortcut)
    TextArea.bind("<Control-o>", openFileShortcut)
    TextArea.bind("<Control-s>", saveFileShortcut)
    TextArea.bind("<Control-q>", quitAppShortcut)
    TextArea.bind("<Control-h>", helpShortcut)

    # Creating ScrollBar
    Scroll = Scrollbar(TextArea, troughcolor="red")
    Scroll.pack(side=RIGHT, fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

    # Creating Status Bar
    cursorPos = TextArea.index('insert')
    cursorPosList = cursorPos.split(".")

    statusVar = StringVar()
    statusVar.set(f"Row {cursorPosList[0]} Column {int(cursorPosList[1]) + 1}")

    statusBar = Label(root, textvar=statusVar, font="Consolas 10 bold", anchor="e", padx=30)
    statusBar.pack(side=BOTTOM, fill=X)

    # Close Button
    root.protocol('WM_DELETE_WINDOW', quitApp)

    root.mainloop()
