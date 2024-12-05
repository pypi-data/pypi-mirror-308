import re

class DstUtils:
    def processDstLine(self, dstLine:str):
        #  : 'Student:[name=str, age=int]'
        # matches the name of the class and the types
        dataPattern = r"^([A-Za-z]+):\[(.+)\]"

        # extract the text
        # [('Student', 'name=str, age=int')]
        searchResult = re.findall(dataPattern, dstLine)

        # will store the class details
        nameOfClass = None

        classMeta = None

        if len(searchResult) == 1:
            # get the sole result
            # ('Student', 'name=str, age=int')
            firstResult = searchResult[0]

            # get the class name
            # 'Student'
            nameOfClass = firstResult[0]

            # list of acceptable types
            acceptableTypes = {'str':str, 'int':int, 'float':float}

            # get the names and the types
            # 'name=str, age=int'
            namesAndTypeString = firstResult[1]

            # [('name', 'str'), ('age', 'int')]
            foundMatches = re.findall(r"([A-Za-z]+)=([A-Za-z]+)", namesAndTypeString)

            # those that match
            confirmedMatches = [eachPair for eachPair in foundMatches if eachPair[1] in acceptableTypes]

            if len(confirmedMatches) > 0:
                # create the class attribute types object
                # {name:int}
                classMeta = { eachConfirmedPair[0]:acceptableTypes[eachConfirmedPair[1]] for eachConfirmedPair in confirmedMatches}

            else:
                pass

            # print(nameOfClass, "has", confirmedMatches)

            # foundTypes[namesAndTypeString]

        else:
            pass


        return nameOfClass, classMeta