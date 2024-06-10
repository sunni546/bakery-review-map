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

    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    level = db.relationship("Level", back_populates="users")

    def __repr__(self):
        return (f"User(id={self.id!r}, email={self.email!r}, password={self.password!r}, nickname={self.nickname!r}, "
                f"image={self.image!r}, point={self.point!r}, level_id={self.level_id!r})")


class Level(db.Model):
    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    point = db.Column(db.Integer, unique=True, nullable=False)

    users = db.relationship("User", back_populates="level")

    def __repr__(self):
        return f"Level(id={self.id!r}, name={self.name!r}, point={self.point!r})"


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return f"Category(id={self.id!r}, name={self.name!r})"
