rm users/migrations/0*.py titles/migrations/0*.py reviews/migrations/0*.py 
rm db.sqlite3
py manage.py makemigrations
py manage.py migrate
py import_csv.py

