# Defines base image
FROM python:3.10

# Defines the work directory inside the container
WORKDIR /app

# Copies requirement file to the working directory
COPY requirements.txt .

# Installs project dependecies (as described in requirements file)
RUN pip install --no-cache-dir -r requirements.txt

# Copies the project source code to the working directory
COPY . .

# Defines the comand to execute the API (this command is executed as soon as the container is up and running)
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000", "--reload"]