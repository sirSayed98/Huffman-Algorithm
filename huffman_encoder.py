import heapq
from collections import defaultdict


def huffman_encoding(freq):

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


def Build_dic(pixels):
    freq = defaultdict(int)
    for char in pixels:
        freq[char] += 1
    return freq
