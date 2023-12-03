from application import db 

# database table to store user's information, username, password and date join
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    join_on = db.Column(db.DateTime, nullable=False)
    
# database table to store prediction records
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'),  nullable=True)
    year_purchase = db.Column(db.Integer, nullable=False)
    engine_displacement = db.Column(db.Integer, nullable=False)
    max_power = db.Column(db.DECIMAL(precision=4, scale=1), nullable=False)
    torque = db.Column(db.DECIMAL(precision=5, scale=1), nullable=False)
    brand = db.Column(db.String, nullable=False)
    fuel = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    pred_price = db.Column(db.Integer, nullable=False)
    predict_on = db.Column(db.DateTime, nullable=False)