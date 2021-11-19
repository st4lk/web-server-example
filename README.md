Web Server Example
==================
Works on python 3.6+

Run
---

### Run web server using current app
```bash
python src/server.py app:web_app
```

### Run web server using another app (django)

1. Activate virtual env of your django project
2. Step into the path, where manage.py file is
3. Replace `project` with your folder name where wsgi.py file is placed in the command below
4. Replace `/path/to/current/webserver/` with full path where you cloned this repo in the command below
5. Run

```bash
PYTHONPATH=. python /path/to/current/webserver/src/server.py project.wsgi:application
```

### Run gunicorn

- Will serve app from this repo on http://0.0.0.0:9999

```bash
cd gunicorn
make run
```

If you want to server your own app (django), do the following:
```bash
cd /path/to/django/project/
# activate your virtual env if you use it
pip install gunicorn
# replace "project" with your project name
gunicorn -b 0.0.0.0:9999 -w 2 project.wsgi:application
```

### Run nginx

- Will serve on http://0.0.0.0:8080
- Will proxy requests to http://0.0.0.0:9999

```bash
cd nginx
make run

# OR, to serve static from /path/to/static/ (replace path to match your folder)
STATIC_ROOT=/path/to/static/ make run
```

Simulate slow client
--------------------

```bash
python src/client.py 0.0.0.0:9999

python src/client.py 0.0.0.0:8080
```
