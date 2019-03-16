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

### Script profiling
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

#### LOAD DATA INFILE 
I decided to use *LOAD DATA INFILE* function because according to [mysql documentation](https://dev.mysql.com/doc/refman/5.7/en/insert-optimization.html) this is the best option to insert many rows into a table.
It also do not require to remember that data, which prevents from trying to load about 500 000 rows in memory.



