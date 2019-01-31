#!/usr/bin/python3
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2018)
#

from PIL import Image, ImageDraw, ImageFont
import math
import sys
import collections as col
import itertools as itr
CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
SMALL_PROB = math.log(1.0/10000000)
LIT_PIXEL = '*'
NON_LIT_PIXEL = ' '
EmissionProbModel = 'Bayes Net'



def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print (im.size)
    print (int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }



<<<<<<< HEAD
def emission_prob(testImageRep , actualLetter, dictOfCorrectRep ):
    matchedCount = 0
    for testRow , actualRow in zip(testImageRep,dictOfCorrectRep[actualLetter]):
        for pixelTest, pixelActual in zip(testRow,actualRow):
            if pixelTest == pixelActual:
                matchedCount += 1
     
        
    emissionGivenActLetter = matchedCount/(CHARACTER_HEIGHT*CHARACTER_WIDTH)
        
    return emissionGivenActLetter



#####
# main program
#(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]

train_img_fname = "courier-train.png"
train_letters = load_training_letters(train_img_fname)
test_img_fname = "test-1-0.png"
test_letters = load_letters(test_img_fname)

print(emission_prob(test_letters[12],'A',train_letters))
=======


def load_data(filename):
        
        ##returns list of sentences as each sentence is ( (words),(tags))
        
        AllSentencesAsLetters= [] ## [((words),(corresponding tags)), (sentence 2)]
        file = open(filename, 'r');
        for line in file:
            data = tuple([w for w in line.split()])
            sentence = ' '.join(data[0::2])
#            tags = data[1::2]
            Letters = tuple(sentence)
            
            
            AllSentencesAsLetters.append(Letters) #isolating sentence as well
        file.close()
        return AllSentencesAsLetters ##rerutns list of tuples as characters in the sentece  


>>>>>>> 0c3ad45cd5bd4c1937a523bfebefbb9e90431bb8
#####
# main program
    
    
    
def train(AllSentencesAsLetters):
    
    ###Initial letter probability####
    AllLetter1List = [characters[0] for characters in AllSentencesAsLetters]
        
    Total_Letter1 = len(AllLetter1List)
    ProbOfLetter1AsDict = dict(col.Counter(AllLetter1List)) 
    ProbOfLetter1AsDict = {letter: math.log(frequency/Total_Letter1) for letter,frequency in ProbOfLetter1AsDict.items()}
    
    
    ###rest letters probabilities
    
    AllButLetter1List = list(itr.chain.from_iterable([characters[1:] for characters in AllSentencesAsLetters]))
    Total_LetterButL1 = len(AllButLetter1List)
    ProbOfLetter_AllAsDict = dict(col.Counter(AllButLetter1List)) 
    ProbOfLetter_AllAsDict = {letter : math.log(frequency/Total_LetterButL1) for letter, frequency in ProbOfLetter_AllAsDict.items()} 
    
    
    ######transition probabilities
    
    seqLetters = []
    for sentence in AllSentencesAsLetters:
         ##can be combined in list comprehension but would lose readability
         
         seqLetters += [ letter + "_" + nextLetter for letter,nextLetter in zip(sentence,sentence[1:])]
     
    TotalNumSequences = len(seqLetters)
        
    ProbOfLetterSeqAsDict = dict(col.Counter(seqLetters))
    ProbOfLetterSeqAsDict = {letterSeq: math.log(frequency/TotalNumSequences) for letterSeq,frequency in ProbOfLetterSeqAsDict.items()}
    
    
    
    
    return ProbOfLetter1AsDict,ProbOfLetter_AllAsDict,ProbOfLetterSeqAsDict

