'''

Program: Essay Evaluator


'''
import csv
import numpy as np

import matplotlib.pyplot as plt
from nltk import wordpunct_tokenize
from nltk.tag import pos_tag

import re
import enchant

from LSA.LSAClass import LSA

'''For Grammar Checker'''
#Start

#from py4j.java_gateway import JavaGateway
#gateway = JavaGateway()
#grammarCheckerApp = gateway.entry_point

#End

print "\'ESSAY EVALUATOR\'\n\n"

'''LSA Initialization'''
stopwords = ['a','an','the','to','for','in','on','up','down','at','before','after','above','below','under','over','what','when','who','how','why','which','where','if','so','but','and','otherwise','however','hence','therefore','that','he','she','it','they','each','every','all','you','I','we','him','her','us','my','mine','is','was','were','are','am','will','shall','may','might','can','could','should','would','do','did','does','done','has','have','had','again']
ignorechars = ''',:'!'''

print "\nInitializing LSA Procedure..."
lsaObj = LSA(stopwords, ignorechars)
print "Building Word By Document Matrix..."
lsaObj.build()
#lsaObj.printA()
print "\nBuilding LSA Model..."
lsaObj.calc()
print "\nLSA Model Ready"
lsaObj.printSVD()

def returnPOSTaggedWords(text):
    output={"CC":0,"CD":0,"DT":0,"EX":0,"FW":0,"IN":0,"JJ":0,"JJR":0,"JJS":0,"LS":0,"MD":0,"NN":0,"NNP":0,"NNPS":0,"NNS":0,"PDT":0,"POS":0,"PRP":0,"PRP$":0,"RB":0,"RBR":0,"RBS":0,"RP":0,"SYM":0,"TO":0,"UH":0,"VB":0,"VBD":0,"VBG":0,"VBN":0,"VBP":0,"VBZ":0,"WDT":0,"WP":0,"WP$":0,"WRB":0,"#":0,"$":0,"''":0,"(":0,")":0,",":0,".":0,":":0,"''":0,"-NONE-":0,"``":0}
    tokens=wordpunct_tokenize(text)
    tagged=pos_tag(tokens)

    for word,pos in tagged:
        output[pos]=output[pos]+1
    return output

def returnNounCount(TaggedWords):
    return (TaggedWords["NN"]+TaggedWords["NNP"]+TaggedWords["NNPS"]+TaggedWords["NNS"])

def returnVerbCount(TaggedWords):
    return (TaggedWords["VB"]+TaggedWords["VBD"]+TaggedWords["VBG"]+TaggedWords["VBN"]+TaggedWords["VBP"]+TaggedWords["VBZ"])

def returnAdjectiveCount(TaggedWords):
    return (TaggedWords["JJ"]+TaggedWords["JJS"]+TaggedWords["JJR"])

def returnAdverbCount(TaggedWords):
    return (TaggedWords["RB"]+TaggedWords["RBR"]+TaggedWords["RBS"])

def returnWordCount(essay):
    return len(re.split(r'[^0-9A-Za-z]+',essay))

def returnSentenceCount(essay):
    return len(re.split(r'[.!?]+', essay))

def returnCommaCount(essay):
    return essay.count(',')

"""
def returnSpellingScore(text):
    ignorechars = ''',:.;'?!'''
    dictionary=enchant.Dict("en_US")
    words = re.findall(r"(?i)\b[a-z]+\b", text)

    totalno=0.0
    score=0.0

    for w in words:
        w = w.translate(None, ignorechars)

        if dictionary.check(w)==True:
            score=score+1;
        totalno=totalno+1
    percentage=score/totalno;

    return percentage * 10

def returnGrammarScore(essay):
    return grammarCheckerApp.returnScore(essay)
"""

def evaluateEssay(essay,coeff):
    m1=coeff[0]
    m2=coeff[1]
    m3=coeff[2]
    m4=coeff[3]
    m5=coeff[4]
    m6=coeff[5]
    m7=coeff[6]
    m8=coeff[7]
    #m9=coeff[8]

    #wGrammarScore = coeff[9]
    c=coeff[8]

    TaggedWords = returnPOSTaggedWords(essay)
    wordCount=returnWordCount(essay)*1.0
    adjCount=(returnAdjectiveCount(TaggedWords)/wordCount) * 100
    advCount=(returnAdverbCount(TaggedWords)/wordCount) * 100
    nounCount=(returnNounCount(TaggedWords)/wordCount) * 100
    verbCount=(returnVerbCount(TaggedWords)/wordCount) * 100
    sentenceCount=returnSentenceCount(essay)
    commaCount=returnCommaCount(essay)

    coherenceScore=lsaObj.calculateCoherence(essay) * 100

    #spellingScore = returnSpellingScore(essay)
    #grammarScore = returnGrammarScore(essay)

    print "\n\nEvaluating Essay...\n"

    print "Adjective Count -> ",adjCount
    print "Adverb Count -> ",advCount
    print "Noun Count -> ",nounCount
    print "Verb Count -> ",verbCount
    print "Word Count -> ",wordCount
    print "Sentence Count -> ",sentenceCount
    print "Comma Count -> ",commaCount
    print "Average Coherence ->",coherenceScore
    #print "Spelling Score ->",spellingScore
    #print "Grammar Score ->",grammarScore

    predicted_score=c+(m1*adjCount)+(m2*advCount)+(m3*nounCount)+(m4*verbCount)+(m5*wordCount)+(m6*sentenceCount)+(m7*commaCount)+(m8*coherenceScore)
    print "Predicted Score of Essay --> ", predicted_score

