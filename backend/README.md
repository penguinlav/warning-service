Backend server
==============

Installation
------------
1. Build [frontend](frontend/README.md)

2. Edit `config.yml`

3. Create env and install requirements:
```bash
$ python3 -m venv env && source env/bin/activate && pip install -r requirements.txt
```

4. Apply migrations:
```bash
$ python run.py migrate head
```

5. Fill test data:
```bash
$ python run.py fillfixtures
```

Running
-------
Start server:
```bash
$ python run.py runserver --host localhost --port 8000
```
