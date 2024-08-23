# library imports
import flask 
import pickle
import traceback
import pandas as pd
import os
from flask import Flask, json, request, jsonify, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
import re
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import requests
from bs4 import BeautifulSoup
import validator

app = Flask(__name__)


gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]


# Function to check if a website contains fake news
def is_fake_news(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Modify the logic below based on the structure of the news website
        # Check for specific elements that might indicate fake news
        fake_news_keywords = [
            'unreliable', 'misleading', 'fake','false']

        for keyword in fake_news_keywords:
            if keyword in soup.get_text().lower():
                return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# Compare results with data
channels = ['Ary', 'Samaa', 'Bol', 'Geo News']
urls = {
    'Geo News': 'https://www.geo.tv/',
    'Ary': 'https://www.arynews.tv/en/',
    'Samaa': 'https://www.samaa.tv/',
    'Bol': 'https://www.bolnews.com/',
    'BBC News': 'https://www.bbc.com/',
    'Al Jazeera':'https://www.aljazeera.com/'
}
# Function to check if a URL is valid
def is_valid_url(url):
    if not validators.url(url):
        return False

    # Check for specific conditions in the URL (customize as needed)
    if not (url.startswith('') or url.startswith('h')):
        return False

    # Add more conditions to check for specific words or patterns
    invalid_words = ['gololol' 'goom', '8887']
    if any(word in url for word in invalid_words):
        return False

    return True

# API route for checking if news is fake or real
@app.route('/api/v1/check_news', methods=['POST'])
def check_news():
    try:
        data = request.get_json()
        url = data.get('url', '')

        if not url:
            return jsonify({"error": "Missing 'url' parameter"}), 400
        # Check if the URL is valid
        if not is_valid_url(url):
            return jsonify({"error": "Invalid URL"}), 400

        # Check if the news is fake or real
        if is_fake_news(url):
            result = {"prediction": "FAKE", "message": "The news is likely fake."}
        else:
            result = {"prediction": "REAL", "message": "The news is likely real."}

        return jsonify(result)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing the request."}), 500

# HTML route for the home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index',methods=['POST'])
def index():
    return render_template('index.html')

@app.route('/live')
def live():
    return render_template('live.html')

@app.route('/about')
def about():
    return render_template('about.html')
        
@app.route('/register')
def register():
    return render_template('register.html')

    int_features2 = [str(x) for x in request.form.values()]

    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
        
    

    

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root",'',"ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()


    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
                      

                      
    print(gmail_list1)
    if logu1 in gmail_list1:
        return render_template('register.html',text="This Username is Already in Use ")

    else:

                  
              

# Prepare SQL query to INSERT a record into the database.
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                  return render_template('register.html',text="Succesfully Registered")



@app.route('/login')
def login(): 
    return render_template('login.html')         
                      


@app.route('/logedin',methods=['POST'])
def logedin():
    
    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]


    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root","","ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()

    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
                      

                      
    print(gmail_list)
    

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()

    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
                    
                      
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))
    
    if gmail_list.index(logu)==password_list.index(passw):
        return render_template('index.html')
    else:
        return render_template('login.html',text='Use Proper Username and Password')
  
                                               

   


@app.route('/production')
def production(): 
    return render_template('index.html')

#path relative to working library

MODEL_PATH = os.path.join(app.root_path, 'model')

#importing moodel passive-aggressive-classifier
with open(f"{MODEL_PATH}/pac_model.pkl", 'rb') as f:
    classifier = pickle.load(f)
#import vectorizer
with open(f"{MODEL_PATH}/tfidf_vectorizer.pkl", 'rb') as f:
    tfidf_vectorizer = pickle.load(f)
#importing moodel LogisticRegression
with open(f"{MODEL_PATH}/lr_model2.pkl", 'rb') as f:
    classifiers = pickle.load(f)    
#html routes
def index():
    return render_template('index.html')

#fake news prediction
@app.route("/api/v1.0/analyze", methods=["POST"])
def invokeAnalyzer() :
    try:
        # assume all objects getting are json objects.
        body = request.get_json(force=True)

        # Validate that "title" and "body" fields are present
        if "title" not in body or "body" not in body or not body["title"].strip() or not body["body"].strip():
            return jsonify({"error": "Both 'title' and 'body' fields are required and cannot be empty."}), 400
        # print body
        article_title = body["title"]
        article_text = body["body"].lower()


        # vectorizer expects series as input
        text = pd.Series([article_text])

        tfidf_test = tfidf_vectorizer.transform(text)
        prediction = list(classifier.predict(tfidf_test)) [0]
        confidence = list(classifier.decision_function(tfidf_test)) [0]

        return jsonify({
            "title": article_title,
            "text": article_text,
            "prediction": prediction,
            "confidence": confidence
        })

    except:
        # returns
        return jsonify({
            "trace": traceback.format_exc()
        })
# runserver
if __name__ == "__main__":
    app.run()

