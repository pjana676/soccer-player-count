# Use the official Python image as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for YOLO
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    libopencv-dev \
    libopencv-core-dev \
    libopencv-imgcodecs-dev \
    libopencv-highgui-dev

# Clone Darknet repository
RUN git clone https://github.com/pjreddie/darknet /app/darknet

# Set the working directory to Darknet
WORKDIR /app/darknet

# Build Darknet (adjust options if needed)
RUN make

# Create the /app/cfg directory
RUN wget https://pjreddie.com/media/files/yolov3.weights


# Create and set the working directory
WORKDIR /app


# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install project dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire Django project to the container
COPY . /app/

# Expose the port that Django runs on (adjust if needed)
EXPOSE 8000

# Command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
