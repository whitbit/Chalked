from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class User(db.Model):
    """User of climbing website."""

    __table__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    pw = db.Column(db.String(30), nullable=False)

    def getUserPoints(self):
        """Calculates points accrued based on completed climbs."""

        points = 0

        for log in self.logs:
            if log.completed:
                points += int(log.route.v_grade)
        for review in self.reviews:
            points += 1

        return points

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={}, username={}>".format(self.user_id, self.username)


class Route(db.Model):
    """Route information."""

    __table__ = 'routes'

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location = db.Column(db.String(50))
    v_grade = db.Column(db.String(3))
    url = db.Column(db.Text) # limit to string
    img = db.Column(db.Text) # limit to string

    def __repr__(self):
         """Provide helpful representation when printed."""

         return "<Route id={}, name={}, vgrade={}>".format(self.route_id,
                                                           self.name,
                                                           self.v_grade)


class Review(db.Model):
    """Reviews for climbs."""

    __table__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.user_id))
    route_id = db.Column(db.Integer, db.ForeignKey(routes.route_id))
    date = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    description = db.Column(db.Text)
    photos = db.Column(db.String(500)) 


    user = db.relationship('User', backref=db.backref('reviews'), order_by=date)

    route = db.relationship('Route', backref=db.backref('reviews'), order_by=date)

    def __repr__(self):
         """Provide helpful representation when printed."""

         return "<Review id={}, user_id={}, route_id={}, completed={}>".format(self.review_id
                                                                               self.user_id,
                                                                               self.route_id,
                                                                               self.completed)


class UserLog(db.Model):
    """User's log of completed/in-progress climbs."""

    __table__ = 'logs'

    log_id = db.Column(db.Integer, db.primary_key)
    user_id = db.Column(db.Integer, db.ForeignKey(users.user_id))
    route_id = db.Column(db.Integer, db.ForeignKey(routes.route_id))
    date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    completed = db.Column(db.Boolean)
    photo = db.Column(db.String(500))

    user = db.relationship('User', backref=db.backref('logs'), order_by=date)

    route = db.relationship('Route', backref=db.backref('logs'), order_by=date)

    def __repr__(self):
         """Provide helpful representation when printed."""

         return "<Review id={}, user_id={}, route_id={}, completed={}>".format(self.review_id
                                                                               self.user_id,
                                                                               self.route_id,
                                                                               self.completed)


class UserFavorites(db.Model):
    """Favorite climbs by Users."""

    __table__ = 'user_favorites'

    favorites_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.user_id))
    route_id = db.Column(db.Integer, db.ForeignKey(routes.route_id))

    def __repr__(self):
         """Provide helpful representation when printed."""

         return "<Favorites id={}, user_id={}, route_id={}>".format(self.favorites_id
                                                                    self.user_id,
                                                                    self.route_id)



def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///climbs'
    app.config['SQLCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

connect_to_db(app)