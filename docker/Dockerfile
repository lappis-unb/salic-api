FROM debian:buster-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-crypto \
        sqlite3 \
        gunicorn3 \
        unixodbc-dev \
        tdsodbc \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
ADD . /app

# Install project's dependencies
RUN python3 setup.py install
RUN pip3 install invoke

# Create database
RUN inv db --force

# Set enviroment variables to prevent encode related issues
ENV LC_ALL C.UTF-8
ENV LANG=C.UTF-8

# Install pyodbc
RUN pip3 install pyodbc
COPY docker/odbcinst.ini /etc/odbcinst.ini

EXPOSE 5000

ENTRYPOINT ["docker/entrypoint.sh"]

CMD ["inv", "run-gunicorn", "-h 0.0.0.0:5000", "-w 4"]
