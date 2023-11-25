FROM navikey/raspbian-bullseye
RUN apt-get update \
&& apt-get install build-essential -y \
&& apt-get install python3-pip -y \
&& pip install poetry

COPY ./pyproject.toml /rpi-hex-control/
WORKDIR /rpi-hex-control/
RUN poetry install --no-dev

COPY ./app /rpi-hex-control/app/
COPY ./dotenv /rpi-hex-control/dotenv/
RUN poetry install --no-dev
ENTRYPOINT poetry run python -m app.main

