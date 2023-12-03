from flask import Flask
import pickle
from flask_sqlalchemy import SQLAlchemy

# craete app
app = Flask(__name__)
db = SQLAlchemy()

# load config
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    from .dbTables import Users, Prediction
    db.create_all()
    db.session.commit()
    print('Created Database!')

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)

model_file = "./application/static/models/model.pkl"
oneHot_fille = "./application/static/models/oneHot.pkl"
ordCoder_fille = "./application/static/models/ordCoder.pkl"
scaler_fille = "./application/static/models/scaler.pkl"

# loading models
with open(model_file, 'rb') as f: 
    model = pickle.load(f) 
with open(oneHot_fille, 'rb') as f: 
    oneHot = pickle.load(f) 
with open(ordCoder_fille, 'rb') as f: 
    ordCoder = pickle.load(f)
with open(scaler_fille, 'rb') as f: 
    scaler = pickle.load(f) 

from application import routes