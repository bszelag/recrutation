# test_db task

### Prerequisites
* python3.6, virtualenv
* **version with creating database**
  * mysql
  * docker
  * ```bash
	   cd recrutation/task_0
	   git clone git@github.com:datacharmer/test_db.git
	   mv employees_wo_titles.sql test_db/

	```

### Install requirements
```bash
make venv
. .venv/bin/activate
make install
```

### Remove old databases and create new ones:
* default envs:
	```bash
	export DB_HOST=${DB_HOST:=0.0.0.0}
	export DB_USER=${DB_USER:=root}
	export DB_PASSWORD=${DB_PASSWORD:=mysql-pass}
	export DB_NAME=${DB_NAME:=employees}
	
	export DEST_DB_HOST=${DEST_DB_HOST:=0.0.0.0}
	export DEST_DB_USER=${DEST_DB_USER:=root}
	export DEST_DB_PASSWORD=${DEST_DB_PASSWORD:=mysql-pass}
	export DEST_DB_NAME=${DEST_DB_NAME:=employees_2}
	```
* using default envs:
	```bash
	. create_new_db.sh
	```
* if you want to use custom env, then please export it before running create_new_db.sh script

### Copy titles from first database (employees) to second (employees_2)
```bash
python copy_titles_data.py
```

### Tests
* style check
  ```bash
  make style
  ```
* functional test
  ```bash
  make test
  ```  

### Script profiling **old version**
I decided to use cProfile to check how long it takes to perform copying titles from one database to another.

Result: 6499 function calls (6331 primitive calls) in **2.445 seconds**

5 most time consuming funtions:
```bash
   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    2.445    2.445 copy_titles_data.py:27(main)
        1    0.000    0.000    2.399    2.399 copy_titles_data.py:20(copy_titles)
        2    0.000    0.000    2.377    1.189 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:171(execute)
        2    0.000    0.000    2.377    1.189 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:309(_query)
        2    2.377    1.188    2.377    1.188 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/connections.py:220(query)

```

Results show that the most time consuming function is copy_titles from main. But this is not surprising - copy_titles executes 4 commands:
* saving titles from employees database to file
* commiting command described above
* loading data to employees_2 database using LOAD DATA INFILE (this function is specially designed to insert rows fast)
* commiting command described above

and they are actually creating the whole program.

#### LOAD DATA INFILE  **old version**
I decided to use *LOAD DATA INFILE* function because according to [mysql documentation](https://dev.mysql.com/doc/refman/5.7/en/insert-optimization.html) this is the best option to insert many rows into a table.
It also do not require to remember that data, which prevents from trying to load about 500 000 rows in memory.



### Changes to adjust script to working on different servers
I decided to use simple *SELECT* and *INSERT*  queries. To make it more efficient I try to get and insert x rows at a time.
To get the *x* value, I:
* fetched *max_allowed_packet* value from destination database
* prepared query length (without any data)
* prepared max row's length (50 for title, 10 for date, 10 for other date, 11 for max id number)
* counted x with formula: (*max_allowed_packet*-*query_length*) // *max_row_length*

#### Profiling results
* Time execution increased twice, to ~5s
* ```bash
	 7065 function calls (6897 primitive calls) in 5.020 seconds
	```
* Ordered by cumulative time (per function) - TOP 5
	```bash
   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    5.020    5.020 copy_titles_data.py:39(main)
        1    0.318    0.318    4.969    4.969 copy_titles_data.py:23(copy_titles)
       22    0.000    0.000    4.500    0.205 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:171(execute)
       22    0.000    0.000    4.495    0.204 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:309(_query)
       22    3.814    0.173    3.814    0.173 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/connections.py:220(query)
       22    0.000    0.000    0.448    0.020 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:143(_do_get_result)
       22    0.000    0.000    0.448    0.020 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:345(_get_result)
       22    0.448    0.020    0.448    0.020 {method 'store_result' of '_mysql.connection' objects}
       22    0.000    0.000    0.233    0.011 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:348(_post_get_result)
       22    0.000    0.000    0.232    0.011 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/cursors.py:319(_fetch_row)
       12    0.232    0.019    0.232    0.019 {method 'fetch_row' of '_mysql.result' objects}
       10    0.000    0.000    0.146    0.015 copy_titles_data.py:20(commit_changes)
       10    0.146    0.015    0.146    0.015 {method 'commit' of '_mysql.connection' objects}
        2    0.000    0.000    0.049    0.025 copy_titles_data.py:15(__init__)
        2    0.000    0.000    0.049    0.024 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/__init__.py:81(Connect)
        2    0.042    0.021    0.046    0.023 /home/ja/recrutation/task_0/.venv/lib/python3.6/site-packages/MySQLdb/connections.py:42(__init__)


	```
#### Conclusion	
As we can see most of the time is consumed by mysqlDB cursor's methods: execute, query, getting results.

In case of further optimization I should consider:
* changing current *LIMIT* rows value to bigger (we could assume that most of the titles are saved on less than 50 chars, same with the id)
* special MySQL queries optimised for inserting many rows

