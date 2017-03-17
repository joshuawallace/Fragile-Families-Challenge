a = [[1,2,3],[4,5,6],[7,8,9]]

b = [list(a[i]) for i in range(len(a))]

#print b

c = [line.pop(0) for line in a]
#a = [line[1:] for line in a]

#print a
#print b
#print c


import general_functions as generalf

a = [['1','NA','NA','NA','NA','NA','NA'],
    ['1','NA','NA','NA','NA','NA','NA'],
    ['1','NA','NA','NA','NA','NA','NA'],
    ['1','NA','NA','NA','NA','23','NA']]

#print a[0]
#print a[0][4]

b = generalf.remove_lines_with_all_NA(a)