from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import os
import pandas as pd
from Classifier import *

def build():
    if not entry1.get()=="":
        checkBinNum()
        #get sturucture file
        pathToStructure=entry1.get()+"\\Structure.txt"
        pathToStructure = pathToStructure.replace('/', '\\')
        try:
            structure = pd.read_csv(pathToStructure,index_col=False,sep='\t')
        except:
            popErrorMessage("Error- Empty Files!")

      #  df_structure=pd.DataFrame(structure)
       # print df_structure
        #get train set
        pathToTrainSet=entry1.get()+"\\train.csv"
        pathToTrainSet=pathToTrainSet.replace('/','\\')
        try:
            _trainSet = pd.read_csv(pathToTrainSet)
        except:
          popErrorMessage("Error- Empty Files!")

        df_trainSet = pd.DataFrame(_trainSet)
        classifier = Classifier(structure, entry2)
        updateTrainSet,numericFeaturesArr=classifier.cleanData(pathToTrainSet,df_trainSet)
        globals()['trainSet']=updateTrainSet
        #relase Classify botton
        classifyBut.config(state="normal")
        popErrorMessage("Building classifier using train-set is done!")

def exit():
    sys.exit(0)



def Classify():
    # get sturucture file
    pathToStructure = entry1.get() + "\\Structure.txt"
    pathToStructure = pathToStructure.replace('/', '\\')
    try:
        structure = pd.read_csv(pathToStructure, index_col=False, sep='\t')
    except:
       popErrorMessage("Error- Empty File!")
    #create classifier & classify Test set
    classifier=Classifier(structure,entry2)
    classifier.classify(entry1.get(),trainSet)

    end=Tk()
    end.title("Naive Bayes Classifier")
    end.minsize(400, 300)
    infoLabel = Label(end, text="Classified Successfully!")
    infoLabel.pack()
    okBut = Button(end, text="OK", command=exit)
    okBut.pack()
    end.mainloop()
def close():
    root2.destroy()
#present error message
def popErrorMessage(message):
    globals()['root2'] = Tk()
    root2.title("Naive Bayes Classifier")
    root2.minsize(300, 200)
    error = Label(root2, text=message)
    error.pack()
    ok_but = Button(root2, text="OK",command=close)
    ok_but.pack()
    root2.mainloop()


def browseFile():
    filename=tkFileDialog.askdirectory()
    #in case one or more files missing, pop error message
    if validPath(filename)=="Error":
       popErrorMessage("Some of the files missing in the Path.\n try again")
    else:
        entry1.insert(0, filename)


def checkBinNum():
    try:
        input=int(entry2.get())

        if input<1:
         popErrorMessage("You enter invalid value in bin field.\n try again")
    except ValueError:
        popErrorMessage("You enter invalid value in bin field.\n try again")


#check all neccery files in path
def validPath(filename):
    if os.path.isfile(filename+ "/Structure.txt")==FALSE | os.path.isfile(filename+ "/train.csv")== FALSE | os.path.isfile(filename+ "/test.csv")==FALSE:
        return "Error"

global trainSet
global root2

root = Tk()
root.title("Naive Bayes Classifier")
root.minsize(400, 300)
# create entries
entry1 = Entry(root)
entry2 = Entry(root)
# crete bottoms
browserBut = Button(root, text="Browse", command=browseFile)
buildBut = Button(root, text="Build",command=build)
classifyBut = Button(root, text="Classify",command=Classify,state=DISABLED)
pathLabel = Label(root, text="Directory Path")
binsLabel = Label(root, text="Discretization Bins")


# locate widgets
pathLabel.grid(row=0, sticky=E)
entry1.grid(row=0, column=1)
browserBut.grid(row=0, column=2)
binsLabel.grid(row=1, sticky=E)
entry2.grid(row=1, column=1)
buildBut.grid(row=2)
classifyBut.grid(row=3)

root.mainloop()
