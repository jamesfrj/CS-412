import sys

#apriori algorithm, retrun Fk
def apriori(candidate, min_supp):
    ret = []
    #for loop to select items satisfy s are over minimum support
    for i in range(len(candidate)):
        if candidate[i][1] >= min_supp:
            ret.append(candidate[i])
    return  ret

#search data base to find candidate set
def candidate(frequent, input):
    temp_array = []
    update = []
    frequent.sort()
    #double for loop to find all possible n-k itemset
    for i in range(len(frequent)):
        for temp in range(len(frequent)):
            curr = frequent[i][0]
            nxt =  frequent[temp][0]
            if i != temp:
                update = list(set(curr+nxt))
                update.sort()
                if update not in temp_array:
                    if len(update) != 0 and len(update) == len(curr)+1:
                        temp_array.append(update)
    count = []
    hold = []
    #double for loop to find occurance of each itemset
    for item in input:
        for term in temp_array:
            if set(term).issubset(item):
                count.append(term)
                if term not in hold:
                    hold.append(term)
    hold.sort()
    ret = [(term,count.count(term)) for term in hold]
    return ret

#discover closed patterns of given data, sub-itemset pruning
def closed_pattern(freq_pattern):
    ret = []
    for each in freq_pattern:
        ret.append(each)
    #hold index of items that should be pruned
    cal = []
    #double for loop to compare each item
    for i in range(len(ret)):
        curr_item = ret[i][0]
        curr_count = ret[i][1]
        for j in range(len(ret)):
            nxt_item = ret[j][0]
            nxt_count = ret[j][1]
            if i != j:
                #determine if exist superset with same support
                if set(nxt_item).issubset(curr_item) and nxt_count == curr_count:
                    if j not in cal:
                        cal.append(j)
    cal.sort(reverse=True)
    #for loop to delete items should be pruned
    for del_index in cal:
        del ret[del_index]
    ret.sort()
    return ret

#discover max pattern of given data
def max_pattern(freq_pattern):
    ret = []
    for each in freq_pattern:
        ret.append(each)
    #hold index of items that should be pruned
    cal = []
    #double for loop to compare each item
    for i in range(len(ret)):
        curr_item = ret[i][0]
        curr_count = ret[i][1]
        for j in range(len(ret)):
            nxt_item = ret[j][0]
            nxt_count = ret[j][1]
            if i != j:
                #determine if exist superset with same support
                if set(nxt_item).issubset(curr_item):
                    if j not in cal:
                        cal.append(j)
    cal.sort(reverse=True)
    #for loop to delete items should be pruned
    for del_index in cal:
        del ret[del_index]
    ret.sort()
    return ret

#Main Function
#get minimum support
min_supp = int(raw_input())
#get input
input = []
for line in sys.stdin:
    input.append(line.split())
#get number of transactions
size = len(input)
#find occurance of each item
temp = []
count = []
for i in range(size):
    for j in input[i]:
        if j not in temp:
            temp.append(j)
        count.append(j)
temp.sort()

#get C1
C1 = [([item],count.count(item)) for item in temp]
#prune items under minimum support
F = apriori(C1, min_supp)
freq_pattern = []
#while loop for apriori algorithm
while len(F) != 0:
    freq_pattern += F
    C = candidate(F, input)
    F = apriori(C, min_supp)

#mined frequent pattern of given data
freq_pattern.sort(key=lambda item: (-item[1], item[0]))
for (key,value) in freq_pattern:
    print(str(value)+" ["+" ".join(item for item in key)+"]")
#print empty line
print ""

#mined closed pattern based on found frequent pattern
closed_pattern = closed_pattern(freq_pattern)
closed_pattern.sort(key=lambda item: (-item[1], item[0]))
for (key,value) in closed_pattern:
    print(str(value)+" ["+" ".join(item for item in key)+"]")
#print empty line
print "" 

#mined max pattern based on found frequent pattern
max_pattern = max_pattern(freq_pattern)  
max_pattern.sort(key=lambda item: (-item[1], item[0]))
for (key,value) in max_pattern:
    print(str(value)+" ["+" ".join(item for item in key)+"]")

