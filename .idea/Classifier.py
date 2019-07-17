import pandas as pd
class Classifier():
    def __init__(self,Structure,bins):
        self.structure=Structure
        self.bins=bins


    def binning(self,col,cutPoints,min,max,labels=False):
        break_points=[min]+cutPoints+[max]
        discritizedData=pd.cut(col,bins=break_points,labels=labels,include_lowest=True)
        return discritizedData

    def discritization(self,dataToDiscritizate,feature,trainSet):
        # sepeate to bins and replace with bin value
        cutPoints = []
        labels = []
        curBin = 0
        min = trainSet[feature].min()
        max = trainSet[feature].max()
        jump = (max - min) / int(self.bins.get())
        while curBin < int(self.bins.get()) - 1:
            cutPoints.insert(curBin, min + (curBin + 1) * jump)
            labels.insert(curBin, curBin)
            curBin = curBin + 1
        labels.insert(curBin, curBin)
        newDate = self.binning(dataToDiscritizate[feature], cutPoints,min,max,labels)
        dataToDiscritizate[feature] = newDate
        return dataToDiscritizate
        return dataToDiscritizate

    def cleanData(self,pathToDataToClean,trainSet):
        numericFeature=[]
        #read the data that we should clean
        try:
            _DataToClean=pd.read_csv(pathToDataToClean)
        except:
            error = Tk()
            error.title("Naive Bayes Classifier")
            error.minsize(400, 300)
            infoLabel = Label(error, text="Empty File!")
            infoLabel.pack()
            error.mainloop()
        dataToClean=pd.DataFrame(_DataToClean)
        df=pd.DataFrame(self.structure,columns=None)
        i=-1
        while i<=len(df.values)-1:
            if i==-1:
                line=df.axes[1]._data
            else:
                line=df.values[i]
            curLine=line[0].split(' ')
            feature = curLine[1]
            if "NUMERIC" not in curLine:
                common=trainSet[feature].value_counts().idxmax()
                dataToClean[feature].fillna(common,inplace=True)

            elif "NUMERIC" in curLine:
                #replace null values in average
                numericFeature.append(feature)
                average= trainSet[feature].mean()
                dataToClean[feature].fillna(average, inplace=True)
            i=i+1
        return dataToClean,numericFeature

    def getProbTable(self,line, featchers, classValues,classInfo, trainSet):
        # create table to store all probability by class and feaure
        probOfCurrentLine = pd.DataFrame(None, columns=featchers, index=classValues)
        for c in classValues:
            i=0;
            while i<len(featchers):
               # print "num of lines with class= "+c +" and "+featchers[i]+ " = "+str(line[i])
                numOfBothValues=len(trainSet.loc[(trainSet[featchers[i]] == line[i]) & (trainSet["class"] == c),
                                                 [featchers[i],"class"]])
               # print "num of both values is :"+str(numOfBothValues)
                mutualProb=float(numOfBothValues+2*(float(1)/len(classValues)))/(classInfo[classValues.index(c)]*len(trainSet)+2)
               # print classInfo[classValues.index(c)]*len(trainSet)+2
                #print "mutual prob is: "+ str(mutualProb)
                probOfCurrentLine.xs(c)[featchers[i]]=mutualProb
                i=i+1
        return probOfCurrentLine

    def classify(self,path,trainSet):
        pd.options.mode.chained_assignment = None  # default='warn'
        df = pd.DataFrame(self.structure, columns=None)
        #get all featchers into 'featchers' array
        featchers=[]
        curFeature = -1
        while curFeature <= len(df.values) - 2:
            if curFeature == -1:
                line = df.axes[1]._data
            else:
                line = df.values[curFeature]
            curLine = line[0].split(' ')
            featchers.append(curLine[1])
            curFeature=curFeature+1

        #complete null values in Test set
        cleanTestSet,numericFeatures=self.cleanData(path+"\\test.csv",trainSet)
        f=open(path+"//output.txt","w+")
        #get info about class values
        classInfo= pd.value_counts(trainSet["class"],sort=False,normalize=True)
        classValues = [] #contain all classValues
        c=0
        while c<=len(classInfo)-1:
            classValues.append(classInfo[classInfo==classInfo.values[c]].index[0])
            c=c+1

        #discritizide test and train set
        for numericFeat in numericFeatures:
            testSet=self.discritization(cleanTestSet,numericFeat,trainSet)
            trainSet=self.discritization(trainSet,numericFeat,trainSet)

        #iterate over lines in testTest
        lineInx=0
        for line in testSet.values:
            #get Probabilities table accourding values of line
            table=self.getProbTable(line,featchers,classValues,classInfo,trainSet)
            c=0
            # add coloumns - "multiplyProb" and probClass
            featchers.insert(0, "probClass")
            featchers.insert(0, "multiplyProb")
            table.insert(0, "probClass", None, allow_duplicates=False)
            table.insert(0, "multiplyProb", None, allow_duplicates=False)

            while c<len(classValues):
                # do muliplation with prob to class
                i = 1  # first cell is for multiplayProb
                output = 1
                #insert to class count(Ci)/total
                table.xs(classValues[c])["probClass"]=classInfo[c]
                #multiplay all probabilities
                while i<len(featchers):
                    output=float(output)*float(table.xs(classValues[c])[featchers[i]])
                    i=i+1
                #insert output of multiply to table
                table.xs(classValues[c])["multiplyProb"]=output
                c=c+1
            #choose max - it's the classification
            maxValue= table['multiplyProb'].max()
            t=table.index.get_loc(table.index[table['multiplyProb'] == maxValue][0])
            classClassify=classValues[t]
            f.write(str(lineInx+1)+" "+classClassify+"\n")
            featchers.remove('multiplyProb')
            featchers.remove('probClass')
            lineInx=lineInx+1
        f.close()
