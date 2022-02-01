sudo apt-get install -y python3 python3-pip pythonsqlite3 python3-venv python3-tk apache2 libapache2-mod-wsgi-py3
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt

#bash
key=$(openssl rand -base64 32)
echo "SECRET_KEY=${key}" > .env
printf "hostname (name of your website, or IP address): "
read hostname
echo "ALLOWED_HOSTS = ['${hostname}']" >> royal/.env.py
echo "STATIC_URL = ['static/']" >> royal/.env.py
echo "STATIC_ROOT = ['static/']" >> royal/.env.py
echo "MEDIA_URL = ['media/']" >> royal/.env.py
echo "MEDIA_ROOT = ['media/']" >> royal/.env.py
# https://www.youtube.com/watch?v=Sa_kQheCnds
#nobash
python manage.py collectstatic
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