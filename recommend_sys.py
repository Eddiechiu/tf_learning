import numpy as np 

dataMat = np.mat([[4,4,0,2,2],
                  [4,0,0,3,3],
                  [4,0,0,1,1],
                  [1,1,1,2,0],
                  [2,2,2,0,0],
                  [1,1,1,0,0],
                  [5,5,5,0,0]])

def ecludSim(inA, inB):
    return 1.0 / (1.0 + np.linalg.norm(inA - inB))

# 皮尔逊相似度计算，使用corrcoef计算相似系数矩阵，可以消除输入变量inA和inB的量纲差异
def pearsSim(inA, inB):
    if len(inA) < 3:
        return 1.0
    else:
        0.5 + 0.5 * np.corrcoef(inA, inB, rowvar = 0)[0][1]

# 余弦相似度，也可以消除输入向量的量纲
def cosSim(inA, inB):
    num = float(inA.T * inB)
    denom = np.linalg.norm(inA) * np.linalg.norm(inB)
    return 0.5 + 0.5 * (num/denom)

# 计算user吃过的其它所有菜与item的相似度
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
        overlap = np.nonzero(np.logical_and(dataMat[:,item].A>0, 
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
    
def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=standEst):
    # 找到此用户没有评分的菜，所以取列，也就是[1]
    unratedItem = np.nonzero(dataMat[user,:].A==0)[1]
    if len(unratedItem) == 0:
        print('everything is rated')
    itemScores = []
    for item in unratedItem:
        estimatedScore = standEst(dataMat, user, simMeas, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda x: x[1], reverse=True)[:N]

print(recommend(dataMat, 4, N=1))