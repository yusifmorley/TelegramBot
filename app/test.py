
import functools
lis=[5,8,6,4,7]
def compare(x,y):
    return x-y

lis.sort(key=functools.cmp_to_key(compare))
print(lis)