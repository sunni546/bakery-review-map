from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Level(db.Model):
    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    point = db.Column(db.Integer, unique=True, nullable=False)

    users = db.relationship("User", back_populates="level")

    def __repr__(self):
        return f"Level(id={self.id!r}, name={self.name!r}, point={self.point!r})"


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

    interests = db.relationship("Interest", back_populates="user", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"User(id={self.id!r}, email={self.email!r}, password={self.password!r}, nickname={self.nickname!r}, "
                f"image={self.image!r}, point={self.point!r}, level_id={self.level_id!r})")


class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True)

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id', ondelete="CASCADE"))
    bakery = db.relationship("Bakery", back_populates="interests")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    user = db.relationship("User", back_populates="interests")

    def __repr__(self):
        return f"Interest(id={self.id!r}, bakery_id={self.bakery_id!r}, user_id={self.user_id!r})"


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    score = db.Column(db.Integer, nullable=False)

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id', ondelete="CASCADE"))
    bakery = db.relationship("Bakery", back_populates="reviews")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    user = db.relationship("User", back_populates="reviews")

    reviewed_breads = db.relationship("ReviewedBread", back_populates="review", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"Review(id={self.id!r}, content={self.content!r}, image={self.image!r}, score={self.score!r}, "
                f"bakery_id={self.bakery_id!r}, user_id={self.user_id!r})")


class ReviewedBread(db.Model):
    __tablename__ = 'reviewed_breads'

    id = db.Column(db.Integer, primary_key=True)

    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id', ondelete="CASCADE"))
    review = db.relationship("Review", back_populates="reviewed_breads")

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"))
    category = db.relationship("Category", back_populates="reviewed_breads")

    def __repr__(self):
        return f"ReviewedBread(id={self.id!r}, review_id={self.review_id!r}, category_id={self.category_id!r})"


class Bakery(db.Model):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True, comment="빵집 번호")
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Numeric(10, 7), nullable=False)
    lng = db.Column(db.Numeric(10, 7), nullable=False)
    score = db.Column(db.Float, default=0)
    review_number = db.Column(db.Integer, default=0)

    breads = db.relationship("Bread", back_populates="bakery", cascade="all, delete-orphan")
    interests = db.relationship("Interest", back_populates="bakery", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="bakery", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"Bakery(id={self.id!r}, name={self.name!r}, address={self.address!r}, "
                f"lat={self.lat!r}, lng={self.lng!r}, score={self.score!r}, review_number={self.review_number!r})")


class Bread(db.Model):
    __tablename__ = 'breads'

    id = db.Column(db.Integer, primary_key=True)

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id', ondelete="CASCADE"))
    bakery = db.relationship("Bakery", back_populates="breads")

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"))
    category = db.relationship("Category", back_populates="breads")

    def __repr__(self):
        return f"Bread(id={self.id!r}, bakery_id={self.bakery_id!r}, category_id={self.category_id!r})"


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    breads = db.relationship("Bread", back_populates="category", cascade="all, delete-orphan")
    reviewed_breads = db.relationship("ReviewedBread", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Category(id={self.id!r}, name={self.name!r})"
