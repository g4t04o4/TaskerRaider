FROM python:3.14.7-slim
ARG UID=424242
RUN adduser --disabled-password --uid "${UID}" truser
WORKDIR /trapp
COPY --chown=truser ./requirements.txt /trapp/requirements.txt
RUN pip install --no-cache-dir -r /trapp/requirements.txt
USER truser
COPY --chown=truser . /trapp
EXPOSE 3080
CMD ["fastapi", "run", "main.py", "--port", "3080"]
