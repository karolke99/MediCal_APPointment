generate-db-migration:
	@echo "$(BOLD)Generating db migration file(RESET)"
	pipenv run flask db stamp head && pipenv run flask db migrate && pipenv run flask db upgrade


set-db:
	docker pull postgres:16.1
	docker volume create postgres_data
	docker run --name postgres_container -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres