FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "jupyter", "notebook", "--allow-root", "--ip", "0.0.0.0" ]