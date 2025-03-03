FROM python:3.12
LABEL maintainer="Juan Treminio <jtreminio@gmail.com>"

COPY ./oseg /usr/app/oseg
COPY ./static /usr/app/static
COPY ./LICENSE /usr/app/LICENSE
COPY ./pyproject.toml /usr/app/pyproject.toml
COPY ./requirements.txt /usr/app/requirements.txt
COPY ./run.py /usr/app/run.py
COPY ./setup.py /usr/app/setup.py

WORKDIR /usr/app

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

ENTRYPOINT ["python3", "/usr/app/run.py"]
