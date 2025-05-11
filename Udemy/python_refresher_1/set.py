myset={3,5,6,7}

myset.discard(5)  # removes 5 from the set
print(myset)

myset.pop()  # removes and returns an arbitrary element from the set
print(myset)

myset.clear()  # removes all elements from the set
print(myset)

myset.add(7)  # adds 7 to the set
print(myset)

myset.update({3,4,5}) # adds multiple elements to the set
print(myset)