# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
This is designed to be a generalized function for base conversions, between arbitrary bases.

There are three accepted input formats
1) if the input is a plain integer or float, then it is assumed to be base 10

2) otherwise, the input should be a 2-element tuple, and the second element of the tuple will explicitly
specify the base.
If 2<= base <= 36, the first tuple element may be numeric or string.

3) however, it is always acceptable to use a list to store the components of the first element of the tuple
we will use BigEndian convention to agree with conventional reading order 

Decimals are permitted, as numeric, string, or list elements 

For base 2-36, user can get list-style output by setting prefOut='List'
"""
def baseConvert(numIn, baseOut=10, prefOut='noList', threshold=1e-12, chatty=False):
    
    import math
    import numbers
    errorString = ''
    isInt = True
    isNeg = False
    #First we have to verify and sort input, and requested output
    if baseOut < 2 or repr(type(baseOut)) != "<class 'int'>" :
        errorString = 'illegal baseOut: ' + baseOut
        return errorString
    #everything gets converted to base 10 intermediary
    if isinstance(numIn, numbers.Number):
        num10 = numIn
        intVal = math.floor(num10)
        if intVal != num10:
            isInt = False
            decVal = num10 % 1 
        if num10 < 0:
            isNeg = True
            num10 *= -1
    else: #2-element tuple
        try:
            baseIn = numIn[1]
            if baseIn < 2 or repr(type(baseIn)) != "<class 'int'>" :
                errorString = 'illegal baseIn: ' + baseIn
                return errorString
        except:
            errorString = 'numIn must be numeric type or 2-element tuple; invalid entry: ' + str(numIn)
            return errorString
            
        #now that we have validated numIn[1], we convert all forms of numIn[0] into a charList
        valIn = numIn[0]
        if chatty:
            print(valIn)
        if isinstance(valIn, numbers.Number):
            valIn = str(valIn)
        valIn = list(valIn)
        if '.' in valIn:
            #if decimal, deal with edge cases, otherwise acknowledge float
            if valIn.count('.') > 1:
                errorString = 'illegal list: too many decimals'
                return errorString
            elif valIn.index('.') == (len(valIn) - 1):
                valIn = valIn[:-1]
            else:
                isInt = False
        #check for neg, we don't deal with that til very end
        if valIn[0] == '-':
            isNeg = True
            valIn = valIn[1:]
        #at this point, we have a list of either char representations of numbers,
        #actual numbers, or alphabetical char representations:
        #we need to convert all of these to real numbers...
        #if using alpha-chars to represent b11-36, convert to numbers
        if chatty:
            print (valIn)
        for ePos, eItem in enumerate(valIn):
            if (not isinstance(eItem, numbers.Number)) and eItem != '.':
                if eItem.isnumeric():
                    valIn[ePos] = int(eItem)
                else:
                    valIn[ePos] = ord(eItem.upper())-54
        if chatty:
            print(valIn)
        #now we split into <=2 sublists, based on float status
        if isInt:
            intIn = valIn
        else:
            intIn = valIn[:valIn.index('.')]
            decIn = valIn[valIn.index('.')+1:]
        #now we convert intIn to base10
        intVal = 0
        thisPow = 1
        for i in range(-1, -1*len(intIn)-1, -1):
            intVal += intIn[i]*thisPow
            thisPow *= baseIn
        num10 = intVal
        #likewise for any decimal component
        if not isInt:
            decVal = 0.0
            thisPow = 1.0
            for i in range(len(decIn)):
                thisPow /= baseIn
                decVal += thisPow*decIn[i]
            num10 += decVal
    #and this is our validated base10 value!
    if chatty:
        print(num10 * (not isNeg) )
    #now lets make the outVal
    if baseOut == 10:
        return num10
    else:
        #for the integer component,
        #initialize empty list based on maxPower, then fill in values using mods
        powList = [0]
        maxList = [1]
        maxVal = baseOut
        while maxVal <= intVal:
            powList.append(0)
            maxList.insert(0, maxVal)
            maxVal *= baseOut
        if chatty:
            print (maxList)
        thisPos = 0
        tempVal = intVal
        while thisPos < len(powList):
            powList[thisPos]=tempVal//maxList[thisPos]
            tempVal %= maxList[thisPos]
            thisPos += 1
        #apply same procedure to decimal component, to within tolerance of threshold
        outList = powList
        if not isInt:
            decList = []
            rem = num10%1
            divisor = 1.0 / baseOut
            while rem > threshold:
                decList.append(math.floor(rem/divisor))
                rem %= divisor
                divisor /= baseOut
            outList.append('.')
            outList+= decList
        if isNeg:
            outList.insert(0, '-')
        if baseOut > 36 or prefOut == 'List':
            return outList
        else:
            #if noList, any base over 10 gets autocast as string
            if baseOut > 10:
                for ePos, eVal in enumerate(outList):
                    if isinstance(eVal, numbers.Number):
                        if eVal >= 10:
                            outList[ePos] = chr(55+eVal)
                for ePos, eVal in enumerate(outList):
                    outList[ePos] = str(eVal)
                outString = "".join(outList)
                return outString
                #otherwise we need string cast for join, and then convert to numeric
            else:
                for ePos, eVal in enumerate(outList):
                    outList[ePos] = str(eVal)
                outString = "".join(outList)  
                if isInt:
                    outNum = int(outString)
                else:
                    outNum = float(outString)
                return outNum
                
                
                
            
            
            
    
            
            
        
    
    
    
    
    
    
    
    
    
    
    