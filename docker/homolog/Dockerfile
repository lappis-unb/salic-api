FROM debian:buster-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-crypto \
        python3-setuptools \
        python3-pyodbc \
        tdsodbc \
        gunicorn3 \
 && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
ADD . /app

# Install project's dependencies
RUN pip3 install wheel
RUN python3 /app/setup.py bdist_wheel
RUN python3 /app/setup.py develop
RUN pip3 install -e ".[dev]"

# Set enviroment variables to prevent encode related issues
ENV LC_ALL C.UTF-8
ENV LANG=C.UTF-8

# Install pyodbc
COPY docker/odbcinst.ini /etc/odbcinst.ini

EXPOSE 5000

CMD ["inv", "run-gunicorn", "-h 0.0.0.0:5000", "-w 4"]
