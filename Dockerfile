# Use an official Python runtime as a parent image  
FROM python:3.9-slim  
    
# Set the working directory in the container  
WORKDIR /usr/src/app  

# Copy the requirements file into the container  
COPY requirements.txt ./  

# Install any dependencies specified in requirements.txt  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application code into the container  
COPY . .  

# Make port 80 available to the world outside this container  
# (Optional, only if your application runs on a specific port)  
# EXPOSE 80  

# Define environment variable  
# ENV PYTHONUNBUFFERED=1  

# Make the run script executable  
RUN chmod +x run.sh  

# Command to run the script  
CMD ["./run.sh"]  