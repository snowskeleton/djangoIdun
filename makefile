sudo apt-get install -y python3 python3-pip pythonsqlite3 python3-venv python3-tk apache2 libapache2-mod-wsgi-py3
sudo apt update
sudo apt-get install -y python3 python3-pip python3.8-venv python3-tk apache2 libapache2-mod-wsgi-py3
sudo python3 -m venv ./venv
source venv/bin/activate
sudo python3 -m pip install -r requirements.txt

#bash
key=$(openssl rand -base64 32)
echo "SECRET_KEY=${key}" > .env
printf "hostname (name of your website, or IP address): "
read hostname
echo "ALLOWED_HOSTS=['${hostname}', "127.0.0.1"]" >> .env
echo "STATIC_URL='static/'" >> .env
echo "STATIC_ROOT='static/'" >> .env
echo "MEDIA_URL='media/'" >> .env
echo "MEDIA_ROOT='media/'" >> .env
# https://www.youtube.com/watch?v=Sa_kQheCnds
#nobash
sudo python3 manage.py collectstatic
# source .crips/migrateDatabase.sh
sudo cp default_setup/defaultApache /etc/apache2/sites-available/royal.conf
sudo a2ensite royal.conf
sudo a2dissite 000-default.conf

sudo touch db.sqlite3 && mkdir media
sudo mkdir -p /var/www/nobility/ && sudo cp -r $(pwd) /var/www/
sudo chown :www-data /var/www/nobility/db.sqlite3
sudo chown :www-data /var/www/nobility/
sudo chown -R :www-data /var/www/nobility/media
sudo chmod -R 775 /var/www/nobility/media
sudo chmod 664 /var/www/nobility/db.sqlite3

export DJANGO_SETTINGS_MODULE=royal.settings

sudo systemctl enable apache2
sudo systemctl restart apache2