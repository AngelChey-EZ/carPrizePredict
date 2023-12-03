#Due to scikit-learn
FROM python:3.8-slim

#Change our working directory to app folder
WORKDIR /app
COPY requirements.txt .
#Install all the packages needed to run our web app
RUN pip install -r requirements.txt
# Add every files and folder into the app folder
COPY . .

EXPOSE 8000

# Run gunicorn web server and binds it to the port
CMD python3 -m flask run --host=0.0.0.0
