from collections import defaultdict
import heapq
from bitarray import bitarray
from PIL import Image
import csv
import json
import cv2
import numpy as np
import os
import pickle
import sys
import huffman_encoder

# help in storing pixels_freq


def storeData(thisdict, filename):
    if os.path.exists(filename):
        os.remove(filename)

    dbfile = open(filename, 'ab')
    # source, destination
    pickle.dump(thisdict, dbfile)
    dbfile.close()


def loadData(filename):
    dbfile = open(filename, 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db


with open('sample.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

path = json_object['path']
im = Image.open(path)
width, height = im.size  # get width and height
size = width*height
print("width of photo: ", width)
print("height of photo: ", height)
print("size: ", size)

pixels = list(im.getdata())

# get freq foreach character
freq = defaultdict(int)
for char in pixels:
    freq[char] += 1


# apply huffman algo
huffmantree = huffman_encoder.huffman_encoding(freq)


# huffman dictionary used in encoding
huffman_dic = {pixel[0]: pixel[1]for pixel in huffmantree}
storeData(huffman_dic, 'huff_dictionary')

huffman_dic = {x: bitarray(str(y))for x, y in huffman_dic.items()}
# encoding input file
encoded_text = bitarray()
encoded_text.encode(huffman_dic, pixels)

print(sys.getsizeof(encoded_text))
# we store data in bytes  (8 bits) so add padding in encoding && remove it from decoding
padding = 8-(len(encoded_text) % 8)

# save encoded binary file
with open('encoded_file.bin', 'wb') as en:
    encoded_text.tofile(en)


# decoding
huffman_dic = loadData('huff_dictionary')
huffman_dic = {x: bitarray(str(y))for x, y in huffman_dic.items()}

# generate output binary file
decoded_pixels = bitarray()
with open('encoded_file.bin', 'rb') as de:
    decoded_pixels.fromfile(de)


# remove padding
decoded_pixels = decoded_pixels[:-padding]
decoded_pixels = decoded_pixels.decode(huffman_dic)

val = decoded_pixels[len(decoded_pixels)-1]
while (len(decoded_pixels) != size):
    decoded_pixels.append(val)

decoded_pixels = np.reshape(decoded_pixels, (height, width))
cv2.imwrite("decodedimage.png", decoded_pixels)

arr3 = np.array(pixels, dtype='int8')
np.save('pixels.npy', arr3)
