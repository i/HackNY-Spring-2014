from PIL import Image
import sys
import imagehash
hash = imagehash.average_hash(Image.open(sys.argv[1]))
print 'ahash: ' + str(hash)

hash = imagehash.phash(Image.open(sys.argv[1]))
print 'phash: ' + str(hash)

hash = imagehash.dhash(Image.open(sys.argv[1]))
print 'dhash: ' + str(hash)
