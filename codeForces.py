__author__ = 'zihaozhu'
import tkinter
import sqlite3
import CodeForcesCategorizer
from tkinter import *

dbProb=[]

def getProblems(var):
    conn=sqlite3.connect('codeForces.db')
    cursor = conn.execute("SELECT PROBLEM, TITLE FROM CODEFORCES WHERE TYPE LIKE ? AND STATUS = ?",('%'+str(var.get())+'%',0))
    row=cursor.fetchall()

    conn.close()
    return row
def select(var):
    value = "value is %s" % var.get()
    row=getProblems(var)
    cs=myText.curselection()
    myText.delete(0,END)
    for problem in row:
        myText.insert(END,problem[0]+" "+problem[1])
    #print(value)

def textSelect(evt):
    prob=evt.widget
    index = int(prob.curselection()[0])
    value = prob.get(index)
    toplevel = Toplevel()
    #complete task
    problem=value.split()[0]
    print(problem)
    completed = Button(toplevel, text="Completed", width=10, command=lambda:CodeForcesCategorizer.update(problem))
    completed.pack()
    No = Button(toplevel,text="None", width=10, command=lambda:toplevel.destroy())
    No.pack()
    print("You selected item %s"%(value))


#do the following for responsive design
#problems=CodeForcesCategorizer.setUp()
problems=sorted(['None','2-sat', 'matrices', 'constructive algorithms', 'two pointers', 'sortings', 'implementation', 'games', 'graph matchings', 'combinatorics', 'string suffix structures', 'schedules', 'number theory', 'dp', 'bitmasks', 'flows', 'dsu', 'chinese remainder theorem', 'divide and conquer', 'ternary search', 'strings', 'graphs', 'dfs and similar', 'probabilities', 'shortest paths', 'expression parsing', 'brute force', 'meet-in-the-middle', 'binary search', 'greedy', 'hashing', 'geometry', 'trees', 'fft', 'data structures', 'math'])

window = Tk()
#problem list
var2=StringVar()
problemList = Label(window, text="Problems")
problemList.place(x=100,y=50)

#initial set up
setup = Button(window, text="Initial Set Up/Reset",command=lambda :CodeForcesCategorizer.setUp())
setup.place(x=200,y=340)
#text for the problems
text = Scrollbar(window)
myText = Listbox(window,yscrollcommand=text.set,width=30)

text.place(x=50,y=70)
myText.insert(END,"None")
myText.bind('<Double-Button-1>',textSelect)
myText.place(x=50,y=70)

text.config(command=myText.yview)
#following is the label for title
var=StringVar()
title = Label(window,text="CodeForces Categorizer",justify="center")
title.pack()
#label for problems
problemChoices = Label(window,textvariable=var)
var.set("Problem Types")
problemChoices.place(x=300,y=50)
var1 = StringVar(window)
#initialize value for drop down box
var1.set("None")
#drop down box for problem choices
dropDown = tkinter.OptionMenu(window,var1,*problems)
dropDown.place(x=300,y=70)
dropDown.configure(width=15)
#button to submit problem choice
submit = Button(window, text="Find", command=lambda: select(var1))
submit.place(x=420,y=70)
window.maxsize(500,500)
window.minsize(500,500)
window.mainloop()
