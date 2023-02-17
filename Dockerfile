FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m playwright install
RUN playwright install-deps
COPY . .

CMD [ "python3", "run.py"]