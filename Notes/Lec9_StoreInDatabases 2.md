# Databases

## To Run For Both:

```shell
scrapy crawl spiderName -o outputfile.csv > log.txt 
```

To install SQL server on linux: `sudo apt-get install mysql-server`

To install SQL connector on linux: `pip install mysql-connector-python`

<https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html>

## Store Data in SQL

```shell
cd books_crawler2
scrapy crawl booksData4_SQL -o items.csv > log.txt
# > log.txt redirects printed statements(for debugging purpose) to log.txt, not necessary
# -o items.csv specifies where data is stored
# after data are stored into items.csv, close() function will transfer data into MySQL DB
```
```python
def close(self, reason):
    csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
    print('debug, target file: ', csv_file)
    mydb = SQL.connect(host='localhost', user='root', password='password', database='booksDB')
    cursor = mydb.cursor()
    with open(csv_file) as data_file:
        csv_data = csv.reader(data_file, delimiter=',')
        row_count = 0
        for row in csv_data:
            if row_count != 0:
                query = ("INSERT IGNORE INTO books_table "
                         "(rating, product_type, upc, title) "
                         "VALUES (%s, %s, %s, %s)")
                cursor.execute(query, row)
                row_count += 1
                print('debug: total row added = ', row_count)

                mydb.commit()
                cursor.close()
                mydb.close()
```

To install MongoDB on linux: 

```shell
sudo apt-get install mongodb
sudo apt-get update
sudo service mongodb start
mongo		# Enter Mongo Shell
sudo pip install pymongo		# install for python
```

Details see `./booksCrawler_MongoDB`.

In `pipelines.py`,

```python
import scrapy
from pymongo import MongoClient
class MongoDBPipeline(object):

    def __init__(self):
        self.connection = MongoClient(
            'localhost',
            27017
        )
        db = self.connection['books']
        self.collection = db['products']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
```

In `Books.py`, nothing changes.

In `settings.py`,

```python
ITEM_PIPELINES = {
   'booksCrawler_MongoDB.pipelines.MongoDBPipeline': 300,
}
# Specify where items are going to (MongoDBPipeline i.e. the class in pipeline.py).
```



