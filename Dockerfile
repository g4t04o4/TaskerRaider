FROM python:3.14.7-slim
WORKDIR /trapp
COPY ./requirements.txt /trapp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /trapp/requirements.txt
COPY . /trapp
CMD ["fastapi", "run", "main.py", "--port", "3080"]
EXPOSE 3080