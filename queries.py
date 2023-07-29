from datetime import date

from sqlalchemy import func, Integer, update

from models import Idea, User


# вычислить сколько идей всего
def get_all_idea():
    return Idea.query.all()

# вычислить сколько у каждого пользователя идей
def get_user_with_ideas():
    return db.session.query(User).join(Idea).all()

# вычислить пользователя по Id
def get_user_by_id():
    return User.query.filter_by(id=1).яfirst()

# вычислить пользователя по first_name
def get_users_by_name():
    return User.query.filter_by(first_name="Меган").all()


# найти идею которая содержит "arn" (не учитывает регистр ilike, может быть все что угодно до и после,но обязательно содержать эти 3 буквы)
def get_ideas_by_name_substring():
    return Idea.query.filter(
        Idea.idea.ilike(f"%arn%")
    ).all()

# найти идею которая начинается с этого слова ,если i подставляем то без учета регистра
def get_udeas_name_startswith():
    return Idea.query.filter(
        Idea.idea.startswith(f"Make")
    ).all()

# получить пользователя, у которога идея заканчивается на букву 'k'
def get_users_with_ideas_ending_with_k():
    return User.query.filter(
        User.ideas.any(Idea.idea.like("%k"))
    ).all()

# получить пользователя ,у которго имя заканчивается на 'а' не выходит результат!!
def get_users_ending_with_a():
    return User.query.join(Idea).filter(User.first_name.like("%a")).all()

# получить всех пользователей ,которые находится в списке "in" (Кира, Меган)
def get_users_by_names():
    return User.query.filter(User.first_name.in_(["Кира", "Меган"])).all()

# получить только тех пользователей , у которых количесвто идей больше 5
def select_users_with_gte_5_ideas():
    return db.session.query(User).outerjoin(User.ideas).group_by(User).having(func.count(Idea.id) >= 5).all()

def func():
    # Удалить все идеи, в которых есть слово "Learn"
    ideas_to_delete = Idea.query.filter(Idea.idea.ilike('%Learn%')).all()
    for idea in ideas_to_delete:
        db.session.delete(idea)
    db.session.commit()

    # Обновить имя пользователя с id=1
    update_query = update(User).where(User.id == 1).values(first_name='Дэвид')

    # Выполняем SQL-запрос
    db.session.execute(update_query)
    db.session.commit()


if __name__ == "__main__":
    from app import db, app

    with app.app_context():
        result = func()
        result