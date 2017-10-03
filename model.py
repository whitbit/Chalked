from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User of climbing website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    pw = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    gender = db.Column(db.String(30))

    def getUserPoints(self):
        """Calculates points accrued based on completed climbs."""

        points = 10

        for log in self.logs:
            if log.completed:
                points += (1 + log.route.v_grade)

        return points

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={}, username={}>".format(self.user_id, self.username)


class Route(db.Model):
    """Route information."""

    __tablename__ = 'routes'

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    state = db.Column(db.String(100))
    area = db.Column(db.String(100))
    v_grade = db.Column(db.Integer)
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))

    def getOverallRating(self):

        sum = 0

        if self.logs:

            for log in self.logs:
                sum += log.rating

        rating = float(sum / len(self.logs))

        return rating

    def __repr__(self):
         """Provide helpful representation when printed."""

         return "<Route id={}, vgrade={}>".format(self.route_id,
                                                  self.v_grade)


class UserLog(db.Model):
    """User's log of completed/in-progress climbs."""

    __tablename__ = 'logs'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    date = db.Column(db.DateTime)
    notes = db.Column(db.Text, default='No notes logged!')
    rating = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(500))

    user = db.relationship('User', backref=db.backref('logs'), order_by=date)

    route = db.relationship('Route', backref=db.backref('logs'), order_by=date)

    def __repr__(self):
         """Provide helpful representation when printed."""

         return "<Review id={}, user_id={}, route_id={}, completed={}>".format(self.review_id,
                                                                               self.user_id,
                                                                               self.route_id,
                                                                               self.completed)

class UserFavorites(db.Model):
    """Favorite climbs by Users."""

    __tablename__ = 'user_favorites'

    favorites_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))

    def __repr__(self):
         """Provide helpful representation when printed."""

         return "<Favorites id={}, user_id={}, route_id={}>".format(self.favorites_id,
                                                                    self.user_id,
                                                                    self.route_id)


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///vroutes'
    app.config['SQLCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."

