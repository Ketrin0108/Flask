import time

from flask import Flask, render_template, request, redirect, url_for, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
import requests
from sqlalchemy import event

from models import db, User, Idea
from schemas import UserSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# что хотим сделать до выполнения запроса
@app.before_request
def before_request():
    g.start_time = time.time()

# что хотим сдедать после выполнения запроса
@app.after_request
def after_request(response):
    total_time = time.time() - g.start_time
    print(f"Время выполнения запроса {total_time:.6f} секунд")
    return response

def log_db_queries(app):
    @event.listens_for(db.engine, "before_cursor_execute") # функция которая слушвет запросы к базе данных
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        # Выводим запросы к базе данных в консоль
        print("Executing query: %s", statement)


with app.app_context(): # доступ контекст к приложению (контекстный менеджер)
    log_db_queries(app)


# Страница для отображения всех пользователей:
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)



@app.route("/")
def home():
    return {"status" : "ok"}

# просмотр идеи для конкретного пользователя:
@app.route("/ideas/users/<int:user_id>")
def show_ideas(user_id):
    return render_template(
        "user_ideas.html",
        user=User.query.get(user_id),
        ideas=Idea.query.filter_by(user_id=user_id).all()
    )

# Функция для генерации идеи и сохранения в базе данных:
@app.route('/ideas/generate/<int:user_id>', methods=['POST'])
def generate_idea(user_id):
    response = requests.get('https://www.boredapi.com/api/activity').json()
    idea = response['activity']
    new_idea = Idea(idea=idea, user_id=user_id)
    db.session.add(new_idea)
    db.session.commit()
    return redirect(url_for('users'))


# создание пользователя
@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        data = request.form
        schema = UserSchema()

        try:
            result = schema.load(data)
        except ValidationError as error:
            return render_template("create_user.html", errors=error.messages, data=data)

        new_user = User(
            first_name=result["first_name"],
            last_name=result["last_name"],

        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("users"))
    else:
        return render_template("create_user.html")


if __name__ == "__main__":
    app.run(debug=True)