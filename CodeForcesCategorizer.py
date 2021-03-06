__author__ = 'zihaozhu'
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from socket import timeout
import re
import sqlite3
import sys
import os

def insert(codeForces):
    conn = sqlite3.connect('codeForces.db')
    print("---Inserting data---")
    for item in codeForces:
       #type str keeps track of all the different types of problems
        #insert that into the database based off of entire string
        #use % to find
       type=""
       for st in item[3]:
           type= type+st+" "
       #print(type)
       conn.execute("INSERT INTO CODEFORCES VALUES(?,?,?,?,?)",(None,item[0],item[1],item[2],type))
    conn.commit()
    print ("Record created successfully!")
    conn.close()

#def userAuth():

#updates the db
def update(problems):
    conn=sqlite3.connect('codeForces.db')
    print("Attempting to update...")
    for prob in problems:
        #print(prob)
        conn.execute("UPDATE CODEFORCES SET STATUS = ? WHERE PROBLEM=?",(1,prob))
    conn.commit()
    print("Record updated successfully!")
    conn.close()
#checks user submission for the problems they've solved
def accepted(name):
    acceptedProblem=[]
    linkAdd="/page/1"
    link = "http://www.codeforces.com"
    linkTemp = "http://www.codeforces.com/submissions/"+name+linkAdd
    try:
        print(linkTemp)
        page = urlopen(linkTemp)
    except urllib.error.URLError:
        print("User does not exist")
        exit(0)
    except urllib.error.HTTPError:
        print("Something went wrong!")
        exit(0)
    except timeout:
        print("Time out!")
        exit(0)
    soup = bs(page.read(),"html.parser")
    linkAdd=soup.find_all('a', href=True, text="→")[0]['href']
    print(linkAdd)

    while(len(linkAdd)!=0):
        table = soup.find('table',{'class': 'status-frame-datatable'})
        #print(table)
        if table:
            problem = table.find_all('a', href=re.compile('/problemset/problem/\d+/\w+'))
            status = table.find_all('span')
            #print(status )
            status = [status[x].text for x in range(0,len(status))]
            problem =[problem[x].text.split() for x in range(0,len(problem))]
        for i in range (0,len(problem)):
            if(status[i]=="Accepted"):
                #print(problem[i])
                acceptedProblem.append((problem[i][0]))
        linkTemp = link+linkAdd
        soup =bs(urlopen(link+linkAdd).read(), "html.parser")
        submission=soup.find_all('a', href=True, text="→")
        try:
            linkAdd=submission[0]['href']
        except IndexError:
            print("Reached the end")
            break

    return set(acceptedProblem)

def setUp():
    #final list to keep track of all the data before insertion
    codeForces = []
    problemTypeSet = set()
    #check if database exists
    if(os.path.isfile('codeForces.db')):
        print("Connecting to database...")
        conn = sqlite3.connect('codeForces.db')
        #return
    else:
        conn = sqlite3.connect('codeForces.db')
        conn.execute('''CREATE TABLE CODEFORCES (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PROBLEM TEXT NOT NULL,
        TITLE   TEXT NOT NULL,
        STATUS  INT NOT NULL,
        TYPE TEXT NOT NULL
        );'''
        )
        print("Database created successfully.")
    link = "http://www.codeforces.com"
    page = urlopen(link)
    soup = bs(page.read(), "html.parser")
    problemSet = soup.find_all('a', href=True, text="Problemset")
    if(len(problemSet)==0):
        print("Link not found. Please check website")
    else:
        #print(problemSet)
        print("------Initiate crawling------")
        linkAdd=problemSet[0]['href']
        #print(problemSet[0]['href'])

    while(len(problemSet)!=0):
        table = soup.find('table', {'class': 'problems'})
        if table:
            rows = table.find_all('tr')
            for tr in rows:
                cols = tr.find_all('td')

                if(cols):
                    problemType=[]
                    problemNum = (cols[0].find_all('a', href=re.compile('/problemset/problem/\d+/\w*')))[0].text.strip()
                    problemName = (cols[1].find_all('a', href=re.compile('/problemset/problem/\d+/\w*')))[0].text.strip()
                    if(cols[1].find_all('div'))[1].find_all('a',{'class':'notice'}):
                        for type in (cols[1].find_all('div'))[1].find_all('a',{'class':'notice'}):
                            problemTypeSet.add(type.text)
                            problemType.append(type.text)
                    #for type in problemType:
                    #    insert(problemNum, problemName, 0, type)
                    codeForces.append((problemNum, problemName, 0,problemType))

        soup =bs(urlopen(link+linkAdd).read(), "html.parser")
        problemSet=soup.find_all('a', href=True, text="→")



        try:
            linkAdd = problemSet[0]['href']
        except IndexError:
            print("Reached the end")
            break
    #print(problemTypeSet)
    #print(codeForces)
    #insert(codeForces)
    conn.close()
    return problemTypeSet
"""
def main():
    setUp()
    handle = input("Enter handle name: ")
    acceptedProblem=accepted(handle)
    update(acceptedProblem)
main()
"""