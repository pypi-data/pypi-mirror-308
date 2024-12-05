![](https://gracepeter.pythonanywhere.com/static/dstore/dst.png)

# How to start using `dstore`

Ready for use , with all BASIC (Create, Read, Update, Delete) operations are supported.

Developed by `Mutiibwa Grace Peter` [🔗](https://gracepeter.pythonanywhere.com/), `Tukasiima Blessing` (c) 2024

---
Report issues at [🔍 dstore-orm repo](https://github.com/GracePeterMutiibwa/dstore-orm/issues)

---
`dstore-orm`  is a Sqlite ORM that offers means of saving objects (dictionaries) to the database, making it applicable for less data intensive applications while hiding the complexities of database interactions.

- This `package` aims to make it so easy to get going with saving object structured data for small scale appliactions.

## `Getting started`
Install the package using;
``` python
pip install dstore-orm
```

## `Usage Guide`

1. Creating a `definitions` file

The **definitions file** should have an extension of `.dst`

```markdown
# Inside the the .dst file  you can add definitions like;

Student:[name=str, age=int]
```

- `No spaces` should exist between the name of the Table and the colon and the list of field names i.e.

```
Student : [name=str] is Invalid
       ^ ^ 
       | |

Such spaces are not valid
```

> ![Creating a `.dst` file](https://gracepeter.pythonanywhere.com/static/dstore/dstore-dst.svg)

- In the list of fields like `[name=str, age=int]` **no spaces** should exist between the `field name and the type`.

```
Student: [name = str, age=str]
              ^ ^
              | |
            Such spaces wont
            be recognized
```

---

- Above , `Student` is the name of the table and the list `[name=str]` is a definition of the fields the `Student` table will have


```markdown

# With many tables and many fields

Student:[name=str, age=int]

Color:[name=str, code=str]

```

Suppose the `details.dst` is located in a folder called `learn`

> Note: If the `dst` file is  put in a folder, that folder should exist. 

---


2. Creating a connection to the `database` in our python file or code via the `definitions` file.

```python

from dstore import SqliteORM


# path to definitions
definition_path = './learn/details.dst'

# connect to the definitions file
datase_connection = SqliteORM().connect(definition_path)
```

> Upon successfull connection; 
- The `definitions file` will be `created if its missing`.

- An `sqlite database file with the same name as the definitions file` will be created.

Get meta information about the database created using the `meta` and `definitions` attribute
```python

# display a list of tables as defined in the database
print(datase_connection.meta)

# display the structure of the databse tables
print(datase_connection.definitions)
```

**Note**: Before any operations can be done, ensure that there are `definitions` in your `definitions file` otherwise you `will get an error`.

---

# CRUD OPERATIONS

**Note**: Before any (Create, Read, Update, Delete) operation, a connection to the database must be created.

```python
from dstore import SqliteORM

# definitions
definition_path = 'learn/details.dst'

# create connection
databaseConnection = SqliteORM().connect(definition_path)
```

1. `Saving` objects to the database

> Before any saving operation, an object (`a dictionary`) with fields defined as in the `definitions` file is prepared.
---
![Object structure](https://gracepeter.pythonanywhere.com/static/dstore/dstore-object.svg)

- Keys (.i.e. name, age) of the object (dictionary) should match those defined in the definitions file.

- Data types for the values should match to i.e. `'John Doe'` is a string (`str`) and `12` is an integer (`int`)
---

```python
# an object
sampleObject = {
    'name': 'John Doe',
    'age': 12
}

# save
databaseConnection.save('Student', sampleObject)
```

2. `Reading` data from the database

```python

# fetch all records in `Student` table
data = databaseConnection.fetch("Student")

```

```python
# Get certain fields from the table
# i.e. get only the name field
data = databaseConnection.fetch("Student", ['name'])

print(data)
```

3. `Updating` records in the database
```python
databaseConnection.update("Student", ['age'], [17], ('name', 'John Doe'))
```

> Explanation
![How to update](https://gracepeter.pythonanywhere.com/static/dstore/dstore-update.svg)


|Section|Description|
|---|---|
|`Student`|Name of the table to update|
|`['age']`| A list of fields to replace, if they are `many the format is  ['age', 'name']`|
|`[17]`| The replace list containing values for the replace fields, note that the `order matters`, in case they are `many the format is [17, 'Red']`|
|`('name', 'John Doe')`| `'name'` - For all fields to replace, the name field value i.e. 'John Doe' will  be looked for, and wherever its found, `fields in that record will be updated with values in the replace list`. |

---



4. `Deleting` records from the database
> Deleting specific record
```python
# data record based on conditions
databaseConnection.delete("Student", [('id', 67)])
```

- `'Student'` - Is the table you want to delete from.

- [`('id', 67)`] - A list containing tuple indicating the fields to look for i.e. `id`, and in case they have the specified values i.e. `67` in the `id` field, then that field will be deleted.

> Deleting (`purging`) all records in a given table.

```python
# delete : all data in table but not the table.
databaseConnection.purge("Student")
```

5. Deleting the whole table from the database
```python
# delete table 'Student' from the database
databaseConnection.drop("Student")
```

**Note**;
- A `wrong table name will raise an error` (ensure the table actuall exists before deleting).

- Deleting the table `does not remove it from the definitions file`.

- Attempting to `save to the table after the table is deleted will re-create` the table.
