import os
os.chdir("C:/Users/User/Google Drive/Documenten/RU/Jaar 6/Information Retrieval/IR Project")
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, webbrowser
from Recipe import Recipe
from BM25f import *

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('recipeGUI.ui', self) # Load the .ui file
        #add button
        self.button = self.findChild(QtWidgets.QPushButton, 'searchButton') # Find the button
        self.nextScenario = self.findChild(QtWidgets.QPushButton, 'nextScenario') # Find the button
        #refer to def when pressed
        self.button.clicked.connect(self.searchButtonPressed) # Remember to pass the definition/method, not the return value!
        self.nextScenario.clicked.connect(self.nextScenarioPressed)
        #add input
        self.input = self.findChild(QtWidgets.QTextEdit, 'searchBar')
        #add results widgetlist
        self.results = self.findChild(QtWidgets.QListWidget, 'queryResults')
        #couple to action
        self.results.itemClicked.connect(self.itemClicked)
        # Show the GUI
        self.show() 
        #read in data
        self.weights=[1,1,1]
        self.data = bag(pd.read_csv("Data.csv",sep=",",header=None).values,self.weights)
        #set parameters
        self.b = 0.75
        self.k = 1.2
        self.N = 10
        self.i = 0 #aantal queries
        self.j = 0 #aantal clicks
        self.scenarionumber=0
        self.engineList = []
        self.scenarioList = []
        #Vul hier de experimentkey in als lijst van tuples
        #Bijvoorbeeld: self.experiment= [['s6', 1], ['s4', 2], ['s3', 2], ['s1', 1], ['s2', 1], ['s9', 1], ['s5', 2], ['s10', 1], ['s7', 2], ['s8', 2]]

        self.experiment= [['s6', 1], ['s4', 2], ['s3', 2], ['s1', 1], ['s2', 1], ['s9', 1], ['s5', 2], ['s10', 1], ['s7', 2], ['s8', 2]]
        
        #transform key into list of searchengines to use        
        for s in self.experiment:
            self.engineList.append(s[1])
            self.scenarioList.append(s[0])
            #print(s[1])
        self.engine = self.engineList[self.scenarionumber] #1=default, 2=titlefocussedsearch
        print(str(self.scenarionumber+1)+"|New Scenario: "+ str(self.scenarioList[self.scenarionumber]) +" with engine: "+ str(self.engineList[self.scenarionumber]))

        
    def searchButtonPressed(self):
        self.results.clear()
        print("Query = ", self.input.toPlainText())
        self.i += 1
        print("nQuery = ", self.i)
        query = self.input.toPlainText()
        #use different weights based on the search engine to use
        if self.engine >1:
            self.weights = [10,1,1] #use titlefocussed engine
        else:
            self.weights = [1,1,1] #use unfocussed engine
        #search!    
        self.res = BM25f(query, self.data, self.weights, self.b, self.k, self.N)
        for r in self.res:
            self.results.addItem(r[0].title)
        if len(self.res) == 0:
            self.results.addItem("Geen resultaten gevonden")
    
    def nextScenarioPressed(self):
        self.scenarionumber += 1
        print("Scenario Summary, nQueries = "+str(self.i)+" nClicks = "+str(self.j))
        self.i=0
        self.j=0
        print(str(self.scenarionumber+1)+"|New Scenario: "+ str(self.scenarioList[self.scenarionumber]) +" with engine: "+ str(self.engineList[self.scenarionumber]))
        self.engine = self.engineList[self.scenarionumber]
        
    
    def itemClicked(self, item):
        if not item.text() == "Geen resultaten gevonden":
            self.j += 1
            print("Click = ", item.text())
            print("nClick = ", self.j)
            for i in range(0,len(self.res)):
                if item.text() == self.res[i][0].title:
                    webbrowser.open("https://www.ah.nl/" + self.res[i][0].link)

def window():
    app = QApplication(sys.argv)
    win = Ui()
    win.setWindowTitle("RecipeSearch")
    win.show() 
    
    
    sys.exit(app.exec_())

window()
    