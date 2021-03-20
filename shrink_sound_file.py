import sys
import numpy as np
import scipy.io.wavfile


def distance(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))


def converged(arr1, arr2):
    for i in range(len(arr1)):
        if not np.array_equal(arr1[i][0],arr2[i][0]):
            return False
    return True


def findClosestCentroid(sound, centroidsWithSerial):
    closest=-1
    closestDistance=9999999
    counter = 0
    for cent in centroidsWithSerial:
        distance2 = distance(cent[0],sound)
        if distance2 < closestDistance:
            closestDistance=distance2
            closest=counter
        counter+=1
    return closest,closestDistance


def getAvgFromCluster(sortToClusters,cent):
    data = sortToClusters[cent[1]]
    if not data:
        return cent[0]
    avg = np.mean(data, axis=0)
    avg[0]=round(avg[0])
    avg[1] = round(avg[1])
    return avg


def getCentroidsString(centroidsWithSerial):
    str=""
    for cent in centroidsWithSerial:
        str += cent[0].__str__() + ","
    str = str[:-1]
    return str


def resetDictionaryValues(dict):
    for x in dict:
        dict[x]=[]


toCalculateLoss = True
f = open("output.txt", "w")
f.close()
sample = sys.argv[1]
centroids = sys.argv[2]
fs, y = scipy.io.wavfile.read(sample)
soundArray = np.array(y.copy())
centroids = np.loadtxt(centroids)
counter = 0
centroidsWithSerial = []
CentroidsWithSerialCopy =[]
for cent in centroids:
    centroidsWithSerial.append([cent,counter])
    CentroidsWithSerialCopy.append([np.array((1,1)), counter])
    counter+=1
sortToClusters={}
for cent in centroidsWithSerial:
    sortToClusters[cent[1]]=[]
counter = 0
totalLoss=0

while (not converged(centroidsWithSerial, CentroidsWithSerialCopy)) & (counter < 30):
    # make a copy of current list
    CentroidsWithSerialCopy = []
    for cent in centroidsWithSerial:
        CentroidsWithSerialCopy.append(cent.copy())
    # sort each sound particle to closest centroid & find loss:
    for sound in soundArray:
        closestCentroid,loss = findClosestCentroid(sound, centroidsWithSerial)
        totalLoss+=loss**2
        sortToClusters[closestCentroid].append(sound)
    # calculate new centroids as avg:
    for cent in centroidsWithSerial:
        cent[0] = getAvgFromCluster(sortToClusters,cent)
    # print new centroids to output.txt:
    printLine = "[iter " + str(counter) + "]:" + getCentroidsString(centroidsWithSerial)
    print(printLine)
    f = open("output.txt", "a")
    f.write(printLine+"\n")
    f.close()
    # reset clusters
    resetDictionaryValues(sortToClusters)
    # calculate loss
    if toCalculateLoss:
        avgLoss = totalLoss/len(soundArray)
        print("[iter " + str(counter) + "] avg loss: " + str(avgLoss))

    counter += 1
    totalLoss = 0

""""
# export sound file
result = []
for sound in soundArray:
    closestCentroid = findClosestCentroid(sound,centroidsWithSerial)
    for cent in centroidsWithSerial:
        if closestCentroid[0] is cent[1]:
            result.append(cent[0])
print(soundArray)
scipy.io.wavfile.write("compressed.wav", fs, np.array(result, dtype=np.int16))
"""