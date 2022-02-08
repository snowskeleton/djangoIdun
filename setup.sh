# prelim
sudo apt update
sudo apt-get install -y python3 python3-pip python3-venv python3-tk apache2 libapache2-mod-wsgi-py3 sqlite3
sudo apt-get install libpq-dev postgresql postgresql-contrib
python3 -m venv ./venv
source venv/bin/activate
alias python="venv/bin/python3"
sudo python -m pip install -r requirements.txt

# .env config
sudo rm -f .env
key=$(openssl rand -base64 32)
echo "SECRET_KEY=${key}" > .env
printf "hostname (name of your website, or IP address): "
read hostname
echo "ALLOWED_HOSTS=${hostname},127.0.0.1" >> .env
echo "STATIC_URL='static/'" >> .env
echo "STATIC_ROOT='static/'" >> .env
echo "MEDIA_URL='media/'" >> .env
echo "MEDIA_ROOT='media/'" >> .env

# site setup
sudo python manage.py collectstatic
sudo sed "s/changeMe/${USER}/g" default_setup/defaultApache > tmp
sudo cp tmp /etc/apache2/sites-available/royal.conf
sudo a2ensite royal.conf && sudo a2dissite 000-default.conf

# permissions and db
# create user king;
# create database treasure;
# alter role king with password 'gold';
# grant all privileges on database treasure to king;
# alter database treasure owner to king;
sudo rm db.sqlite3 && touch db.sqlite3 && mkdir media
sudo chown -R www-data:www-data ../nobility
sudo python3 manage.py migrate --run-syncdb
sudo python3 manage.py makemigrations && python3 manage.py migrate
sudo chown -R www-data:www-data ../nobility
sudo chmod -R 775 media
sudo chmod 664 db.sqlite3

# new user
printf "New admin user: "
        read username
sudo python3 manage.py createsuperuser --username=${username} --email=''

export DJANGO_SETTINGS_MODULE=royal.settings

sudo systemctl enable apache2
sudo systemctl restart apache2
