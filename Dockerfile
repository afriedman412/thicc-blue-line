FROM python:3.11-slim
ADD src /src
WORKDIR /src
EXPOSE 8000
CMD ["python", "server.py"]