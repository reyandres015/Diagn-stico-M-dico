## Paso 1: Activar ambiente virtual
```shell
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Paso 2: Crear variable para ejecución
```shell
export FLASK_APP = main.py
```

## Paso 3: Iniciar aplicación web

```shell
flask run
```

La página estará disponible en
[http://localhost:5000/](http://localhost:5000/)
