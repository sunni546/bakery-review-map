from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(16), unique=True, nullable=False)
    image = db.Column(db.String(255))
    point = db.Column(db.Integer, default=0)

    def __repr__(self):
        return (f"User(id={self.id!r}, email={self.email!r}, password={self.password!r}, nickname={self.nickname!r}, "
                f"image={self.image!r}, point={self.point!r})")
