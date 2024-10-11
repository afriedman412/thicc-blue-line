FROM python:3.11-slim

# Install the locales package
RUN apt-get update && apt-get install -y locales

# Generate and set the locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Set environment variables for locale
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

ADD src /app/src
ADD requirements.txt /app/requirements.txt
ADD app.py /app/app.py
ADD config.py /app/config.py
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]