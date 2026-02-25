FROM python:3.10-slim

RUN useradd -ms /bin/bash  appuser
WORKDIR /home/appuser

RUN apt-get update && \
	apt-get -y install python3-dev libevent-dev gcc

USER appuser

COPY --chown=appuser:appuser requirements.txt requirements.txt
COPY --chown=appuser:appuser requirements_test.txt requirements_test.txt

ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV TEST_IN_CONTAINER=True

RUN pip install --upgrade pip && \
	pip install --user -r requirements.txt && \
	pip install --user -r requirements_test.txt

COPY --chown=appuser:appuser . .

CMD ["-m", "unittest"]
ENTRYPOINT ["python3"]