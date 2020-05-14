from collections import defaultdict
import heapq
from bitarray import bitarray


def encoding(freq):

    # freq.items()return list of tuples
    heap = [[weight, [char, '']]for char, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)  # lowest list
        right = heapq.heappop(heap)  # highest list
        for val in left[1:]:
            val[1] = '0'+val[1]
        for val in right[1:]:
            val[1] = '1'+val[1]
        heapq.heappush(heap, [left[0]+right[0]]+left[1:]+right[1:])

    # ignore summation of all occurance  #return list of list
    return heap[0][1:]


# open file
string = open('input_file.txt', 'r')

# string instead of object file
string = string.read()

# get freq foreach character
freq = defaultdict(int)
for char in string:
    freq[char] += 1
print(freq)

# apply huffman algo
huffmantree = encoding(freq)
# print(huffmantree)

# huffman dictionary used in encoding
huffman_dic = {l[0]: bitarray(str(l[1]))for l in huffmantree}

print('char !! code ')
for char, val in huffman_dic.items():
    print(char, val)


# encoding input file
encoded_text = bitarray()
encoded_text.encode(huffman_dic, string)

# we store data in bytes  (8 bits) so add padding in encoding && remove it from decoding
padding = 8-(len(encoded_text) % 8)

# save encoded binary file
with open('encoded_file.bin', 'wb') as en:
    encoded_text.tofile(en)

# generate output binary file
decoded_text = bitarray()
with open('encoded_file.bin', 'rb') as de:
    decoded_text.fromfile(de)

# remove padding
decoded_text = decoded_text[:-padding]


decoded_text = decoded_text.decode(huffman_dic)
decoded_text = ''.join(decoded_text)

f = open("outputfile.txt", "a")
f.write(decoded_text)
f.close()
