FROM python:alpine3.14

# Set the working directory
WORKDIR /dynuiuc
COPY python/*.py /dynuiuc
COPY . /dynuiuc

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "main.py"]