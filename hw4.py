# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
import math


def entropy(size, table):
    temp = []
    for each in table:
        if each not in temp:
            temp.append(each)
    count = [[term,table.count(term)] for term in temp]
    ret = 0
    for each in count:
        ratio = float(each[1])/float(size)
        ratio = round(ratio,3)
        ret -= ratio*math.log(ratio,2)
        ret = round(ret,3)
    return ret
    
def info_gain(size, data, index):
    table = []
    for each in data:
        table.append(each[index])
    #temp has all different items in the attribute
    temp = []
    for each in table:
        if each not in temp:
            temp.append(each)
    #count has each item's size
    count = [[p,table.count(p)] for p in temp]
    hold = []
    for each in temp:
        for term in data:
            if term[index] == each:
                hold.append(term[len(term)-1])
    ret = 0
    begin = 0
    for item in count:
        item_size = item[1]
        end = begin + item_size
        tab = hold[begin:end]
        ratio = float(item_size)/float(size)
        ratio = round(ratio,3)
        ret += ratio*entropy(item_size,tab)
        ret = round(ret,3)
        begin += item_size
    return ret
    

#Main Function
#get number of lines / number of training instances
num_lines = raw_input()
size = int(num_lines) - 1
#get attributes
temp = raw_input()
attribute = []
count = 0
for i in range(len(temp)):
    if temp[i] == ",":
        attribute.append(temp[count:i])
        count = i+1
attribute.append(temp[count:len(temp)])
#get rest training instances
data = []
for line in sys.stdin:
    data.append(line.strip("\n").split(","))
#select target table
target_tab = []
for each in data:
    target_tab.append(each[len(each)-1])
#get expected information
expected_info = entropy(size, target_tab)
#get each attribute's information gain
information_gain = []
for i in range(len(attribute)):
    if attribute[i] is attribute[len(attribute)-1]:
        break
    information_gain.append(info_gain(size, data, i))
#find index of the maximum information gain value
max_index = 0
for i in range(len(information_gain)):
    information_gain[i] = round(expected_info - information_gain[i],3)
    if information_gain[i] > information_gain[max_index]:
        max_index = i
#print attribute selection by information gain
print attribute[max_index]

split_info = []
for i in range(len(attribute) - 1):
    split_temp = []
    for each in data:
        split_temp.append(each[i])
    split_info.append(entropy(size,split_temp))

result = []
max_index = 0
for i in range(len(information_gain)):
    result.append(information_gain[i]/split_info[i])
    result[i] = round(result[i],3)
    if result[i] > result[max_index]:
        max_index = i
print attribute[max_index]