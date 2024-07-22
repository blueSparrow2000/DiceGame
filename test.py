class A():
    def __init__(self,i):
        self.a = i

el = [A(i) for i in range(3)]

gg = set([el[0],el[0],el[1]])

for ent in list(gg):
    print(ent.a)

# for i in range(2):
#     el.remove(el[i])
#
# print(len(el))