def emission_prob(testImageRep , actualLetter, dictOfCorrectRep ):
    
        
    global EmissionProbModel
    m = 0.05    
    
    if EmissionProbModel == 'Naive Bayes':
    
        matchedCount = 0
        litPixels = 0

            
        for testRow , actualRow in zip(testImageRep,dictOfCorrectRep[actualLetter]):
            for pixelTest, pixelActual in zip(testRow,actualRow):
                if pixelTest == LIT_PIXEL:
                    litPixels += 1
                if pixelTest == pixelActual:
                    matchedCount += 1
               
           
        try: 
            
            emissionGivenActLetter = matchedCount*math.log(1-m) + ((CHARACTER_HEIGHT*CHARACTER_WIDTH)-matchedCount) * math.log(m) 
        except :
            emissionGivenActLetter = SMALL_PROB
    #    print(matchedCount)
    #   emissionGivenActLetter = matchedCount/(CHARACTER_HEIGHT*CHARACTER_WIDTH)
        return emissionGivenActLetter
    
    
    if EmissionProbModel == 'Bayes Net':
        
        logProb = 0
        for testRow , actualRow in zip(testImageRep,dictOfCorrectRep[actualLetter]):
        
            for position, (testPixel , prevActualPixel, ActualPixel) in enumerate(zip(testRow,[actualRow[0]]+list(actualRow),actualRow)): ##(e,e,f,g,h),(e,f,g,h)
            
                if position == 0:
                    ###possible cases of the distributions
                    if testPixel == ActualPixel and ActualPixel == LIT_PIXEL :   
                        logProb += math.log(1-m) + dictOfPixelProbs[actualLetter][LIT_PIXEL]
                        
                    if testPixel == ActualPixel and ActualPixel == NON_LIT_PIXEL :   
                        logProb += math.log(1-m) + dictOfPixelProbs[actualLetter][NON_LIT_PIXEL]
                        
                    if testPixel != ActualPixel and ActualPixel == LIT_PIXEL :   
                        logProb += math.log(m) + dictOfPixelProbs[actualLetter][LIT_PIXEL]
                    
                    if testPixel != ActualPixel and ActualPixel == NON_LIT_PIXEL :   
                        logProb += math.log(m) + dictOfPixelProbs[actualLetter][NON_LIT_PIXEL]
                    
                    
                else :
                    
                    if testPixel == ActualPixel :   
                        logProb += math.log(1-m) + dictOfPixelTransitionProbs[actualLetter][prevActualPixel+"_"+ActualPixel]
                        
                    
                    if testPixel != ActualPixel  :   
                        logProb += math.log(m) + dictOfPixelTransitionProbs[actualLetter][prevActualPixel+"_"+ActualPixel]
                    
                    
                    
                    
                    
            return logProb  
            

            

<<<<<<< HEAD
train_img_fname = "courier-train.png"
=======

def train_emissionModelParams(dictOfCorrectRep):
    
    
    dictOfTransitionProbs = col.defaultdict(dict)
    dictOfPixelProbs = col.defaultdict(dict)
    
    
    for letter in dictOfCorrectRep:
    
        
        seqPixels = []
        for pixelRow in dictOfCorrectRep[letter]:
            
            ##transition probabilities
            seqPixels.extend([ pixel + "_" + nextPixel for pixel,nextPixel in zip(pixelRow,pixelRow[1:])])
        
        
        ####starting probabilities priors
        collapsedListPixels = list(itr.chain.from_iterable(dictOfCorrectRep[letter]))
        
        totalPixels = len(collapsedListPixels)
        
        dictOfPixelProbs[letter] = dict(col.Counter(collapsedListPixels))
        
        dictOfTransitionProbs[letter] = dict(col.Counter(seqPixels))
        totalTransistions = sum(dictOfTransitionProbs[letter].values())
        
        
        dictOfPixelProbs[letter] = {key: math.log(value/totalPixels) for key,value in dictOfPixelProbs[letter].items()}
        dictOfTransitionProbs[letter]  = {key: math.log(value/totalTransistions) for key,value in dictOfTransitionProbs[letter].items()}
    
    return dictOfPixelProbs,dictOfTransitionProbs ##as logarithmic
    
    

