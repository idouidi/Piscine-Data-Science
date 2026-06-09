# ==============================================================================
#  Makefile — PostgreSQL via Docker Compose
# ==============================================================================

# ---------------------------------------------------------------------------- #
#  Configuration
# ---------------------------------------------------------------------------- #

COMPOSE_FILE   := docker-compose.yml
ENV_FILE       := .env
DC             := docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE)



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
	@command -v docker > /dev/null 2>&1 || \
		(printf "$(RED)[ERROR]$(RESET) Docker is not installed.\n" && exit 1)
	@docker info > /dev/null 2>&1 && exit 0; \
		printf "$(YELLOW)[WARN]$(RESET)  Docker daemon is not running, starting it...\n"; \
		sudo systemctl start docker || \
			(printf "$(RED)[ERROR]$(RESET) Failed to start Docker daemon.\n" && exit 1); \
		printf "$(GREEN)[OK]$(RESET)    Docker daemon started.\n"

# Ensure .env exists and all required variables are set
_check-env:
	@test -f $(ENV_FILE) || \
		(printf "$(RED)[ERROR]$(RESET) $(ENV_FILE) not found. Create it with the required variables:\n" && \
		 printf "  POSTGRES_USER=\n  POSTGRES_PASSWORD=\n  POSTGRES_DB=\n  POSTGRES_PORT=\n  PGADMIN_EMAIL=\n  PGADMIN_PASSWORD=\n  PGADMIN_PORT=\n" && \
		 exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_USER" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_USER is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_PASSWORD" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_PASSWORD is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_DB" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_DB is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$POSTGRES_PORT" || \
		(printf "$(RED)[ERROR]$(RESET) POSTGRES_PORT is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$PGADMIN_EMAIL" || \
		(printf "$(RED)[ERROR]$(RESET) PGADMIN_EMAIL is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$PGADMIN_PASSWORD" || \
		(printf "$(RED)[ERROR]$(RESET) PGADMIN_PASSWORD is not set in $(ENV_FILE)\n" && exit 1)
	@. ./$(ENV_FILE) && test -n "$$PGADMIN_PORT" || \
		(printf "$(RED)[ERROR]$(RESET) PGADMIN_PORT is not set in $(ENV_FILE)\n" && exit 1)

# ---------------------------------------------------------------------------- #
#  FULL STACK
# ---------------------------------------------------------------------------- #

## up    : Start stack and wait for all healthchecks
up: _check-docker _check-env
	@printf "$(GREEN)[UP]$(RESET)    Starting the stack...\n"
	@$(DC) up -d --remove-orphans
	@printf "$(GREEN)[OK]$(RESET)    Stack started. Waiting for healthchecks...\n"
	@for CID in $$($(DC) ps -q); do \
		name=$$(docker inspect --format='{{.Name}}' $$CID | sed 's#^/##'); \
		has_health=$$(docker inspect --format='{{if .State.Health}}yes{{end}}' $$CID 2>/dev/null); \
		[ "$$has_health" != "yes" ] && printf "$(YELLOW)[SKIP]$(RESET)  $$name (no healthcheck)\n" && continue; \
		printf "$(CYAN)[WAIT]$(RESET)  $$name\n"; \
		timeout=60; \
		state=pending; \
		while [ $$timeout -gt 0 ]; do \
			status=$$(docker inspect --format='{{.State.Health.Status}}' $$CID 2>/dev/null); \
			if [ "$$status" = "healthy" ]; then \
				printf "$(GREEN)[OK]$(RESET)    $$name healthy\n"; \
				state=ok; \
				break; \
			fi; \
			if [ "$$status" = "unhealthy" ]; then \
				printf "$(RED)[ERROR]$(RESET) $$name healthcheck failed\n"; \
				docker logs $$CID; \
				state=fail; \
				break; \
			fi; \
			sleep 1; \
			timeout=$$((timeout - 1)); \
		done; \
		if [ "$$state" = "pending" ]; then \
			printf "$(RED)[ERROR]$(RESET) Timeout waiting for $$name\n"; \
			docker logs $$CID; \
			state=fail; \
		fi; \
		[ "$$state" = "fail" ] && exit 1; \
		true; \
	done
	@printf "$(GREEN)[READY]$(RESET) All healthchecks passed.\n"

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
	@printf "$(CYAN)[POSTGRES]$(RESET) Opening bash shell in container 'postgres'...\n"
	@docker exec -it postgres bash

# ---------------------------------------------------------------------------- #
#  CLEAN
# ---------------------------------------------------------------------------- #

## clean    : Remove all containers, volumes and local images
clean: _check-docker
	@printf "$(RED)[CLEAN]$(RESET) Removing all Docker resources...\n"
	@$(DC) down --volumes --remove-orphans 2>/dev/null || true
	@docker system prune -a --volumes -f 2>/dev/null && \
		printf "$(YELLOW)[CLEAN]$(RESET) All Docker resources removed.\n" || \
		printf "$(YELLOW)[CLEAN]$(RESET) Nothing to remove.\n"
	@printf "$(GREEN)[OK]$(RESET)    Clean complete.\n"

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
	@printf "\n$(YELLOW)Individual service example:$(RESET)\n"
	@printf "  $(GREEN)make service-up SVC=postgres$(RESET)\n\n"