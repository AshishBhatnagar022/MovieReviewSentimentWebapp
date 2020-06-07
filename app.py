from __future__ import division,print_function
import sys
import os
import flask
from flask import Flask,redirect,url_for,render_template,request
from flask import Flask, Response, render_template, request

from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib.request
import cv2
from ast import literal_eval
import random
from urllib.request import urlopen
import re


app=Flask(__name__)




PEOPLE_FOLDER = os.path.join('static')

# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
# 
import json
from flask import jsonify
import pickle

model = pickle.load(open('model.pkl', 'rb'))
tokenizer=pickle.load(open('tranform.pkl','rb'))
from keras.preprocessing.sequence import pad_sequences
data1=pd.read_csv('dataset.csv')
NAMES=list(data1['original_title'])
# print(NAMES)

def url_to_image(url):
  image=""
  resp=""
  try:
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    url1=url
  except Exception as e:
    resp = urllib.request.urlopen("https://www.my24erica.com/assets/images/imdbnoimage.jpg")
    url1="https://www.my24erica.com/assets/images/imdbnoimage.jpg"
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

  return url1
@app.route('/')
def index():
  return render_template('index.html')
@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('autocomplete')
    app.logger.debug(search)
    return Response(json.dumps(NAMES), mimetype='application/json')
@app.route('/result',methods=['GET','POST'])
def result():
  # comment='comm'
  error=''
  # prediction=1
  if request.method == 'POST':
      movie_name=flask.request.form['autocomp']
      print("MOVIENAME",movie_name)

      comment = request.form['w3review']
      if comment=='' or movie_name=='':
        print("Empty string")
        error='Please enter movie name and review'
        # return redirect('/')

        return render_template('index.html',error=error)
      # elif movie_name not in data1['original_title']:
        # error='Movie not found in database'
        # return render_template('index.html',error=error)
      else:
        mainImg=data1[data1['original_title']==movie_name]['Poster'].values[0]
        # mainImg=url_to_image(mainImg)
        print("IIIIII",mainImg)
        # pass
        # movie_name=flask.request.form['autocomp']

        test_samples=[comment]
        test_sample_token=tokenizer.texts_to_sequences(test_samples)
        test_sample_tokens_pad=pad_sequences(test_sample_token,maxlen=200)
        prediction=model.predict(x=test_sample_tokens_pad)
       



       
        return render_template('result.html',comment=comment,prediction=prediction,mainImg=mainImg,movie_name=movie_name)




if __name__=='__main__':
    app.run(debug=True,threaded=False)
