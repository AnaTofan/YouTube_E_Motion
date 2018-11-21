from pymongo import  MongoClient
from math import sqrt
import re
import cluster
import refine_comments
from PIL import Image,ImageDraw



refine_comments.generate_dataset("SolarEnergy")
videotitles,words,data=cluster.readfile('SolarEnergy.txt')
rdata=cluster.rotatematrix(data)
wordclust=cluster.hcluster(data)
cluster.drawdendrogram(wordclust,labels=words,jpeg='SolarEnergyWC.jpg')


client=MongoClient();
db=client.LatestTechnologies
#for collection in db.collection_names():
    # filename=collection+".txt"
    # dendogram_name=collection+".jpg"
    # generatewordvector.generate_dataset(collection)
    # videotitles, words, data = cluster.readfile(filename)
    # clust = cluster.hcluster(data)ss
    # cluster.drawdendrogram(clust, videotitles, jpeg=dendogram_name)
    #generatewordvector.frequency_distribution(collection)
    #generatewordvector.generate_text_file(collection)
    #generatewordvector.create_corpus(collection)


#generatewordvector.frequency_distribution("ElectricCars")
#generatewordvector.create_corpus("ElectricCars")
#cluster.printclust(clust, labels=videotitles)
#cluster.drawdendrogram(clust,videotitles,jpeg='CloudComputing.jpg')
refine_comments.generate_dispersion_plot("SolarEnergy")