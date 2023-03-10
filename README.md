# Charity Solutions:ukraine:


## :arrow_up: The project purpose
It's <b>Ukranian project</b>, the main purpose of which - couple charity organisations with people in :ukraine: who need help.
- <b>Charity organisation</b> can registrate themself and post some 'help-posts' where, what, when and how they can help
- <b>Ordinary people</b> can read this info, and realise, when they can receive help in their region. 
<br>Moreover, they can registrate themself for easier registration in line of help, that charity organisation can provide.

## :hammer: Enviroment stack
Python, Django, PostgreSQL, DjangoToolBar, black, Jinja, HTML, Bootstrap
<br><br>

## :computer: Back-end features
- Optimized DB queries
- FBV
- docker-support: https://github.com/YehorVoitenko/CharitySolution_docker.git
- DjangoToolBar
<br><br>


## :bust_in_silhouette: Contacts

- <b>Email:</b> egorka.voitenko@gmail.com
- <b>LinkedIn:</b> https://www.linkedin.com/in/yehorvoitenko/
- <b>CV:</b> in LinkedIn
<br><br>

## 	:dizzy: Quickstart

```bash
pip install django
pip install -r requirements.txt
```

<h3>There are 2 ways to start my project</h3>

<h3>:whale: To start poject in <b>DOCKER</b>:</h3>

1. Go to: https://github.com/YehorVoitenko/CharitySolution_docker.git
2. There clone this repository: https://github.com/YehorVoitenko/CharitySolution.git
3. Use this command
```
docker-compose build

docker-compose up
```
4. Make migrations in second terminal
```
docker-compose run web-app python manage.py makemigrations

docker-compose run web-app python manage.py migrate

```

<h3>:abacus:	 To start poject in <b>TERMINAL</b>:</h3>

```
python manage.py runserver

```





