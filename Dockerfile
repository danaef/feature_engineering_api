FROM python:3.11-slim   #used the official Python 3.11 slim base image
WORKDIR /app            #set the working directory within the container to /app
COPY requirements.txt . #copied the project's requirements.txt to the container
RUN pip install -r requirements.txt  #installs the dependencies listed on requirements.txt
COPY . .   #copied the entire project directory to the container
EXPOSE 8080 #exposed port for the application.
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"] # defined command to run the application using Uvicorn
