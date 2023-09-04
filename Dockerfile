#used the official Python 3.11 slim base image
FROM python:3.11-slim   

#set the working directory within the container to /app
WORKDIR /app            

#copied the project s requirements.txt to the container
COPY requirements.txt . 

#installs the dependencies listed on requirements.txt
RUN pip install -r requirements.txt  

#copied the entire project directory to the container
COPY . .   

#exposed port for the application.
EXPOSE 8080 

# defined command to run the application using Uvicorn
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"] 
