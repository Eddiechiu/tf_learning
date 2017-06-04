import numpy as np 

dataMat = np.mat([[0,0,0,2,2],
                  [0,0,0,3,3],
                  [0,0,0,1,1],
                  [1,1,1,0,0],
                  [2,2,2,0,0],
                  [5,5,5,0,0],
                  [1,1,1,0,0]])

def ecludSim(inA, inB):
    return 1.0 / (1.0 + np.linalg.norm(inA - inB))
    
def pearsSim(inA, inB):
    if len(inA) < 3:
        return 1.0
    else:
        0.5 + 0.5 * np.corrcoef(inA, inB, rowvar = 0)[0][1]

def cosSim(inA, inB):
    num = float(inA.T * inB)
    denom = np.linalg.norm(inA) * np.linalg.norm(inB)
    return 0.5 + 0.5 * (num/denom)

def standEst(dataMat, user, simMeas, item):
    n = np.shape(dataMat)[1]
    simTotal = 0.0
    ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0: 
            continue
        # 注意np.nonzero的用法，其返回两个数组
        # 第一个数组记录非零元素的行位置，第二个数组记录非零元素的列位置（这里我们只需要行位置即可）
        overlap = np.nonzero(np.logical_and(dataMat[:,2].A>0, 
                                      dataMat[:,j].A>0)) [0]
        if len(overlap) == 0:
            similarity = 0
        else:
            similarity = simMeas(dataMat[overlap, item], dataMat[overlap, j])
        simTotal += similarity
        # ratSimTotal为了后面计算食物评分的估计值
        ratSimTotal += similarity * userRating 
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal
    
    
    
    
    
    
    
    
    