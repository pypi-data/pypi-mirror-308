import sqlite3

import os

class DefinitionUtils:
    baseRelationTypesMap = {
        'int': 'INTEGER',
        'float': 'REAL',
        'str': 'TEXT'
    }

    def determineTypeAsString(self, dataValue):
        if isinstance(dataValue, str):
            foundType = 'str'

        elif isinstance(dataValue, float):
            foundType = 'float'

        else:
            foundType = 'int'

        return foundType


    def createPreStoreFormat(self, fieldName:str, fieldData:int|float|str, whereToStoreFormatObject:dict):
        # 'str'
        deducedType = self.determineTypeAsString(dataValue=fieldData)

        if deducedType == 'str':
            # '' - add the string quotes to the data
            typedValue = f"'{fieldData}'"

        else:
            # int|float
            typedValue = fieldData

        # generate type-data object
        whereToStoreFormatObject[fieldName] = (self.baseRelationTypesMap[deducedType], typedValue)

        return

class MappingUtils:
    def __init__(self, pathToDatabase):
        self.pathToDatabase = pathToDatabase

        assert os.path.exists(self.pathToDatabase), "Database file not found"

    def getDatabaseConnection(self):
        # connect to the database
        return sqlite3.connect(self.pathToDatabase)
    
    def plainQueryExecutor(self, queryToExecute):
        # get connection
        databaseConnection = self.getDatabaseConnection()

        databaseConnection.execute(queryToExecute)

        databaseConnection.commit()

        databaseConnection.close()

        return
    
    def returnQueryExecutor(self, queryToExecute):
        # get connection
        databaseConnection = self.getDatabaseConnection()

        # store the results
        foundMatches = databaseConnection.execute(queryToExecute).fetchall()


        databaseConnection.close()

        return foundMatches
    

    def getRecordsFromDatabase(self, nameOfTable:str, listOfFieldsToInclude:list):
        # merged fields
        mergedFields = ", ".join(listOfFieldsToInclude)

        # query to get data from database
        # SELECT * FROM Employee;
        getQuery = f"SELECT {mergedFields} FROM {nameOfTable};"

        # print(getQuery)

        # [(23, 'Blessing'), (26, 'Believe'), (67, 'Sample')]
        resultsOfQuery = self.returnQueryExecutor(queryToExecute=getQuery)

        # print(resultsOfQuery)

        return resultsOfQuery
    
    
    def generateDatabaseRecognizedTypes(self, nameOfField:str, dataForField:int|str|float):
        if isinstance(dataForField, str):
            mappedTypeValue = f'{nameOfField}="{dataForField}"'

        else:
            mappedTypeValue = f'{nameOfField}={dataForField}'

        return mappedTypeValue
    

    def executeDataWipe(self, nameOfTable:str, conditions:list):
        # make sure all are mapped
        mappedDataAndTypes = [self.generateDatabaseRecognizedTypes(nameOfField=eachPair[0], dataForField=eachPair[1]) for eachPair in conditions]
        
        # conditions merged
        andedConditions = " AND ".join(mappedDataAndTypes)

        # generated query will look like -> DELETE FROM Student WHERE name="Sample" AND age=67;
        deleteQuery = f"DELETE FROM {nameOfTable} WHERE {andedConditions};"

        # print(deleteQuery)

        self.plainQueryExecutor(deleteQuery)

        return
        

    def executePurge(self, nameOfTable:str):
        # deletes everything in the table
        purgeQuery = f"DELETE FROM {nameOfTable};"

        self.plainQueryExecutor(purgeQuery)

        return
    
    def executeTableDrop(self, nameOfTable:str):
        # deletes the give table
        dropQuery = f"DROP TABLE {nameOfTable};"

        self.plainQueryExecutor(dropQuery)

        return
    

    def executeTableUpdate(self, nameOfTable:str, fieldLabelsList:list, fieldValuesList:list, primaryKeyMeta:tuple):
        # ['name="Grace"']
        typeMappedValuesList = [self.generateDatabaseRecognizedTypes(nameOfField=eachValue, dataForField=fieldValuesList[eachIndex]) for eachIndex, eachValue in enumerate(fieldLabelsList)]

        # merged replacements
        joinedReplacements = ", ".join(typeMappedValuesList)

        # key field name
        keyFieldName = primaryKeyMeta[0]

        formattedKeyValue = '"{}"'.format(primaryKeyMeta[1]) if isinstance(primaryKeyMeta[1], str) else primaryKeyMeta[1]

        # make the query - UPDATE Employee SET name="Bless" WHERE id=24;
        updateQuery = f'UPDATE {nameOfTable} SET {joinedReplacements} WHERE {keyFieldName}={formattedKeyValue};'

        # print(updateQuery)

        # make the changes to the database
        self.plainQueryExecutor(updateQuery)

        return


    
    def affirmThatTablesExist(self, databaseDefinition:dict):
        # {'Student': {'name': <class 'str'>, 'age': <class 'int'>}, 
        # 'Employee': {'id': <class 'int'>, 'name': <class 'str'>}}
        tableCreationQueryList = []

        # get type info
        typesMeta = DefinitionUtils().baseRelationTypesMap


        baseTypeRawTypeMap = {
            int: typesMeta['int'],
            str: typesMeta['str'],
            float: typesMeta['float']
        }


        for tableName, tableDefinition in databaseDefinition.items():
            # default fields have our unique id
            defaultFields = ['__rowid__ TEXT']

            # get the fields
            # {'name': <class 'str'>, 'age': <class 'int'>}
            tableFields = ["{} {}".format(eachFieldName, baseTypeRawTypeMap[eachFieldType]) for eachFieldName, eachFieldType in tableDefinition.items()]

            # combine
            combinedFields = defaultFields + tableFields

            # merge them
            mergedNamesAndTypes = ', '.join(combinedFields)

            # print(tableName, mergedNamesAndTypes)
            # Employee __rowid__ TEXT, id INTEGER, name TEXT

            # create a query
            # CREATE TABLE IF NOT EXISTS Student (__rowid__ TEXT, name TEXT, age INTEGER);
            tableCreationQuery = f"CREATE TABLE IF NOT EXISTS {tableName} ({mergedNamesAndTypes});"


            # print(tableCreationQuery)

            # create tables
            self.plainQueryExecutor(tableCreationQuery)

        return



    def writeDatabaseRecord(self, nameOfTable, dataMeta:dict):
        # collectors
        tableFieldsCollector  = []

        insertFields = []

        # print(dataMeta)

        for eachTableField, eachFieldMeta in dataMeta.items():
            # get the type : 'TEXT'
            fieldDatabaseType = eachFieldMeta[0]
            
            # 'name TEXT'
            nameAndType = f"{eachTableField} {fieldDatabaseType}"

            # print(nameAndType)

            # store
            tableFieldsCollector.append(nameAndType)

            insertFields.append(str(eachFieldMeta[1]))

        # merge them
        mergedNamesAndTypes = ','.join(tableFieldsCollector)

        mergedFieldNames = ','.join(insertFields)

        # print(mergedNamesAndTypes)

        # create write query
        # INSERT INTO Student VALUES ('9b63e0f0-231f-4b98-84c1-6ffbf26f8541','Bless',12);
        
        dataInsertQuery = f"INSERT INTO {nameOfTable} VALUES ({mergedFieldNames});"

        # print(dataInsertQuery)

        self.plainQueryExecutor(dataInsertQuery)

        return

