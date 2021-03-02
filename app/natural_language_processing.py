import refine_comments
import cluster
import nltk
from pymongo import  MongoClient
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import random
from nltk.corpus import movie_reviews
from nltk.tokenize import  PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer


def count_modal_words():
    client = MongoClient();
    db = client.LatestTechnologies
    modals=['can','could','may','might','must','will']
    for collection in db.collection_names():
        fdist=nltk.FreqDist([w.lower() for w in refine_comments.get_comments('CloudComputing')])
        for m in modals:
            print (collection + m+ ': ', fdist[m])

#A lot of times we have different variation of words based on their stems (which are root words) but the meaning of the word is unchanged(we are exposed to the risk of redundancy)
def stemming_words(comments):
    ps=PorterStemmer();
    stem_words=[]
    for word in comments:
        stem_words.append(ps.stem(word))

    return stem_words


#Labeling the part  of speech for every single word
def part_of_speech(comment_text):
  custom_sent_tokanizer = PunktSentenceTokenizer()
  tokenized = custom_sent_tokanizer.tokenize(comment_text)
  tagged=[]
  try:
     for i in tokenized:
          words=nltk.word_tokenize(i)
          tag=nltk.pos_tag(words)
          tagged.append(tag)
     return tagged
  except Exception as e:
              return []




#Chunking: group words into meaningful chunks: noun phrases-> next step on finding the meaning of a sentence:uses regex
#RB: regular adverb
def get_chunks(comment_text):
    tagged_text=part_of_speech(comment_text)
    chunkGram=r""""Chunk: {<RB.?>*<VB.?>*<NNP><NN>?} """

    chunkParser=nltk.RegexpParser(chunkGram)
    chunked=chunkParser.parse(tagged_text)
    return  chunked

def chink(comment_text):
    tagged_text=part_of_speech(comment_text)
    chinkGram = r""""Chunk: {<.*>+}
                                }<VB.?|IN|DT|TO>+{"""
    chinkParser = nltk.RegexpParser(chinkGram)
    chinked = chinkParser.parse(tagged_text)
    return chinked


#Named entity recognition
def recognize_named_entity(comment_text):
    tagged_text = part_of_speech(comment_text)
    named_ent=[]
    for tagged in tagged_text:
     namedEnt= nltk.ne_chunk(tagged,binary=True)
     named_ent.append(namedEnt)

    return named_ent

def lemmantize(comment_text):
    lemmantized=[]
    lemmantizer=WordNetLemmatizer
    for word in comment_text:
        lemmantized.append(lemmantizer.lemmatize(word,pos='n'))
    return lemmantized




def classify_text(comments):
    documents=[(list(movie_reviews.words(fileid)),category)
                for category in movie_reviews.categories()
                for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    comments=nltk.FreqDist(comments)
    word_features=list(comments.keys())[:3000]
    words=set(documents)
    features=[]
    words=set(movie_reviews.words('neg/cv000_29416.txt'))
    for w in word_features:
        features[w]=(w in words)
    feature_sets=[]
    return features



# words = generatewordvector.get_comments('SolarEnergy')
# print(stemming_words(words)


# words = generatewordvector.get_comments_text('SolarEnergy')
# print  (part_of_speech(words))

# print(part_of_speech2(generatewordvector.get_comments_text('MarsColoniza

# print(part_of_speech2(generatewordvector.get_comments_text('MarsColonization')))
# print(get_chunks(generatewordvector.get_comments_text('MarsColonization')))

#print(lemmantize(generatewordvector.get_comments('MarsColonization')))

#print(recognize_named_entity(generatewordvector.get_comments_text('MarsColonization')))
print(classify_text(refine_comments.get_comments('SolarEnergy')))