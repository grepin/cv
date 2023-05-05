# PROD
up:
	docker-compose -f docker-compose.yml up -d

# DEV
up_dev:
	docker-compose -f docker-compose.dev.yml up -d

# TEST
# Clean tables in PostgresQL
up_test_enviroment:
	docker-compose -f docker-compose.test.yml up -d
Down:
    docker-compose -f docker-compose.test.yml down

Authorization module (Flask) test run:
    - docker-compose exec -it auth bash test_auth.sh
For adminfunctions test run
    - docker-compose exec -it admin bash test_admin.sh
