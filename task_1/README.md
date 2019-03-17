# task_1

## Prerequisites
* python3.6
* docker, docker-compose

## Environment variables
```bash
export POSTGRES_HOST=${POSTGRES_HOST:='db'}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD:='password'}
export POSTGRES_USER=${POSTGRES_USER:='postgres'}
export POSTGRES_DB=${POSTGRES_DB:='tracker_db'}
```

## Execute with default settings
```bash
. run_all.sh
```

## Example usage
```bash
curl http://<host>:<port>/item -H "Content-Type: application/json" POST -d "{\"name\":\"<name>\",\"value\":<value>,\"external_id\":\"<external_id>\"}"
curl http://<host>:<port>/item -H "Content-Type: application/json" POST -d "{\"name\":\"<name>\",\"value\":<value>,\"external_id\":\"<external_id>\"}" --cookie "cart_id=<cart_id>"
```

## Tests
* prerequisites
  ```bash
	 export POSTGRES_DB
	 export POSTGRES_USER
	 export POSTGRES_PASSWORD
	 export POSTGRES_HOST_ADDRESS (default value: 127.0.0.1)
  ```
* style check
  ```bash
  make style
  ```
* api test
  ```bash
  make test
  ```  
