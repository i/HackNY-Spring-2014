from PIL import Image
from os import listdir
import sys
import pymongo
import imagehash

client = pymongo.MongoClient('localhost', 27017)
db = client.hackny
title = sys.argv[1]
path = sys.argv[2]

print 'title: ' + title
print 'path: ' + path

for img in listdir(path):
  print img
  h = imagehash.average_hash(Image.open(path + '/' + img))
  imghash = {
      "title": title,
      "hash": str(h)
      }

  # print imghash
  db.images.insert(imghash)


def usage():
  print "usage: hash_movie <movie title> <directory containing images>"
