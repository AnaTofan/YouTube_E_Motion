import sentiment_mod as s
import refine_comments as gwv
from pymongo import MongoClient, ASCENDING
import pprint

list=[]
client=MongoClient()
db=client.LatestTechnologies
# for collection in db.collection_names():
print("printing..")
for item in db.BionicLimbs.find(projection={'_id':False,'comments.date':True,'comments.text':True}):
    if item.get('comments') is not None:
        for comment in item.get('comments'):
                  if comment.get('text') is not None or comment.get('date') is not None:
                      sublist=[]
                      sublist.append(comment.get('date'))
                      sublist.append(comment.get('text'))
                      list.append(sublist)


list=sorted(list, key=lambda x: x[0])




list2=[]

# comments = gwv.comments_query("BionicLimbs")
for comment in list:
     sentiment_value, confidence=s.sentiment(comment[1])
     if confidence>0.8:
           sub = []
           #print ("Statement: "+comment[1],'\n'+ "Sentiment value is: "+ sentiment_value)
           sub.append(comment[0])
           sub.append(comment[1])
           sub.append(sentiment_value)
           list2.append(sub)


cate=0
cate2=0
#pprint.pprint(list2)
for comment in list2:
    if comment[2].__eq__('pos'):
            cate=cate+1
    else:
        cate2=cate2+1

print (cate , cate2)