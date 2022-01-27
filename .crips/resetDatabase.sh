rm db.sqlite3
python manage.py migrate --run-syncdb
python manage.py makemigrations
python manage.py migrate
source .crips/createSuperUser.sh snow
