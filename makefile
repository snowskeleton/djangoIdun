sudo apt-get install -y python3 python3-pip sqlite3 python3-venv apache2 libapache2-mod-wsgi-py3
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
# need to change settings.py file. add the correct ALLOWED_HOSTS, and configure static and media paths
# https://www.youtube.com/watch?v=Sa_kQheCnds
python manage.py collectstatic
source .crips/migrateDatabase.sh
start apache2 service and give permissions

