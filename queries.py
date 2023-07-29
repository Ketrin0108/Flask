from datetime import date

from sqlalchemy import func, Integer

from models import User, Idea


def get_all_users():
    return User.query.all()

def get_user_with_count_of_idea():
    return db.session.query(User, func.count(User.id)).outerjoin(User.idea).group_by(Idea).all()


if __name__ == "__main__":
    from app import db, app

    with app.app_context():
        result = get_user_with_count_of_idea()
        print(result)