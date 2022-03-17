import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from scrape_mars import scrape


app = Flask(__name__)


@app.route('/')
def index():
    conn = 'mongodb://localhost:27017'

    client = pymongo.MongoClient(conn)

    db = client.mars_db
    
    mars = list(db.mars_info.find())[0]
    
    return render_template('index5.html', mars=mars)


@app.route('/scrape')
def scraper():
    conn = 'mongodb://localhost:27017'

    client = pymongo.MongoClient(conn)

    db = client.mars_db
    
    mars_info_dictionary = scrape()
    
    db.mars_info.update_one({}, {"$set": mars_info_dictionary}, upsert=True)
    
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)