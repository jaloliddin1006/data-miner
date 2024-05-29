# Data Miner Bot

The telegram bot which written in aiogram framework integrated with django. Database built with postgresql

Just example of `echobot`

## Setup project

- Install all requirements using the command below
```shell
pip install -r requirements.txt
```
- Then copy the .env.example file to .env and customize yourself.
```shell
cp .env.example .env
```
- Add tables to your database.
```shell
python manage.py migrate
```

- Run the bot using the command below
```shell
python manage.py runbot
```

# 
- Create superuser for backend the command below
```shell
python manage.py createsuperuser
```

- Run the django project using the command below
```shell
python manage.py runserver
```


# Deploy Aiogram Bot


aiogram orqali yozilgan telegram botni ubuntu serverga deploy qilamiz.
Buning uchun quidagi manzilda bot uchun service yozish uchun faylni ochib olamiz:

`nano /etc/systemd/system/{yourbot}.service`

endi ushbu service faylga quidagini yozamiz:
```
[Unit]
Description=Aiogram Bot Description

[Service]
Type=simple
ExecStart=/{path}/{your}/{project}/venv/bin/python  /{path}/{your}/{project}/manage.py runbot

[Install]
WantedBy=multi-user.target
```
service ni yozib bo'lgandan so'ng uni ishga tushirib qo'yamiz:

`sudo systemctl daemon-reload`

`sudo systemctl enable {yourbot}.service`

`sudo systemctl start {yourbot}.service`

`sudo systemctl status {yourbot}.service`

# get backup from sqlite
`sqlite3 db.sqlite3 .dump > backup.sql`

# restore backup file
`psql -U db_user db_name < backup.sql`
