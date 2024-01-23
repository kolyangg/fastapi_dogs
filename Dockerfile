# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install dependencies using pip
# The --no-cache-dir option is used to keep the docker image size small
RUN pip install --no-cache-dir fastapi pydantic uvicorn

# Copy the current directory contents into the container at /app
COPY main.py /app/main.py

# Set the working directory to /app
WORKDIR /app

# Make port 5555 available to the world outside this container
EXPOSE 5555

# Define the default command to run when starting the container
# Here we use the uvicorn command to run the main.py file
ENTRYPOINT ["uvicorn"]

# The CMD command is used to provide default arguments for the ENTRYPOINT command
CMD ["main:app", "--host", "0.0.0.0", "--port", "5555"]
