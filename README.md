Kona Org Chart API 

Parses test data json, loads data into database and exposes data for Channels, Users, 
and Teams via API endpoints. 


Running API: 

1. Activate virtual environment
2. pip install requirements.txt from terminal 
3. Run commands to load database tables and start the development server: 
        - python manage.py makemigrations
        - python manage.py migrate
        - python manage.py runserver 8082
4. Navigate to https://localhost:8082/api/consolidated-primary (or the other endpoints)
