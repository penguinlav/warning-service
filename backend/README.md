Backend server
==============

Installation
------------
1. Create env and install application:
```bash
$ python3 -m venv env && source env/bin/activate && python3 setup.py install
```

2. Create config file and edit it:

```bash
$ warning-service copyconfig
```

3. Apply migrations:
```bash
$ warning-service migrate head
```

4. Fill test data:
```bash
$ warning-service fillfixtures
```

Running
-------
Start server:
```bash
$ warning-service runserver --host localhost --port 8000
```
