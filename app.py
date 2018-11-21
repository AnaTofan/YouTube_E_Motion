from flask import Flask, render_template, url_for,abort
from Category import Category
from pymongo import  MongoClient

dbClient = MongoClient()
db = dbClient.LatestTechnologies
CATEGORIES={}
for collection in db.collection_names():
    collection_name=collection
    if collection_name=="Printing3D":
        name= " 3D Printing"
    else:
        name=''.join(map(lambda x: x if x.islower() else " "+x,collection_name))
    logo_path="../static/images/" + collection + "T.jpg"
    category=Category(collection_name,name, logo_path)
    CATEGORIES[collection_name]=category
    print(category.name)


app=Flask(__name__)
# CATEGORIES ={
#     'AI':{
#     'name': 'Artificial Intelligence',
#     'no_comments': 100
# }
#}

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',categories=CATEGORIES)

@app.route('/category/<key>')
def category(key):
    category=CATEGORIES.get(key)
    if not category:
        abort(404)
    return render_template('report.html', category=category)

if __name__ == '__main__':
    app.run(debug=True)


#https://code.tutsplus.com/tutorials/templating-with-jinja2-in-flask-essentials--cms-25571