export POSTGRES_HOST=${POSTGRES_HOST:='db'}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD:='password'}
export POSTGRES_USER=${POSTGRES_USER:='postgres'}
export POSTGRES_DB=${POSTGRES_DB:='tracker_db'}

docker-compose build  --no-cache --build-arg POSTGRES_PASSWORD=${POSTGRES_PASSWORD} --build-arg POSTGRES_DB=${POSTGRES_DB} \
						--build-arg POSTGRES_USER=${POSTGRES_USER} db
docker-compose up -d db
docker-compose build  --no-cache --build-arg POSTGRES_PASSWORD=${POSTGRES_PASSWORD} --build-arg POSTGRES_DB=${POSTGRES_DB} \
						--build-arg POSTGRES_USER=${POSTGRES_USER} --build-arg POSTGRES_HOST=${POSTGRES_HOST} tracker
docker-compose up -d tracker
