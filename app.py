from flask import Flask, render_template, request, jsonify
import os
import requests
import urllib2
import pymongo
from PIL import Image
import sys
import imagehash
import subprocess
from bs4 import BeautifulSoup
import json

client = pymongo.MongoClient('localhost', 27017)
db = client.hackny
movieTitle = ''
app = Flask(__name__, static_url_path = "", static_folder = "")


def computeHash(filename):
  return str(imagehash.average_hash(Image.open(filename)))

def query(target):
  minWeight = 1000000
  minImage = ''
  for obj in db.images.find():
    # compute the hamming weight of the bitwise xor
    try:
      weight = bin(int(target, 16) ^ int(obj['ahash'], 16)).count('1')

      if minWeight > weight:
        minWeight = weight
        minObj = obj
        print target, obj['ahash'], obj['filename']
    except:
      pass

  return minObj


def foursquare(query):
  url = 'https://api.foursquare.com/v2/venues/search?client_id=SIUVLZ0OHAY5YW1W4F0GCDD4XUP0ILCPU3UYXVQBY0SDWSIZ&client_secret=5AKY4AQ0I4F3OOBSB0IWOSFZNJDAPYMU0BEPF0MGIWJPINQ1&v=20130815&ll=40.7,-74&query=%s' % query

  data = urllib2.urlopen(url)
  soup = BeautifulSoup(data)
  dictionary = json.loads(str(soup))
  places = dictionary['response']['venues']
  lines = []
  for place in places:
    name = place['name']
    location = place['location']
    try:
      city = location['city']
    except:
      city = "NYC"
    try:
      state = location['state']
    except:
      city = "NY"

    line = '<li><h3>%s</h3>Distance: %s,%s,%s</li>' % (name, location['distance'], city, state)
    lines.append(line)
  return '<ul>' + ''.join(lines) + '</ul>'




@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")


@app.route('/file', methods=['GET'])
def filePicker():
  return render_template("file.html")

@app.route('/query/', methods=['GET'])
def echo():
  #ret_data = {"value": "Result: "+str(movieTitle)}
  ret_data = {"value": foursquare('steak')}
  return jsonify(ret_data)

@app.route('/aviary', methods=['GET'])
def aviary():
  return render_template("aviary.html")


@app.route('/upload', methods=['POST'])
def upload():
  global movieTitle
  url = request.form['url']
  print url
  file_name = 'temp.'+url.split('/')[-1].split('.')[-1]
  u = urllib2.urlopen(url)
  f = open(file_name, 'wb')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  print "Downloading: %s Bytes: %s" % (file_name, file_size)

  file_size_dl = 0
  block_sz = 8192
  while True:
      buffer = u.read(block_sz)
      if not buffer:
          break

      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      #print status,

  f.close()
  frameObj = query(computeHash(file_name))
  movieTitle = frameObj['title']
  frame = frameObj['filename']
  print(frame)
  subprocess.call(['cp','-f','./images/'+frame,'./temp2.jpg'])
  render_template('file.html')
  return "200"

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.debug = True
  app.run(host='0.0.0.0', port=port)
