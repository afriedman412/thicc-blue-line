FROM python:3.11-slim
ADD src /src
EXPOSE 8000
CMD ["python", "src/server.py"]