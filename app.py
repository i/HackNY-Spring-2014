from flask import Flask, render_template, request
import os
import requests
import urllib2
import pymongo
from PIL import Image
import sys
import imagehash


client = pymongo.MongoClient('localhost', 27017)
db = client.hackny

app = Flask(__name__)


def computeHash(filename):
  return imagehash.average_hash(Image.open(filename))  

def query(target):
  target = str(target)
  minWeight = 1000000
  minImage = ''
  for obj in db.images.find():
    # compute the hamming weight of the bitwise xor
    
    weight = bin(int(target, 16) ^ int(obj['ahash'], 16)).count('1')

    if minWeight > weight:
      minWeight = weight
      minObj = obj

  return obj


@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")


@app.route('/file', methods=['GET'])
def filePicker():
  return render_template("file.html")


@app.route('/aviary', methods=['GET'])
def aviary():
  return render_template("aviary.html")


@app.route('/upload', methods=['POST'])
def upload():
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
      print status,

  f.close()
  frameObj = query(computeHash(file_name))
  movieTitle = frameObj['title']
  frame = frameObj['filename']
  

  return "200"

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.debug = True
  app.run(host='0.0.0.0', port=port)
