from PIL import Image
from os import listdir
import sys
import pymongo
import imagehash

client = pymongo.MongoClient('localhost', 27017)
db = client.hackny
title = sys.argv[1]
path = sys.argv[2]


for img in listdir(path):
  ahash = imagehash.average_hash(Image.open(path + '/' + img))
  phash = imagehash.phash(Image.open(path + '/' + img))
  dhash = imagehash.dhash(Image.open(path + '/' + img))
  imghash = {
      "title": title,
      "ahash": str(ahash),
      "phash": str(phash),
      "dhash": str(dhash),
      "filename": img
      }

  # print imghash
  db.images.insert(imghash)


def usage():
  print "usage: hash_movie <movie title> <directory containing images>"