#(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
test_img_fname = "C:/Users/ntihish/Documents/IUB/Elem of AI/asiignment 3/prgadugu-skandag-chhshar-a3/part2/test-0-0.png"
train_img_fname = "C:/Users/ntihish/Documents/IUB/Elem of AI/asiignment 3/prgadugu-skandag-chhshar-a3/part2/courier-train.png"
>>>>>>> 0c3ad45cd5bd4c1937a523bfebefbb9e90431bb8
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname) #list of strings representing letters



    
def Solve_hmm_viterbi(test_letters,train_letters):
    
    
   ##checck if trained 
   lastPosition = len(test_letters)-1
   ##sentence is passed as tuple of words
   maxPaths = col.defaultdict(dict)
   dictOfPostions = col.defaultdict(dict) ##postionons and letter probabilities
   for position,testLetter in enumerate(test_letters) :
       #for severy postion
       for queryletter in train_letters :
        #for eveery state at a postion
           if position == 0 :
               
              
               dictOfPostions[position][queryletter] = allSimpleLetterProbs.get(queryletter,SMALL_PROB) \
               + emission_prob(testLetter,queryletter,train_letters)
                   
               
               
               maxPaths[position][queryletter] = queryletter
               
               
               
           else:
               #max((value, prevPOS))
           
               (logProbability,prevStateLeadingToMax)  = \
               max(( (dictOfPostions[position-1][prevLetter]+ transitionProbs.get(prevLetter + "_" + queryletter, SMALL_PROB), prevLetter)\
                    for prevLetter in train_letters))

                 
                   
             
               dictOfPostions[position][queryletter] = logProbability + emission_prob(testLetter,queryletter,train_letters)
                   
               
               maxPaths[position][queryletter] = maxPaths[position-1][prevStateLeadingToMax] + "=>" + queryletter
   maxLastProb,lastMaxLetter = max(((probability,lastLetter) for lastLetter,probability in dictOfPostions[lastPosition].items()))
 
   return maxPaths[lastPosition][lastMaxLetter].replace("=>",'')



def solve_By_Simple(test_letters,train_letters):
    maxLettersList = []
        
    for position,testLetter in enumerate(test_letters):
        maxLetter = ''
        maxProb = -float("inf")
        for queryletter in train_letters :
            if position == 0 :
                
                currentProb = emission_prob(testLetter,queryletter,train_letters) + startingProbs.get(queryletter,SMALL_PROB)
            
            else:
                
                currentProb = emission_prob(testLetter,queryletter,train_letters) + allSimpleLetterProbs.get(queryletter,SMALL_PROB)
            
            if currentProb > maxProb:
                maxProb = currentProb
                maxLetter = queryletter
        maxLettersList.append(maxLetter)
        
                
    return ''.join(maxLettersList)




##load and train the tranistions and staritng probabilieites
data = load_data('bc.train')

startingProbs,allSimpleLetterProbs,transitionProbs = train(load_data('bc.train'))

dictOfPixelProbs,dictOfPixelTransitionProbs = train_emissionModelParams(train_letters)


#   return maxPaths
## Below is just some sample code to show you how the functions above work. 
# You can delete them and put your own code here!

print(Solve_hmm_viterbi(test_letters,train_letters))
print(solve_By_Simple(test_letters,train_letters))
# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
print ("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
print ("\n".join([ r for r in test_letters[2] ]))

if __name__ == '__main__':
    emission_prob(test_letters[0],'U',train_letters)
    allSimpleLetterProbs.get('S',SMALL_PROB)
    startingProbs.get('S',SMALL_PROB) + emission_prob(test_letters[0],'S',train_letters)
    startingProbs.get('T',SMALL_PROB) + emission_prob(test_letters[0],'T',train_letters)
    max(allSimpleLetterProbs.values())
    max(allSimpleLetterProbs, key=allSimpleLetterProbs.get)
    allSimpleLetterProbs[' ']
