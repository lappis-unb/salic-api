FROM debian:buster-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    sqlite3

# Install project's dependencies
RUN python3 setup.py develop
RUN pip3 install -e .[dev]

# Create database
RUN inv db -f

# Set enviroment variables to prevent encode related issues
ENV LC_ALL C.UTF-8
ENV LANG=C.UTF-8

# Install pyodbc
RUN apt-get install unixodbc-dev tdsodbc -y
RUN pip3 install pyodbc
COPY docker/odbcinst.ini /etc/odbcinst.ini

# Expose host's port to run the web application
EXPOSE 5000

CMD ["inv", "run", "-h", "0.0.0.0"]
