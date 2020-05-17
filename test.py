from bitarray import bitarray
import sys
thisdict = {1: "1011", 2: "1101"}

huffman_dic = {x: bitarray(str(y))for x, y in thisdict.items()}

print(huffman_dic)