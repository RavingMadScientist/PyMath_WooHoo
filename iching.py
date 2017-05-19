# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:07:04 2017

@author: legitz7
"""

"""
This function utilizes the digits of a time.monotonic() call (P3)
to perform a traditional I Ching reading based on the yarrow stalk method

the final 10 digits of the time call, prepended with the final 2 digits of a successive call,
 are converted to base-49, 44, 40, 36, and 32 

There are 6 iterations of the primary loop, each corresponding to a "line"

For each iteration, the line will be a sum of three numbers, or readings.
The first reading is calculated as:
(1 + (b49[-i]-1) % 4 + 1 + (48-b49[-i] - 1 ) % 4 + 1) // 4 , ->3 if 1
then, if this value is 9, we drop to base 40 for the second reading, otherwise base 44
repeat
then drop either 8 or 4, and repeat again
sum the values 

as indicated in Wilhelm's translation, Bollingen edition  
"""


def iChing(inString = None, dictOut = False):
    import time
    import math
    import mathRoutines
    inTime = time.monotonic()
    inTime = str(inTime).split('.')
    inTime = inTime[0][-1] + inTime[1]
    appendTime = time.monotonic()
    appendTime = str(appendTime)
    inTime = appendTime[-2:] + inTime
    inTime = int(inTime)
    if inString is not None:
        wordSum = 0
        for word in inString.split(' '):
            for ePos, eChar in enumerate(word):
                wVal = int(ord(eChar)* math.pow(128, ePos))
                wordSum +=  wVal
    print (inTime)
    print (wordSum)
    inTime += wordSum
    listDict = {}
    for i in [49,44,40,36,32]:
        listDict[i] = mathRoutines.baseConvert(inTime, i, prefOut='List')
    #print (listDict)
        listDict['raw']=[]
        listDict['lines']=[]
    for j in range(-1, -7, -1):
        thisBase = 49
        read1 = 3 + (listDict[thisBase][j] - 1) % 4 + (thisBase - listDict[thisBase][j] - 2) % 4
        if read1 == 5:
            val1 = 3
        else:
            val1 = 2
        thisBase -= read1

        read2 = 3 + (listDict[thisBase][j] - 1) % 4 + (thisBase - listDict[thisBase][j] - 2) % 4
        if read2 == 4:
            val2 = 3
        else:
            val2 = 2
        thisBase -= read2

        read3 = 3 + (listDict[thisBase][j] - 1) % 4 + (thisBase - listDict[thisBase][j] - 2) % 4
        if read3 == 4:
            val3 = 3
        else:
            val3 = 2
        listDict['raw'].append([val1, val2, val3])
        listDict['lines'].append(sum(listDict['raw'][-1]))
    #print (listDict)
    imString = """"""
    for k in range(-1, -7, -1):
        switchme = listDict['lines'][k]
        if switchme == 6:
            imString += """---x---"""
        elif switchme == 7:
            imString += """-------"""
        elif switchme == 8:
            imString += """--- ---"""
        elif switchme == 9:
            imString += """---o---"""
        imString += '\n'
    print(imString)
    listDict['img'] = imString
    if dictOut:
        return listDict
    else:
        return listDict['lines']
        
    