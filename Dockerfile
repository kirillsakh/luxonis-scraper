FROM python:3.11-slim-bullseye

# Install netcat
RUN apt-get update && apt-get install -y netcat

# Add wait-for script
COPY wait-for /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for

# Set the working directory to /src
WORKDIR /src

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install the Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /src
COPY src/ .

# Specify the command to run on container start
CMD wait-for "$POSTGRES_HOST" "$POSTGRES_PORT" python app.py
