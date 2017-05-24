def loadDataSet():
	return [[1,3,4], [2,3,5], [1,2,3,5], [2,5]]

def CreateC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	return list(map(frozenset, C1))  # python3.X当中，map只返回一个可迭代的对象，因此需要用list(map(...))来替代

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can in ssCnt:
                    ssCnt[can] += 1
                else:
                    ssCnt[can] = 1
    numItems = len(list(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

dataSet = loadDataSet()
C1 = CreateC1(dataSet)
D = list(map(set, dataSet))
L1, supportData = scanD(D, C1, 0.5)
print(L1, '\n', supportData)