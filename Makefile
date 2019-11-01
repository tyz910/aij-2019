IMAGE=tyz910/aij-2019

ifeq ($(OS), Windows_NT)
	DOCKER_BUILD=docker build -t ${IMAGE} .
else
	DOCKER_BUILD=docker build -t ${IMAGE} . && (docker ps -q -f status=exited | xargs docker rm) && (docker images -qf dangling=true | xargs docker rmi) && docker images
endif

DOCKER_RUN=docker run --rm --network none -it -v ${CURDIR}:/app -w /app -p 8000:8000 ${IMAGE}

exec:
	${DOCKER_RUN} /bin/bash

run:
	${DOCKER_RUN} python3 server.py

docker-build:
	${DOCKER_BUILD}

docker-push:
	docker push ${IMAGE}

validate-submission:
	${DOCKER_RUN} /bin/bash -c "python3 dev/validate_submission.py"

sberbank:
	${DOCKER_RUN} /bin/bash -c "python3 lib/sberbank/evaluation_script.py"

submission:
	${DOCKER_RUN} /bin/bash -c "sed -i.bak 's~{image}~${IMAGE}~g' metadata.json && zip -9 -r var/submissions/submission_`date '+%Y%m%d_%H%M%S'`.zip server.py lib/*.py lib/**/*.py lib/**/**/*.py var/model/lgb/* var/model/ctb/* var/model/stress/* var/model/esse/* var/model/pkl/* var/data/esse/* var/model/spell/* var/model/paronyms.pickle metadata.json && mv metadata.json.bak metadata.json"
