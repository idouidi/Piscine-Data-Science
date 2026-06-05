
# ---------------------------------------------------------------------------- #
#  Configuration
# ---------------------------------------------------------------------------- #

COMPOSE_FILE   := docker-compose.yml
ENV_FILE       := .env
DC             := docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE)

CONTAINER      := postgres_db

# Colors (auto-disabled via: make NO_COLOR=1 <target>)
ifdef NO_COLOR
  RED    :=
  GREEN  :=
  YELLOW :=
  CYAN   :=
  RESET  :=
else
  RED    := \033[0;31m
  GREEN  := \033[0;32m
  YELLOW := \033[0;33m
  CYAN   := \033[0;36m
  RESET  := \033[0m
endif

# ---------------------------------------------------------------------------- #
#  Phony targets declaration (prevents any relink on same-named files)
# ---------------------------------------------------------------------------- #

.PHONY: all up down start stop re logs ps \
        service-up service-down postgres psql \
        clean help \
        _check-docker _check-env

# ---------------------------------------------------------------------------- #
#  Default target
# ---------------------------------------------------------------------------- #

all: help

# ---------------------------------------------------------------------------- #
#  Pre-flight checks
# ---------------------------------------------------------------------------- #

# Ensure docker is installed and the daemon is running, start it if needed (Ubuntu)
_check-docker:
	@command -v docker >/dev/null 2>&1 || \
		(printf "$(RED)[ERROR]$(RESET) Docker is not installed.\n" && exit 1)

	@docker info >/dev/null 2>&1 && exit 0; \
		if sudo docker info >/dev/null 2>&1; then \
			printf "$(RED)[ERROR]$(RESET) Current user is not allowed to access Docker.\n"; \
			printf "Run: sudo usermod -aG docker $$USER\n"; \
			exit 1; \
		fi; \
		printf "$(YELLOW)[WARN]$(RESET) Docker daemon is not running, starting it...\n"; \
		sudo systemctl start docker || \
			(printf "$(RED)[ERROR]$(RESET) Failed to start Docker daemon.\n" && exit 1)

# Ensure .env exists and all required variables are set
_check-env:
	@test -f $(ENV_FILE) || \
		(printf "$(RED)[ERROR]$(RESET) $(ENV_FILE) not found.\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_USER" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_USER is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_PASSWORD" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_PASSWORD is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_DB" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_DB is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_PORT" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_PORT is not set in $(ENV_FILE)\n" && exit 1)

# ---------------------------------------------------------------------------- #
#  FULL STACK
# ---------------------------------------------------------------------------- #

## up    : Start the full stack in daemon mode
up: _check-docker _check-env
	@printf "$(GREEN)[UP]$(RESET)    Starting the stack...\n"
	@$(DC) up -d --remove-orphans
	@CID=$$($(DC) ps -q postgres); \
	test -n "$$CID" || { \
		printf "$(RED)[ERROR]$(RESET) Unable to find postgres container.\n"; \
		exit 1; \
	}; \
	printf "$(GREEN)[OK]$(RESET)    Stack started. Waiting for postgres healthcheck...\n"; \
	timeout=60; \
	while [ $$timeout -gt 0 ]; do \
		status=$$(docker inspect --format='{{.State.Health.Status}}' $$CID 2>/dev/null); \
		[ "$$status" = "healthy" ] && { \
			printf "$(GREEN)[READY]$(RESET) PostgreSQL is up and healthy.\n"; \
			exit 0; \
		}; \
		[ "$$status" = "unhealthy" ] && { \
			printf "$(RED)[ERROR]$(RESET) PostgreSQL healthcheck failed.\n"; \
			docker logs $$CID; \
			exit 1; \
		}; \
		sleep 1; \
		timeout=$$((timeout - 1)); \
	done; \
	printf "$(RED)[ERROR]$(RESET) Timeout waiting for PostgreSQL healthcheck.\n"; \
	docker logs $$CID; \
	exit 1

## down  : Stop and remove containers (volumes are kept)
down: _check-docker
	@printf "$(YELLOW)[DOWN]$(RESET)  Stopping and removing containers...\n"
	@$(DC) down --remove-orphans
	@printf "$(GREEN)[OK]$(RESET)    Containers removed.\n"

## start : Start existing containers without recreating them
start: _check-docker
	@printf "$(GREEN)[START]$(RESET) Starting existing containers...\n"
	@$(DC) start
	@printf "$(GREEN)[OK]$(RESET)    Containers started.\n"

## stop  : Stop containers without removing them
stop: _check-docker
	@printf "$(YELLOW)[STOP]$(RESET)  Stopping containers (data preserved)...\n"
	@$(DC) stop
	@printf "$(GREEN)[OK]$(RESET)    Containers stopped.\n"

## re    : Full clean rebuild (clean → up)
re: clean up

# ---------------------------------------------------------------------------- #
#  INDIVIDUAL SERVICE  —  usage: make service-up   SVC=postgres
#                                 make service-down SVC=postgres
# ---------------------------------------------------------------------------- #

SVC ?= postgres

## service-up   : Start a single service (SVC=<name>, default: postgres)
service-up: _check-docker _check-env
	@printf "$(GREEN)[UP]$(RESET)    Starting service '$(SVC)'...\n"
	@$(DC) up -d --no-deps --remove-orphans $(SVC)
	@printf "$(GREEN)[OK]$(RESET)    Service '$(SVC)' started.\n"

## service-down : Stop and remove a single service (SVC=<name>, default: postgres)
service-down: _check-docker
	@printf "$(YELLOW)[DOWN]$(RESET)  Stopping service '$(SVC)'...\n"
	@$(DC) stop $(SVC)
	@$(DC) rm -f $(SVC)
	@printf "$(GREEN)[OK]$(RESET)    Service '$(SVC)' stopped and removed.\n"

# ---------------------------------------------------------------------------- #
#  UTILITIES
# ---------------------------------------------------------------------------- #

## logs     : Stream container logs (Ctrl+C to quit)
logs: _check-docker
	@$(DC) logs -f --tail=50

## ps       : Show detailed container status
ps: _check-docker
	@printf "$(CYAN)[STATUS]$(RESET)\n"
	@$(DC) ps -a

## postgres : Open a bash shell inside the postgres container
postgres: _check-docker
	@printf "$(CYAN)[POSTGRES]$(RESET) Opening bash shell in container '$(CONTAINER)'...\n"
	@docker exec -it $(CONTAINER) bash


# ---------------------------------------------------------------------------- #
#  CLEAN
# ---------------------------------------------------------------------------- #


## clean    : Fully reset project (containers, volumes, images, networks)
clean: _check-docker
	@printf "$(RED)[CLEAN]$(RESET) Full project reset starting...\n"

	@echo "Stopping and removing compose stack..." && \
	$(DC) down --volumes --remove-orphans --rmi all || true

	@echo "Removing project volumes..." && \
	docker volume ls -q | grep postgres || true | xargs -r docker volume rm || true

	@echo "Removing project networks..." && \
	docker network ls -q | grep postgres || true | xargs -r docker network rm || true

	@echo "Removing dangling images..." && \
	docker image prune -af || true

	@printf "$(GREEN)[OK]$(RESET) Full reset complete.\n"

# ---------------------------------------------------------------------------- #
#  HELP
# ---------------------------------------------------------------------------- #

## help     : Display this help message
help:
	@printf "\n$(CYAN)╔══════════════════╗$(RESET)\n"
	@printf "$(CYAN)║     Makefile     ║$(RESET)\n"
	@printf "$(CYAN)╚══════════════════╝$(RESET)\n\n"
	@printf "$(YELLOW)Full stack:$(RESET)\n"
	@grep -E '^## (up|down|start|stop|re) ' $(MAKEFILE_LIST) | \
		awk -F ' : ' '{ printf "  $(GREEN)make %-16s$(RESET) %s\n", substr($$1, 4), $$2 }'
	@printf "\n$(YELLOW)Individual service:$(RESET)\n"
	@grep -E '^## service' $(MAKEFILE_LIST) | \
		awk -F ' : ' '{ printf "  $(GREEN)make %-16s$(RESET) %s\n", substr($$1, 4), $$2 }'
	@printf "\n$(YELLOW)Utilities:$(RESET)\n"
	@grep -E '^## (logs|ps|postgres|psql) ' $(MAKEFILE_LIST) | \
		awk -F ' : ' '{ printf "  $(GREEN)make %-16s$(RESET) %s\n", substr($$1, 4), $$2 }'
	@printf "\n$(YELLOW)Clean:$(RESET)\n"
	@grep -E '^## clean ' $(MAKEFILE_LIST) | \
		awk -F ' : ' '{ printf "  $(GREEN)make %-16s$(RESET) %s\n", substr($$1, 4), $$2 }'
