## IMPORTAMOS LIBRERIAS ##
from flask import Flask, jsonify, redirect
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os 

## CARGAMOS VARIABLES DE CONFIGURACIÓN ##
load_dotenv()

## CREAMOS LA INSTANCIA ##
app = Flask(__name__)

## CONFIGURAMOS INSTANCIA ##
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

## CREAMOS INSTANCIA DE SQLALCHEM ##
db = SQLAlchemy(app)

## MODELO DE BASE DE DATOS ##
class Task(db.Model):
    __tablename__ = "TASKS"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(250))
    done = db.Column(db.Boolean)


## CREAMOS BASE DE DATOS ##
if not os.path.exists("database.db"):
    db.create_all()
    print("-- Base de datos creada --")
else:
    print("-- Base de datos existe --")


## RUTAS DEL SERVIDOR ## 

@app.route("/")
def index():
    return jsonify({"msg":"ok", "route":"index"})

# read
@app.route("/all")
def all():
    tasks = Task.query.all()
    tareas = []
    for task in tasks:
        agregar = [task.id, task.content, task.done]
        tareas.append(agregar)
    return jsonify({"msg":"ok","Tasks":tareas})

# create
@app.route("/add")
def add():
    content = input("Agregar contenido a la tarea: ")
    new_task = Task(content=content, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/all")

# delete
@app.route("/delete/<int:id>")
def delete(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect("/all")

# update
@app.route("/update/<int:id>")
def update(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect("/all")

if __name__ == "__main__":
    app.run(debug=True)