def main():
    print "\nReading Essays and Building Regression Model...\n"
    csvfile=csv.reader(open("training_set_rel3.csv","rb")) #Opens csv file
    i=0;
    count=0
    essays=[]
    grades=[]

    for row in csvfile:             #Reads the 1st 10 records
        if i==0:
            i=i+1
            continue
        if i==10:
            break
        else:
            essays.append(row[2])    #3rd column in the sheet has the essay
            grades.append(row[6])   #7th column has the cumulative grade
            count=count+1;
            i=i+1

    g=0
    essayGrades=[]

    arrayVariable1=[]
    arrayVariable2=[]
    arrayVariable3=[]
    arrayVariable4=[]
    arrayVariable5=[]
    arrayVariable6=[]
    arrayVariable7=[]

    arrayVariableLSACoherence = []
    #arrayVariableSpellingScore = []
    #arrayVariableGrammarScore=[]

    for essay in essays:
        print "Reading Essay %d ..." % (g+1)

        output = returnPOSTaggedWords(essay)
        grade=grades[g]
        g=g+1
        essayGrades.append(grade)

        wordCount = returnWordCount(essay) *1.0
        adjective=(returnAdjectiveCount(output)/wordCount) * 100
        adverb=(returnAdverbCount(output)/wordCount) * 100
        noun=(returnNounCount(output)/wordCount) * 100
        verb=(returnVerbCount(output)/wordCount) * 100
        sentenceCount = returnSentenceCount(essay)
        commaCount = returnCommaCount(essay)
        coherenceScore = lsaObj.calculateCoherence(essay) * 100
        #spellingScore = returnSpellingScore(essay)
        #grammarScore = returnGrammarScore(essay)

        arrayVariable1.append(adjective)
        arrayVariable2.append(adverb)
        arrayVariable3.append(noun)
        arrayVariable4.append(verb)
        arrayVariable5.append(wordCount)
        arrayVariable6.append(sentenceCount)
        arrayVariable7.append(commaCount)

        arrayVariableLSACoherence.append(coherenceScore)
        #arrayVariableSpellingScore.append(spellingScore)
        #arrayVariableGrammarScore.append(grammarScore)


    print "\nApplying Regression...\n"

    x = np.array([arrayVariable1, arrayVariable2, arrayVariable3, arrayVariable4, arrayVariable5, arrayVariable6, arrayVariable7, arrayVariableLSACoherence], np.int32)

    y=np.array(essayGrades)          #Array for the assigned grades
    nn = np.max(x.shape)
    X = np.vstack([x,np.ones(nn)]).T        #Preparing for regression function
    print X
    print y

    coeff = np.linalg.lstsq(X, y)[0]

    print coeff
    print "\nAdj Count Weight--> ", coeff[0]
    print "Adv Count Weight--> ", coeff[1]
    print "Noun Count Weight--> ", coeff[2]
    print "Verb Count Weight--> ", coeff[3]
    print "Word Count Weight--> ", coeff[4]
    print "Sentence Count Weight--> ", coeff[5]
    print "Comma Count Weight--> ", coeff[6]

    print "Average Coherence Weight--> ", coeff[7]
    #print "Spelling Score Weight,  --> ", coeff[8]
    #print "Grammar Score Weight,  --> ", coeff[9]

    print "Fitted Line's Constant Value, c --> ", coeff[8]

#     plt.plot(arrayVariable1, y, 'o', label='Original data', markersize=10) #Plotting graphically
#     plt.plot(arrayVariable1, coeff[0]*arrayVariable1 + coeff[2], 'r', label='Fitted line')
#     plt.xlabel('Kappa Value')
#     plt.ylabel('Score')
#     plt.legend()
#     plt.show()
#
    print "\nEVALUATION MODEL READY\n"
    print "Evaluating essay..."
    #This is the target essay. Row no 15th on the sheet

    filename = "testEssays.txt"
    while filename != 'exit':
        with open(filename) as fp:
            for line in fp:
                testText = line
                evaluateEssay(testText,coeff)
        filename = raw_input("\nEnter filename or type \'exit\' to exit: ")


if __name__ == '__main__':
    main()
