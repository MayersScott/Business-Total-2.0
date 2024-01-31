cd ..

cd .venv\Scripts

call activate

cd .. 

cd ..

cd business_total

python manage.py makemigrations

python manage.py migrate

pause