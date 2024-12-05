import os

from .dstProcessor import DstUtils

from .relationalMapper import MappingUtils

from .relationalMapper import DefinitionUtils

import uuid


class SqliteORM:
    # will store the definitions
    definitions = {}

    # mapping language types to database types
    baseRelationTypesMap = {
        'int': 'INTEGER',
        'float': 'REAL',
        'str': 'TEXT'
    }

    def __init__(self):
        pass

    def prepareDatabaseFiles(self, pathToDstFile:str=None, pathToDb:str=None):
        # create the definitions file
        if not pathToDstFile is None:
            with open(pathToDstFile, 'w+') as dstFileHandle:
                pass
        
        # create the database file now
        if not pathToDb is None:
            with open(pathToDb, 'w+') as databaseHandle:
                pass

        return
    
    def getOutliers(self, baseFieldsList:list, customFieldsList:list):
        return list(set(customFieldsList) - set(baseFieldsList))
    
   

    def confirmTypeMatch(self, dataValuesList:list, dataTypesList:list):
        referenceTypesList = [type(eachDataValue) for eachDataValue in dataValuesList]

        return referenceTypesList == dataTypesList
    
    def delete(self, tableName:str, conditions:list):
        '''
        Delete a given record or number of records based on a list of conditions
        '''
        self.preExecutionChecks()

        assert isinstance(tableName, str), "Table name must of string type"

        assert tableName in self.definitions, "The table name specified does not exist"

        assert isinstance(conditions, list), "The conditions container has to be of type {}".format(type(list()))

        # conditions not empty
        assert len(conditions) > 0, "No conditions were found, if you wish to delete all data use the 'purge' method"

        # are tuples
        allTuplesList = [isinstance(eachCondition, tuple) for eachCondition in conditions]

        assert allTuplesList.count(True) == len(allTuplesList), "The conditions should be formatted as tuples -> ('field', value)"

        # all tuples are pairs
        allTuplesArePairs = [len(eachCondition) == 2 for eachCondition in conditions]

        assert allTuplesArePairs.count(True) == len(allTuplesArePairs), "All conditions should contain only one field and a value"

        # fields
        fieldsAreStrings = [isinstance(eachCondition[0], str) for eachCondition in conditions]

        assert fieldsAreStrings.count(True) == len(fieldsAreStrings), "For every condition, the field names should be of type {}".format(type(''))

        # field names exist
        allFieldNamesExist = [eachCondition[0] in self.definitions[tableName] for eachCondition in conditions]

        assert allFieldNamesExist.count(True) == len(allFieldNamesExist), "It appears like some field names in conditions dont exist"

        # values
        valueTypesAreValid = [isinstance(eachCondition[1], str) | isinstance(eachCondition[1], int) | isinstance(eachCondition[1], float) for eachCondition in conditions]

        assert valueTypesAreValid.count(True) == len(valueTypesAreValid), "Supported types only include strings, integers and floating point numbers"

        # field types match
        fieldTypesMatchList = [isinstance(eachCondition[1], self.definitions[tableName][eachCondition[0]]) for eachCondition in conditions]

        assert fieldTypesMatchList.count(True) == len(fieldTypesMatchList), "Ensure that for each condition, the value specified matches the type of the field"

        # make the deletion
        MappingUtils(pathToDatabase=self.dbPath).executeDataWipe(nameOfTable=tableName, conditions=conditions)

        return

    def purge(self, tableName:str):
        '''
        Deletes all the records in the table and not the table itself
        '''
        self.preExecutionChecks()

        assert isinstance(tableName, str), "Table name must of string type"

        assert tableName in self.definitions, "The table name specified does not exist"

        # execute the purge
        MappingUtils(pathToDatabase=self.dbPath).executePurge(nameOfTable=tableName)

        return
    
    def drop(self, tableName:str):
        '''
        Deletes the table itself from the database
        '''

        self.preExecutionChecks()

        assert isinstance(tableName, str), "Table name must of string type"

        assert tableName in self.definitions, "The table name specified does not exist"

        # execute the purge
        MappingUtils(pathToDatabase=self.dbPath).executeTableDrop(nameOfTable=tableName)

        return


    def update(self, tableName:str, fieldList:list, replaceList:list, primaryKey:tuple):
        """
        Update given fields of the database with other values based on a chosen key
        """
        self.preExecutionChecks()

        assert isinstance(tableName, str), "Table name must of string type"

        assert tableName in self.definitions, "The table name specified does not exist"

        tableFieldList = list(self.definitions[tableName].keys())

        # non empty lists
        assert len(fieldList) > 0 and len(replaceList) > 0, "Check your field and value containers, either or both appears empty"

        # check if replacement fields exist
        allFieldsExist = [eachFieldName in tableFieldList for eachFieldName in fieldList]

        # all fields exist
        assert allFieldsExist.count(True) == len(allFieldsExist), "Fields {} are invalid".format(self.getOutliers(tableFieldList, fieldList))

        # same sizes
        assert len(fieldList) == len(replaceList), "Size of both the fields and value containers should match"

        # data types list
        dataTypesList = [self.definitions[tableName][eachFieldLabel] for eachFieldLabel in fieldList]

        # ensure that the data types match the field types
        assert self.confirmTypeMatch(dataValuesList=replaceList, dataTypesList=dataTypesList) is True, "Type assignments for the fields dont match"

        # primary key
        assert isinstance(primaryKey, tuple), "Primary key definition should be a tuple and not {}".format(type(primaryKey))

        assert len(primaryKey) > 0, "The primary key definition is invalid"

        assert len(primaryKey) == 2, "The primary key definition should contain the field name and the reference data"

        # check if that field exists
        assert primaryKey[0] in self.definitions[tableName], "Primary key field name not found in table definition"

        # Primary: ('name', 'Bless')
        # print('Primary:', primaryKey)

        # should not be part of replacing fields
        # Relaxed rules
        # assert not primaryKey[0] in fieldList, "Primary key field name {} should not be part of the fields to replace".format(primaryKey[0])

        primaryKeyValueDataType = self.definitions[tableName][primaryKey[0]]

        # type of search value
        assert isinstance(primaryKey[1], primaryKeyValueDataType), f"The primary key data should be of type {primaryKeyValueDataType}"

        # we can replace
        MappingUtils(pathToDatabase=self.dbPath).executeTableUpdate(nameOfTable=tableName, fieldLabelsList=fieldList, fieldValuesList=replaceList, primaryKeyMeta=primaryKey)

        return
    
    def fetch(self, tableName:str, dataFields:list=None):
        '''
        Retrieves a the available records from a given table based on the field list provided
        `dataFields` - Is a list but it can be ommitted 
        '''
        self.preExecutionChecks()

        assert isinstance(tableName, str), "Table name must of string type"

        assert tableName in self.definitions, "The table name specified does not exist"

        if dataFields is None:
            # {'id': <class 'int'>, 'name': <class 'str'>} -> ['id', 'name']
            tableFields = list(self.definitions[tableName].keys())

        else:
            # check if its a list
            assert isinstance(dataFields, list), "The data fields container should be type <class 'list'>"

            assert len(dataFields) > 0, "The data fields container provided appears to be empty"

            # print(dataFields)
            # [True, False]
            allFieldsAreValid = [eachField in self.definitions[tableName] for eachField in dataFields]

            # print(allFieldsAreValid)
            assert allFieldsAreValid.count(True) == len(allFieldsAreValid), "Check your fields, its seems like fields -> {} are invalid".format(self.getOutliers(list(self.definitions[tableName].keys()), dataFields))

            tableFields = dataFields.copy()


        # get records
        foundRecords = MappingUtils(pathToDatabase=self.dbPath).getRecordsFromDatabase(nameOfTable=tableName, listOfFieldsToInclude=tableFields)

        return foundRecords

    
    def preExecutionChecks(self):
        # check if there are definitions
        assert len(self.definitions) > 0, "No table definitions detected, please define some and try again"

        return



    def save(self, tableName:str, dataObject:dict):
        # tables should be defined exist
        self.preExecutionChecks()

        assert isinstance(tableName, str), "Table name must of string type"

        assert isinstance(dataObject, dict), "Data format not valid"

        # check if the table name exists in the definitions
        assert tableName in self.definitions, "The table name specified does not exist"

        # Student {'age': 67, 'name': 'Sample'}
        # print(tableName, dataObject)

        # provided keys
        # ['name', 'age']
        providedKeys =  list(dataObject.keys())

        # ['name', 'age']
        internalKeys = list(self.definitions[tableName].keys())

        # print(providedKeys, internalKeys)

        # confirm that fields are the same
        assert sorted(providedKeys) == sorted(internalKeys), f"Provided data has unknown fields, data should be of format {self.definitions[tableName]}"

        # primary key of id
        idOfRecord = str(uuid.uuid4())

        # each row name, mapped to : database type and value
        fieldsAndTypes = {
            '__rowid__': ('TEXT', f"'{idOfRecord}'")
        }

        for eachFieldName, eachDataValue in dataObject.items():
            # get the type information from the definitions
            requiredType = self.definitions[tableName][eachFieldName]

            assert isinstance(eachDataValue, requiredType), f"The data value '{eachDataValue}' should be of type {requiredType}"


            # deduce type and create pre-store format object
            DefinitionUtils().createPreStoreFormat(
                fieldName=eachFieldName,
                fieldData=eachDataValue,
                whereToStoreFormatObject=fieldsAndTypes
            )
        
        # {'__rowid__': ('TEXT', "'9b63e0f0-231f-4b98-84c1-6ffbf26f8541'"), 'name': ('TEXT', "'Bless'"), 'age': ('INTEGER', 12)}
        # print(fieldsAndTypes)

        # save to database
        MappingUtils(pathToDatabase=self.dbPath).writeDatabaseRecord(nameOfTable=tableName, dataMeta=fieldsAndTypes)

        return idOfRecord
    






    def extractLinesFromFile(self, pathOfFile):
        with open(pathOfFile, "r") as dataHandle:
            readData = dataHandle.readlines()

            # 'Student:[name=str, age=int]', 'Employee:[id=int, name=str]'
            withoutNewLines = [eachLine.strip() for eachLine in readData]

        return withoutNewLines

    
    
    def draftSqliteDbPath(self, dstFilePath:str):
        # extract the name of the database

        # ./details, '.dst'
        fullPath, _ = os.path.splitext(dstFilePath)

        # relational database to store the data
        absolutePath = fullPath + '.db'

        return absolutePath

    def connect(self, pathOfDefinitionFile:str):
        # validate its a string
        assert isinstance(pathOfDefinitionFile, str), "Path to databse definition has to be string"

        # ensure the database has valid path length
        assert len(pathOfDefinitionFile) >= 5, "Path to the database definition appears invalid consider checking it"

        # check if the database folder and the format
        # ('s', '.dst')
        _, fileExtension = os.path.splitext(pathOfDefinitionFile)

        assert fileExtension == '.dst', f"The extension '{fileExtension}' of the database definition is invalid"

        # check if the database exists
        databaseDefinitionExists = os.path.exists(pathOfDefinitionFile)


        # get the folder that should contain the database
        databaseDefinitionFolder = os.path.dirname(pathOfDefinitionFile)


        # print(databaseDefinitionFolder)
        
        # make sure the folder to contain the database exists
        assert os.path.exists(databaseDefinitionFolder), f"The path '{databaseDefinitionFolder}' meant to have the definitions file does not exist"


        # path to sqlite database
        self.dbPath = self.draftSqliteDbPath(pathOfDefinitionFile)

        # create the definitions file if its missing
        if databaseDefinitionExists is False:
            self.prepareDatabaseFiles(pathToDstFile=pathOfDefinitionFile, pathToDb=None)

        else:
            pass

        
        # create the database file itself if its missing
        if os.path.exists(self.dbPath) is False:
            self.prepareDatabaseFiles(pathToDstFile=None, pathToDb=self.dbPath)

        else:
            pass


        # load the data from the dst file
        definitionLines = self.extractLinesFromFile(pathOfDefinitionFile)

        # 
        # possible classes or tables
        self.meta = []


        for eachDefinitionLine in definitionLines:
            # process the definition line
            classLabel, classAttributes = DstUtils().processDstLine(eachDefinitionLine)

            if classLabel is None:
                pass

            else:
                # check if the definition exists twice
                assert not classLabel in self.definitions, "Duplicate table names exist"


                # upon connecting : it stores the different classes and the 
                self.definitions[classLabel] = classAttributes

                self.meta.append(classLabel)


        # ensure that the tables exist
        MappingUtils(pathToDatabase=self.dbPath).affirmThatTablesExist(
            databaseDefinition=self.definitions
        )


        return self








