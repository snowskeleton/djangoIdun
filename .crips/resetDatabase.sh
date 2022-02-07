rm db.sqlite3
python manage.py migrate --run-syncdb
python manage.py makemigrations
python manage.py migrate
printf "Username: "
read username
source .crips/createSuperUser.sh ${username}