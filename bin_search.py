import math
array = [1,2,3,4,5,6,7,8,9,11,12,32,34,54,56,76,78,98,100]

def binary_search(numbers, value):
    lo = 0
    hi = len(numbers)
    
    while lo < hi:
        m = math.floor(lo + (hi-lo)/2)
        v = numbers[m]

        if v == value:
            return m
        if v > value:
            hi = m
        else:
            lo = m + 1

    return -1

res = binary_search(array, 2)
#print(res)