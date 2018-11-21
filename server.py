from flask import Flask, request,current_app, send_from_directory,render_template, Response, abort
import json
from categoriesClass import Category

app=Flask(__name__)
CATEGORIES=[]
cat1=Category('Artificial Intelligence','ArtificialIntelligence','/static/images/ArtificialIntelligenceT.jpg')
cat2=Category('Big Data','BigData','/static/images/BigDataT.jpg')
CATEGORIES.append(cat1)
CATEGORIES.append(cat2)

@app.route('/')
def root():
     return current_app.send_static_file('index.html')
    
    

@app.route('/categories')
def getCategoryList():
    mockCategories=[]
    for category in CATEGORIES:
        mockCategories.append(category.logo)
    return Response(json.dumps(mockCategories)), 200
    
    
@app.route('/categories/<id>')
def getCategory(id):
    mockCategories=[]
    for category in CATEGORIES:
        json_format={'name':category.name, 'collection':category.collection,'logo_path':category.logo}
        mockCategories.append(json_format)
    if len([c for c in mockCategories if c['collection'] == id]):
             return Response(json.dumps([c for c in mockCategories if c['collection'] == id][0])), 200
    else:
        abort(404)
    
if __name__ == "__main__":
    app.run(debug=True)