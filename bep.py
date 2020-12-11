# -*- coding: utf-8 -*-
"""Untitled.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ayZ-dVn2nwoagznv-esZTz39PXS3B3Ra
"""

from __future__ import print_function
import re
from nltk.corpus import stopwords
import nltk
import collections
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
#import rbm
import math
from operator import itemgetter
import pandas as pd
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
from nltk.stem import PorterStemmer
from collections import Counter
import para_reader
import os
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
porter = PorterStemmer()

stemmer = nltk.stem.porter.PorterStemmer()

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

stop = set(stopwords.words('english'))

#dataset = pd.read_csv('dataset1.csv',encoding='latin1')

#finalList=[]

'''for m in range (0,10):
    review = re.sub('[^.a-zA-Z]', ' ', dataset['story'][m])
    #review = re.sub(r'[^\w\s]', '', review)
    #print(review)
    str(review)
    #review.decode('utf-8')
    text=[]
    tokens_pos=[]
    ps=PorterStemmer()
    stop_words=set(stopwords.words("english"))
    for sent in sent_tokenize(review):
        
        tokenizer = TreebankWordTokenizer() 
        tokenizer.tokenize(sent) 
        
        x=word_tokenize(sent)
        tokens_pos.append(pos_tag(x))
        #print(tokens_pos)
        #print(type(tokens_pos))
        stemmed_sent=[]
        stemmed_sent2=[]
        #notallowed=[',',']','[','(',')','!'.':','"']
        for j in tokens_pos:
            for i in j:
                if(i[0] in stop_words):
                    j.remove(i)
        #text.append(tokens_pos)
            #else:
             #   stemmed_sent2.append(ps.stem(j[0]))
        for i in x:
            #i=ps.stem(i)
            if(i in stop_words):
                x.remove(i)
            else:
                stemmed_sent.append(ps.stem(i))
                #print(pos_tag(x))
        #text.append(stemmed_sent2)
    finalList.append(tokens_pos)
print(finalList)'''

def remove_stop_words(sentences) :
    tokenized_sentences = []
    for sentence in sentences :
        tokens = []
        split = sentence.lower().split()
        for word in split :
            if word not in stop :
                try :
                   
                    tokens.append(porter.stem(word))
                except :
                    tokens.append(word)
        
        tokenized_sentences.append(tokens)
    return tokenized_sentences

def remove_stop_words_without_lower(sentences) :
    tokenized_sentences = []
    for sentence in sentences :
        tokens = []
        split = sentence.split()
        for word in split :
            if word.lower() not in stop :
                try :
                   
                    tokens.append(word)
                except :
                    tokens.append(word)
        
        tokenized_sentences.append(tokens)
    return tokenized_sentences

def posTagger(tokenized_sentences) :
    tagged = []
    for sentence in tokenized_sentences :
        tag = nltk.pos_tag(sentence)
        tagged.append(tag)
    return tagged

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    #if "," in text: text = text.replace(",\"","\",")

    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    #text = text.replace(",","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names
def ner(sample):
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)



    entity_names = []
    for tree in chunked_sentences:
    # Print results per sentence
    # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))
    print (entity_names)
    return len(entity_names)

def thematicFeature(tokenized_sentences) :
    word_list = []
    for sentence in tokenized_sentences :
        for word in sentence :
            try:
                word = ''.join(e for e in word if e.isalnum())
                #print(word)
                word_list.append(word)
            except Exception as e:
                print("ERR")
    counts = Counter(word_list)
    number_of_words = len(counts)
    most_common = counts.most_common(10)
    thematic_words = []
    for data in most_common :
        thematic_words.append(data[0])
    print(thematic_words)
    scores = []
    for sentence in tokenized_sentences :
        score = 0
        for word in sentence :
            try:
                word = ''.join(e for e in word if e.isalnum())
                if word in thematic_words :
                    score = score + 1
                #print(word)
            except Exception as e:
                print("ERR")
        score = 1.0*score/(number_of_words)
        scores.append(score)
    return scores

def upperCaseFeature(sentences) :
    tokenized_sentences2 = remove_stop_words_without_lower(sentences)
    #print(tokenized_sentences2)
    upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    scores = []
    for sentence in tokenized_sentences2 :
        score = 0
        for word in sentence :
            if word[0] in upper_case :
                score = score + 1
        scores.append(1.0*score/len(sentence))
    return scores

def cuePhraseFeature(sentences) :
    pass

def sentencePosition(paragraphs):
    scores = []
    for para in paragraphs:
        sentences = split_into_sentences(para)
        print(len(sentences))
        if len(sentences) == 1 :
            scores.append(1.0)
        elif len(sentences) == 2 :
            scores.append(1.0)
            scores.append(1.0)
        else :
            scores.append(1.0)
            for x in range(len(sentences)-2) :
                scores.append(0.0)
            scores.append(1.0)
    return scores

