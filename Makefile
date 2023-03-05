up:
	docker-compose up -d --build
down:
	docker-compose down
run:
	python manage.py runserver 0.0.0.0:5000

migrate:
	python manage.py makemigrations itology
	python manage.py migrate itology
d-migrate:
	docker-compose exec web python manage.py makemigrations itology
	docker-compose exec web python manage.py migrate itology

admin:
	python manage.py createsuperuser
d-admin:
	docker exec -it $(docker ps -aqf "name=^movie") python manage.py createsuperuser

ps:
	docker-compose ps
d-ps:
	docker ps

logs-web:
	docker logs --tail 50 --follow --timestamps itology
logs-db:
	docker logs --tail 50 --follow --timestamps dbmovie
logs-celery:
	docker logs --tail 50 --follow --timestamps celery
logs-redis:
	docker logs --tail 50 --follow --timestamps redis


prune:
	docker system prune -a
images:
	docker images
rmi:
	docker rmi $(docker images)

d-db:
	docker-compose exec db psql --username=django_user --dbname=django_movie_dev

flush:
	python manage.py flush

d-info:
	docker-compose exec web python manage.py seed_db_tmdb_data 2020-03-04 2020-03-04
info:
	python manage.py seed_db_tmdb_data 2020-03-04 2020-03-04

test:
	docker-compose exec web pytest
