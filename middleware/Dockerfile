FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for python-ldap and build tools
RUN apt-get update && apt-get install -y \
    libsasl2-dev libldap2-dev libssl-dev gcc libpq-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip  # Optional: upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app

CMD ["python", "main.py"]