def tfIsf(tokenized_sentences):
    scores = []
    COUNTS = []
    for sentence in tokenized_sentences :
        counts = collections.Counter(sentence)
        isf = []
        score = 0
        for word in counts.keys() :
            count_word = 1
            for sen in tokenized_sentences :
                for w in sen :
                    if word == w :
                        count_word += 1
            score = score + counts[word]*math.log(count_word-1)
        scores.append(score/len(sentence))
    return scores

def similar(tokens_a, tokens_b) :
    #Using Jaccard similarity to calculate if two sentences are similar
    ratio = len(set(tokens_a).intersection(tokens_b))/ float(len(set(tokens_a).union(tokens_b)))
    return ratio



def similarityScores(tokenized_sentences) :
    scores = []
    for sentence in tokenized_sentences :
        score = 0;
        for sen in tokenized_sentences :
            if sen != sentence :
                score += similar(sentence,sen)
        scores.append(score)
    return scores

def properNounScores(tagged) :
    scores = []
    for i in range(len(tagged)) :
        score = 0
        for j in range(len(tagged[i])) :
            if(tagged[i][j][1]== 'NNP' or tagged[i][j][1]=='NNPS') :
                score += 1
        scores.append(score/float(len(tagged[i])))
    return scores

def text_to_vector(text):
    words = WORD.findall(text)
    return collections.Counter(words)

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def centroidSimilarity(sentences,tfIsfScore) :
    centroidIndex = tfIsfScore.index(max(tfIsfScore))
    scores = []
    for sentence in sentences :
        vec1 = text_to_vector(sentences[centroidIndex])
        vec2 = text_to_vector(sentence)
        
        score = get_cosine(vec1,vec2)
        scores.append(score)
    return scores


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def numericToken(tokenized_sentences):
    scores = []
    for sentence in tokenized_sentences :
        score = 0
        for word in sentence :
            if is_number(word) :
                score +=1 
        scores.append(score/float(len(sentence)))
    return scores


def namedEntityRecog(sentences) :
    counts = []
    for sentence in sentences :
        count = entity2.ner(sentence)
        counts.append(count)
    return counts


def sentencePos(sentences) :
    th = 0.2
    minv = th*len(sentences)
    maxv = th*2*len(sentences)
    pos = []
    for i in range(len(sentences)):
        if i==0 or i==len((sentences)):
            pos.append(0)
        else:
            t = math.cos((i-minv)*((1/maxv)-minv))
            pos.append(t)

    return pos


def sentenceLength(tokenized_sentences) :
    count = []
    maxLength = sys.maxsize
    for sentence in tokenized_sentences:
        num_words = 0
        for word in sentence :
                num_words +=1
        if num_words < 3 :
            count.append(0)
        else :
            count.append(num_words)
    
    count = [1.0*x/(maxLength) for x in count]
    return count

def executeForAFile(filename,output_file_name,cwd) :
    
    os.chdir(cwd+"/articles")
    file = open(filename, 'r')
    text = file.read()
    paragraphs = para_reader.show_paragraphs(filename)
    print(paragraphs)
    print("Number of paras : %d", len(paragraphs))
    sentences = split_into_sentences(text)
    text_len = len(sentences)
    sentenceLengths.append(text_len)
    
    tokenized_sentences = remove_stop_words(sentences)
    tagged = posTagger(remove_stop_words(sentences))

    thematicFeature(tokenized_sentences)
    print(upperCaseFeature(sentences))
    print("LENNNNN : ")
    print(len(sentencePosition(paragraphs)))

    tfIsfScore = tfIsf(tokenized_sentences)
    similarityScore = similarityScores(tokenized_sentences)

    print("\n\nProper Noun Score : \n")
    properNounScore = properNounScores(tagged)
    print(properNounScore)
    centroidSimilarityScore = centroidSimilarity(sentences,tfIsfScore)
    numericTokenScore = numericToken(tokenized_sentences)
    #namedEntityRecogScore = namedEntityRecog(sentences)
    sentencePosScore = sentencePos(sentences)
    sentenceLengthScore = sentenceLength(tokenized_sentences)
    thematicFeatureScore = thematicFeature(tokenized_sentences)
    sentenceParaScore = sentencePosition(paragraphs)


    featureMatrix = []
    featureMatrix.append(thematicFeatureScore)
    featureMatrix.append(sentencePosScore)
    featureMatrix.append(sentenceLengthScore)
    #featureMatrix.append(sentenceParaScore)
    featureMatrix.append(properNounScore)
    featureMatrix.append(numericTokenScore)
    #featureMatrix.append(namedEntityRecogScore)
    featureMatrix.append(tfIsfScore)
    featureMatrix.append(centroidSimilarityScore)

filename = "article1"
filenames = []
output_file_list = []
cwd = os.getcwd()
WORD = re.compile(r'\w+')

precision_values = []
recall_values = []
Fscore_values = []
sentenceLengths = []

for file in os.listdir(cwd+"/articles"):
    filenames.append(file)
    output_file_list.append(file)


for x in range(len(filenames)):
    executeForAFile(filenames[x],output_file_list[x],cwd)
