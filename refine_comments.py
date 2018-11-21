from pymongo import  MongoClient
from math import sqrt
import re
from nltk.corpus import stopwords,words
import enchant
from nltk.probability import *
from matplotlib import *
import matplotlib.pyplot as plt
from nltk.corpus import PlaintextCorpusReader
import nltk
import unicodedata





def get_words(text):

         words = re.compile(r'[^A-Z^a-z]+').split(text)
         return [word.lower() for word in words if word != '']



def get_word_counts(collection):
    dbClient = MongoClient()
    client =dbClient.LatestTechnologies
	videos = client[collection].find()
    all_comments_string = " "
    #set containing all the english stopwords
    stop = set(stopwords.words('english'))
    d=enchant.Dict("en_US")
    comment_text = []
    words=[]
    for video in videos:
        title=video['title']
        try:
           wc={}
            for comment in video['comments']:
                #eliminating stop word from comments and adding them to a list
                for i in comment['text'].lower().split():
                    if(i not in stop and d.check(i)):
                        all_comments_string = all_comments_string + " " + i
            words = get_words(title + ' ' + all_comments_string)
            for word in words:
                           wc.setdefault(word, 0)
                           wc[word] += 1
            return title, wc
        except KeyError as e:
         return title, {}



def generate_dataset(collection_name):
    apcount = {}
    wordcounts = {}
    client=MongoClient()
    client=getattr(client.LatestTechnologies,collection_name)
    video_ids=client.distinct("_id")
    no_items=client.count()





    title=" "
    for video_id in video_ids:

             title,wc = get_word_counts(collection_name, video_id)

             wordcounts[title] = wc
             for word, count in wc.items():
                 apcount.setdefault(word, 0)
                 if count > 1:
                      apcount[word] += 1

    wordlist = []
    for w, bc in apcount.items():
        frac=float(bc)/no_items
        if (frac>0.05):  wordlist.append(w)


    filename=collection_name+".txt"
    out = open(filename, 'w')
    out.write('Title')
    for word in wordlist: out.write('\t%s' % word)
    out.write('\n')
    for vtitle, wc in wordcounts.items():
         vtitle = vtitle.encode('ascii', 'ignore').decode('ascii')
         out.write(vtitle)
         for word in wordlist:
            if word in wc:
                out.write('\t%d' % wc[word])
            else:
                out.write('\t0')
         out.write('\n')

def get_comments_text(collection):
    dbClient = MongoClient()
    client = getattr(dbClient.LatestTechnologies, collection)
    comments = client.distinct("comments.text")
    all_comments_string = " "
    # set containing all the english stopwords
    stop = set(stopwords.words('english'))
    comms = []
    d = enchant.Dict("en_GB")
    f=enchant.Dict("fr_FR")

    for i in comments:
          all_comments_string = all_comments_string + i


    all_comments_string=''.join(char for char in unicodedata.normalize('NFC',all_comments_string) if char<='\uFFFF')

    comms = get_words(all_comments_string)
    for comm in comms:
        if(d.check(comm)==True and f.check(comm)==False ):
            all_comments_string = all_comments_string + comm + " "


    return all_comments_string

def get_comments(collection):
    dbClient=MongoClient()
    client = getattr(dbClient.LatestTechnologies, collection)
    comments=client.distinct("comments.text")
    all_comments_string = " "
	
    # set containing all the english stopwords
    stop = set(stopwords.words('english'))
    comms=[]
    d = enchant.Dict("en_GB")
    f = enchant.Dict("fr_FR")

    for i in comments:
          all_comments_string=all_comments_string + i

    all_comments_string = ''.join(
        char for char in unicodedata.normalize('NFC', all_comments_string) if char <= '\uFFFF')


    comms=get_words(all_comments_string)
    relevant_words=[]
    for comment in comms:
        if (comment not in stop and d.check(comment) and comment.__len__()>1 and f.check(comment)==False):
            relevant_words.append(comment)
    #print (relevant_words)
    return relevant_words


def get_comments_by_date(collection):
    dbClient=MongoClient()
    client = getattr(dbClient.LatestTechnologies, collection)
    comments = client.distinct("comments.text")
    stop = set(stopwords.words('english'))
    comms = []
    d = enchant.Dict("en_GB")
    f = enchant.Dict("fr_FR")
    individual_comments=[]
    for comm in comments:
        words=get_words(comm)
        comment=" "
        for word in words:
            if( d.check(word) and  f.check(word) == False):
                comment=comment+word+ " "

        individual_comments.append(comment)

    return individual_comments




def frequency_distribution(collection):
    relevant_words=get_comments(collection)
    fdist=FreqDist(samples=relevant_words)
    #fdist.plot(50)
    # plt.title(collection)
    # fdist.plot(50,cumulative=True)
    # print(fdist.hapaxes())
    text=nltk.Text(relevant_words)
    # print(text.collocations())

    #creates a list containing 50 most encountered words in the comments of a collection
    vocabulary = []
    for i in fdist.most_common(50):
       vocabulary.append(i[0])

    text.dispersion_plot(vocabulary)

    #creates a list containing only long words
    long_words=[word for word in relevant_words if len(word)>13]
    #creates a list of collocations: words that are often found together: they are resistant
    #to substitutions with  words that have similar meanings



def generate_text_file(collection):
    comments=get_comments_text(collection)
    filename = "comments_text_files/"+collection + ".txt"
    out = open(filename, 'w')
    out.write(comments)



def create_corpus(collection):
    corpus_root ="/home/ana/Desktop/E-motionPage2/comments_text_files"
    wordlists = PlaintextCorpusReader(corpus_root, '.*')
    #print(wordlists)

# def generate_dispersion_plot(collection):
    # dbClient = MongoClient()
    # client = getattr(dbClient.LatestTechnologies, collection)
    # videos = client.find().sort({title: 1})
    # for comment in videos['comments']:
    #     print (comment)


    # relevant_words = get_comments(collection)
    # fdist = FreqDist(samples=relevant_words)
    # text = nltk.Text(relevant_words)
    # vocabulary = []
    # for i in fdist.most_common(50):
    #     vocabulary.append(i[0])
    #
    # text.dispersion_plot(vocabulary)

# print(get_comments_by_date("SolarEnergy"))

generate_text_file("BionicLimbs")