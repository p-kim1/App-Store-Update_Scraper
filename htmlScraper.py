from bs4 import BeautifulSoup as BS
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from google import google
from datetime import date
import urllib.request
import numpy as np
import sys
import os

#Scrape app store page for update dates
def scrapeDates(app):
        searchResult = google.search(app + " app store ios")
        url = searchResult[0].link
        appName = searchResult[0].name
        with urllib.request.urlopen(url) as html:
                page = BS(html, 'html.parser')

        updates = {}
        for verHist in page.find_all('li'):
                if(verHist['class'] == ['version-history__item']):
                        version = verHist.contents[1].string
                        date = verHist.contents[3].string
                        year = date.split()[2]
                        if(year not in updates.keys()):
                                updates[year] = []
                        updates[year].append([version,date])
        return updates,appName

#Loop until valid app name given
def searchCheck():
        while(1):
                try:
                        app = input("Please enter the name of the app: ")
                        updates,appName = scrapeDates(app)
                        break
                except:
                        print("ERORR: invalid app name")
        return updates,appName

#Write update timelines of top 100 apps as .txt or .csv files
def writeData(fileType,updates,appName,path):
        if fileType == '2':
                path += '.txt'
        else:
                path += '.csv'
                
        f = open(path,'w')
        for key in sorted(updates.keys()):
                for i in range(len(updates[key]),0,-1):
                        version = updates[key][i-1][0]
                        date = updates[key][i-1][1]
                        f.write(version+","+date+'\n')
        f.close()

def printData(updates):
        print('\nUpdate Timeline:')
        for key in sorted(updates.keys()):
                print(key+':','Total updates:',len(updates[key]))
                print('\tVersion:','\t\tDate:')
                for i in range(len(updates[key]),0,-1):
                        version = updates[key][i-1][0]
                        date = updates[key][i-1][1]
                        sys.stdout.write("%+14s %+25s\n" % (version, date))

def graphData(updates,appName):
        dates = []
        for key in sorted(updates.keys()):
                for i in range(len(updates[key]),0,-1):
                        dateTok = str(updates[key][i-1][1]).split()
                        year = int(dateTok[2])
                        month = monthNum(dateTok[0])
                        day = int(dateTok[1][:-1])
                        dates.append(date(year,month,day))
                        print(date(year,month,day))

        xlow = dates[0]
        xhigh = dates[-1]
        if xlow.month > 5:
                xlow = xlow.replace(month = xlow.month - 5)
        else:
                xlow = xlow.replace(month = 12 - xlow.month - 5)
                xlow = xlow.replace(year = xlow.year - 1)
        if xhigh.month < 7:
                xhigh = xhigh.replace(month = xhigh.month + 5)
        else:
                xhigh = xhigh.replace(month = 5 + xhigh.month - 12)
                xhigh = xhigh.replace(year = xhigh.year + 1)
        print(xlow,'|',xhigh)
        

        values = [1]*len(dates)

        
        fig, ax = plt.subplots(figsize=(7,1.5))
        plt.scatter(dates, [1]*len(dates), c=values, marker='o', s=25)
        hfmt = DateFormatter('%Y/%m/%d')
        fig.autofmt_xdate()
        ax.xaxis.set_major_formatter(hfmt)
        
        ax.yaxis.set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        
        ax.get_yaxis().set_ticklabels([])
        plt.tight_layout()
        plt.show()


def monthNum(month):
        monthDict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,
                     'May':5, 'Jun':6, 'Jul':7, 'Aug':8,
                     'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        return monthDict[month]
        
#Obtain data for top 100 apps in one of following categories: Free apps, Paid apps, Gross revenue
def top100Loop():
        inputDict = {'1' : ['Free Apps' ,'https://www.apple.com/itunes/charts/free-apps/'],
                    '2' : ['Paid Apps' ,'https://www.apple.com/itunes/charts/paid-apps/'],
                     '3' : ['Top Grossing Apps' ,'https://www.apple.com/itunes/charts/top-grossing-apps/']}
        top100 = np.empty([100,3], dtype = 'object')
        print('\n---TOP 100 OPTIONS---')     
        while(1):
                print('1) Free apps\n2) Paid apps\n3) Highest grossing apps')
                userInput = input("Choose the type of data (Enter any other key to return to Main Options): ")
                try:
                        url = inputDict[userInput][1]
                except:
                        print()
                        return

                with urllib.request.urlopen(url) as html:
                        page = BS(html, 'html.parser')
                i = -1
                for d in page.body.find_all('div'):
                        if d['class'] == ['main']:
                                for l in d.section.div.find_all('li'):
                                        i += 1
                                        top100[i][0] = l.strong.string
                                        top100[i][1] = l.a.img['alt']
                                        link = l.a['href']
                                        top100[i][2] = link[:link.find('&')]
                curData = inputDict[userInput][0]
                
                while(1):
                        print('\nCurrent Data:', curData)
                        print('1) Print top 100\n'+
                              '2) Save update timelines by app as .txt\n'+
                              '3) Save update timelines by app as .csv\n'+
                              '4) Choose different type of data')
                        userInput = input('Choose an option (Enter any other key to return to Main Options): ')
                        if(userInput == '1'):
                                print('\nTop 100',curData+':')
                                for row in top100:
                                        print(row[0],row[1])
                        elif(userInput == '2' or userInput == '3'):
                                os.makedirs('./Top 100 '+curData, exist_ok = True)
                                for row in top100:
                                        print('Saving data for:',row[0],row[1])
                                        updates,appName = scrapeDates(row[1])
                                        path = './Top 100 ' + curData + "/" + row[0][:-1] + ") " + row[1].replace('/','-')
                                        writeData(userInput,updates,appName,path)
                        elif(userInput == '4'):
                                break
                        else:
                                print()
                                return

def appLoop(updates,appName):
        while(True):
                print('\nCurrent app:',appName)
                print('1) Show updates by year\n'+
                      '2) Save update timelines by app as .txt\n'+
                      '3) Save update timelines by app as .csv\n'+
                      '4) Generate graph\n'+
                      '5) Select another app')
                userInput = input('Choose an option (Enter any other key to return to Main Options): ')
                if userInput == '1':
                        printData(updates)
                elif userInput == '2' or userInput == '3':
                        path = './' + appName.replace('/','-')
                        writeData(userInput,updates,appName,path);
                elif userInput == '4':
                        graphData(updates,appName)
                elif userInput == '5':
                        updates,appName = searchCheck()
                else:
                        print()
                        return

def main():
        while(1):
                print('---MAIN OPTIONS---')
                print('1) Get data for specific app\n2) Get data for top 100 apps')
                userInput = input('Choose an option (Enter any other key to quit): ')
                if userInput == '1':
                        updates,appName = searchCheck()
                        appLoop(updates,appName)
                elif userInput == '2':
                        top100Loop()
                else:
                        return
main()
