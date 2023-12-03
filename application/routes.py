from application import app, db, model, oneHot, ordCoder, scaler
from flask import render_template, flash, request, session, json, jsonify, redirect
from application.forms import LoginForm, SignUpForm, PredictForm, SearchForm
from .dbTables import Users, Prediction
from sqlalchemy import and_
from datetime import datetime, timezone
import numpy as np

# access home/index page
@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
@app.route('/index')
def index_page():
    form = PredictForm()
    if session.get('Logined') != True:
        flash('Warning: You are not a login user. Sign up/login to save your prediction as historical prediction!', 'danger')
    return render_template('index.html', form=form)

# login page
@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

# process login request
@app.route('/loginProcess', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            userName = form.userName.data
            password = form.password.data
            # check if userName and password correct
            id = login_getid(userName, password)
            
            if id != None:
                session['Logined']=True
                session['id']=id
                return redirect("/")
            else:
                flash('Incorrect user name or password', 'danger')
        else: 
            flash("Error, cannot proceed with prediction","danger") 
        return render_template('login.html', form=form)
    
def login_getid(userName, password):
    return db.session.execute(db.select(Users.id).where(Users.userName == userName, Users.password==password)).scalar()

# login api
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data['userName']
    password = data['password']
    id = login_getid(username, password)
    return jsonify({'id': id})

@app.route('/logout')
def logout_page():
    # clear session storage
    session['Logined'] = False
    session['id'] = None
    return redirect('/')

# load signup page
@app.route('/signUp')
def signUp_page():
    form = SignUpForm()
    return render_template('signUp.html', form=form)

# processing signup
@app.route('/signUpProcess', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            userName = form.userName.data
            password = form.password.data
            new_user = Users(
                userName = userName,
                password = password,
                join_on = datetime.utcnow())
            # verify if there is duplicate user
            id = login_getid(userName, password)
            if id == None:
                add_user(new_user)
                
            else:
                flash("Your username and password had been taken, try another one!", 'danger')
                return render_template('signUp.html', form=form)
        else: 
            flash("Error, cannot proceed with your sign up request","danger") 
            return render_template('signUp.html', form=form)
    return render_template('login.html', form=form)

# function to add user
def add_user(new_user):
    try:
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully signed up!", "success")
        return new_user.id
    except Exception as error:
        db.session.rollback()
        flash(error, 'danger')
        
# api for sign up
@app.route('/api/signup', methods=['POST'])
def api_signUp():
    data = request.get_json()
    username = data['userName']
    password = data['password']
    new_user = Users(
                userName = username,
                password = password,
                join_on = datetime.utcnow())
    id = login_getid(username, password)
    if id is None:
        result_id = add_user(new_user)
        return jsonify({'id': result_id, 'error': None})
    
    return jsonify({'id': None, 'error': 'duplicate entry, unable to proceed'})


# api use to remove user during testing
@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id): 
    user = remove_user(int(id))
    return jsonify({'result':'ok'})
def remove_user(id):
    try:
        # entry = Entry.query.grt(id) # version 2
        entry = db.get_or_404(Users, id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, 'danger')
        return 0
    
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    if request.method == 'POST':
        if form.validate_on_submit() and validateForm(form):
            year_purchase = form.year_purchase.data
            brand = dict(form.brand.choices).get(form.brand.data)
            fuel = dict(form.fuel.choices).get(form.fuel.data)
            owner = dict(form.owner.choices).get(form.owner.data)
            # convert data if unit used by user is not same as the one model and database use
            engine_displacement, max_power, torque = convertUnit(form)
            if session.get('id') == True:
                userID = session['id']
            else:
                userID = None
            
            x = np.array([year_purchase, engine_displacement, max_power, torque, brand, fuel, owner])
            # perform data transformation for the model to predict
            x = dataTransform(x)
            
            pred_price = model.predict(x)
            new_predict = Prediction(
                userID = userID,
                year_purchase = year_purchase,
                engine_displacement = int(engine_displacement),
                max_power = max_power,
                torque = torque,
                brand = brand,
                fuel = fuel,
                owner = owner,
                pred_price = int(pred_price[0]),
                predict_on=datetime.now(timezone.utc))
            
            # add record to database
            addPredEntry(new_predict)
            flash(f"Predicted Resale Price: ${int(pred_price[0])}", "success")
        else:
            flash("Error, cannot proceed with prediction","danger")
    if session.get('Logined') != True:
        flash('Warning: You are not a login user. Sign up/login to save your prediction as historical prediction!', 'danger')
    return render_template("index.html", form=form, index=True) 
            
# custom validation for changing of units
def validateForm(form):
    good = True
    value1 = form.engine_displacement.data
    value2 = form.max_power.data
    value3 = form.torque.data
    if(form.engine_unit.data=='1'):
        if(value1 < 100 or value1 > 4500):
            good = False
            form.engine_displacement.errors.append('Number must be between 100 and 4500 for unit cubic centimeter(cc)!')
    else:
        if(value1 <0.1 or value1 >5.0):
            good = False
            form.engine_displacement.errors.append('Number must be between 0.1 and 5.0 for unit liter(L)!')
    
    if(form.max_power_unit.data == '1'):
        if(value2 < 30 or value2 > 600):
            good = False
            form.max_power.errors.append('Number must be between 30 and 600 for unit hourse power(hp)!')
    else:
        if(value2 <22.3 or value2 >450):
            good = False
            form.max_power.errors.append('Number must be between 22.3 and 450 for unit kilowatts(kw)!')
    
    if(form.torque_unit.data == '1'):
        if(value3 < 30 or value3 > 3500):
            good = False
            form.torque.errors.append('Number must be between 30 and 3500 for unit newton meter(Nm)!')
    else:
        if(value3 <3 or value3 >360):
            good = False
            form.torque.errors.append('Number must be between 3 and 360 for unit kilogram force meter(kgm)!')
            
    return good

# convert value to unit that is used by model and database
def convertUnit(form):
    if(form.engine_unit.data == '1'): en = form.engine_displacement.data 
    else: en = form.engine_displacement.data * 1000
        
    if(form.max_power_unit.data == '1'): mp = form.max_power.data
    else:
        # 1kw = 1000watts, 745.7watts = 1hp
        mp = float(form.max_power.data) * 1000 / 745.7
    
    # 9.81nm = 1kgm
    if(form.torque_unit.data == '1'): t = form.torque.data 
    else: t = float(form.torque.data) * 9.81
        
    return en, mp, t

# perform data transformation for model prediction
def dataTransform(data):
    owner = ordCoder.transform(np.array(data[-1]).reshape(-1,1))[0]
    cat = oneHot.transform(data[4:-1].reshape(-1,2))[0]
    num = scaler.transform(data[:4].reshape(-1, 4))[0]
    x = np.concatenate([num, cat, owner], axis=0).reshape(1, -1)
    return x

# add prediction record to db after predict
def addPredEntry(new_predict):
    try:
        db.session.add(new_predict)
        db.session.commit()
        return new_predict.id 
    except Exception as error:
        db.session.rollback()
        flash(error, 'danger')
        
# api to add predict record
@app.route("/api/addPred", methods=['POST'])
def api_addPred():
    # retrive the json file posted from client
    data = request.get_json()
    # retrive each field from the data
    year_purchase = data['year_purchase']
    engine_displacement = data['engine_displacement']
    max_power = data['max_power']
    torque = data['torque']
    brand = data['brand']
    fuel = data['fuel']
    owner = data['owner']
    pred_price = data['pred_price']
    userID = data['userID']
    
    # create an Entry object store all data for db action
    new_entry = Prediction(year_purchase=year_purchase, engine_displacement=engine_displacement,
                      max_power=max_power, torque=torque, brand=brand, fuel=fuel, owner=owner,
                      pred_price=pred_price, userID=userID,
                      predict_on=datetime.utcnow())
    result = addPredEntry(new_entry)
    return jsonify({'id': result})

# api to delete prediction record, used for testing
@app.route("/api/delete_pred/<id>", methods=['GET'])
def api_delete_pred(id): 
    pred = remove_pred(int(id))
    return jsonify({'result':'ok'})
def remove_pred(id):
    try:
        entry = db.get_or_404(Prediction, id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, 'danger')
        return 0

# api to predict, get back predicted price
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    pre_input = np.array([data['year_purchase'], data['engine_displacement'], data['max_power'], data['torque'], data['brand'], data['fuel'], data['owner']])
    pre_input = dataTransform(pre_input)
    price = model.predict(pre_input)
    
    return jsonify({'pre_price': int(price[0])})
    
# my history page
@app.route('/MypredictionHistory', methods=['GET'])
def myPredHistory_Page():
    if session.get('id') == True:
        userID = session['id']
        return render_template("preHistory.html", index=True, records=get_my_predictions(userID)) 
    else:
        userID = None
        form=PredictForm()
        flash('Log in to view your prediction history', 'danger')
        return render_template('index.html', form=form, index=True)
    
# get all user's prediction result
def get_my_predictions(id):
    try:
        return db.session.query(Prediction).filter(Prediction.userID == id).order_by(Prediction.predict_on.desc()).all()
    except Exception as error:
        db.session.rollback()
        flash(error, 'danger')
        return 0

# api to get user's history using user's id
@app.route('/api/get_my_prediction_history/<id>',  methods=['GET', 'POST'])
def api_get_my_history(id):
    history = get_my_predictions(int(id))
    data = {}
    i = 0
    # loop to convert to json/dictionary format
    for hist in history:
        h = {'id' : hist.id,
            'userID': hist.userID,
            'year_purchase': hist.year_purchase,
            'engine_displacement': hist.engine_displacement,
            'max_power' : hist.max_power, 
            'torque' : hist.torque,
            'brand' : hist.brand,
            'fuel' : hist.fuel,
            'owner': hist.owner,
            'pre_price': hist.pred_price,
            'predict_on': hist.predict_on}
        data[str(i)]  = h
        i += 1
    result = jsonify(data)
    return result 

# get latest top 5 prediction record from database
@app.route('/mostRecentPredictionHistory',  methods=['GET'])
def recentPred_Page():
    form = SearchForm()
    filters = []
    return render_template('recentPred.html', form = form, records=filtered_search(filters))

# process filter/search on getting latest top 5 prediction record from database
@app.route('/search', methods=['GET', 'POST'])
def search_Pred():
    form = SearchForm()
    filters=[]
    if request.method == 'POST':
        if form.validate_on_submit() and validateSearchForm(form):
            yp_min = form.yp_min.data
            yp_max = form.yp_max.data
            # for cat data, loop through all selected data and push to a list waiting for process
            brands = []
            if(form.brand.data):
                for b in form.brand.data:
                    brands.append(dict(form.brand.choices).get(b))
                    
            fuels = []
            if(form.fuel.data):
                for f in form.fuel.data:
                    fuels.append(dict(form.fuel.choices).get(f))
            
            owners = []
            if(form.owner.data):
                for o in form.owner.data:
                    owners.append(dict(form.owner.choices).get(o))
            
            # convert numeric data if for unit not used for model and database
            ed_min, ed_max, mp_min, mp_max, t_min, t_max = convertUnit_minmax(form)
            # format all condition to push to sql filter quary
            filters = formatFilter(yp_min, yp_max, ed_min, ed_max, mp_min, mp_max, t_min, t_max, brands, fuels, owners)
                    
        else:
            flash("Error, cannot proceed with searching","danger")
    return render_template("recentPred.html", form=form, records=filtered_search(filters)) 

# format filtering condition
def formatFilter(yp_min, yp_max, ed_min, ed_max, mp_min, mp_max, t_min, t_max, brands, fuels, owners):
    filters = []
    if (yp_min):
        filters.append(Prediction.year_purchase >= yp_min)
    if (yp_max):
        filters.append(Prediction.year_purchase <= yp_max)
        
    if (ed_min):
        filters.append(Prediction.engine_displacement >= ed_min)
    if (ed_max):
        filters.append(Prediction.engine_displacement <= ed_max)
        
    if (mp_min):
        filters.append(Prediction.max_power >= mp_min)
    if (mp_max):
        filters.append(Prediction.max_power <= mp_max)
        
    if (t_min):
        filters.append(Prediction.torque >= t_min)
    if (t_max):
        filters.append(Prediction.torque <= t_max)
        
    if(brands):
        for b in brands:
            filters.append(Prediction.brand == b)
    if(fuels):
        for b in fuels:
            filters.append(Prediction.fuel == b)
    if(owners):
        for b in owners:
            filters.append(Prediction.owner == b)
    return filters
    
# check if min < than max, if not push error
def validateSearchForm(form):
    good = True
    err = 'Minimum cannot be larger than maximum!'
    if(form.yp_min.data and form.yp_max.data):
        if(form.yp_min.data > form.yp_max.data):
            good = False
            form.yp_min.errors.append(err)
        
    if(form.ed_min.data and form.ed_max.data):
        if(form.ed_min.data > form.ed_max.data):
            good = False
            form.ed_min.errors.append(err)
        
    if(form.mp_min.data and form.mp_max.data):
        if(form.mp_min.data > form.mp_max.data):
            good = False
            form.mp_min.errors.append(err)
        
    if(form.t_min.data and form.t_max.data):
        if(form.t_min.data > form.t_max.data):
            good = False
            form.t_min.errors.append(err)
    return good
    
# convert data for fields' unit not same with the one as the model and database use
def convertUnit_minmax(form):
    ed_min=None
    ed_max=None
    mp_min=None
    mp_max=None
    t_min=None
    t_max=None
    if(form.engine_unit.data == '1'): 
        if(form.ed_min.data):
            ed_min = form.ed_min.data 
        if(form.ed_max.data):
            ed_max = form.ed_max.data 
    else: 
        if(form.ed_min.data):
            ed_min = form.ed_min.data * 1000
        if(form.ed_max.data):
            ed_max = form.ed_max.data * 1000
        
    if(form.max_power_unit.data == '1'): 
        if(form.mp_min.data):
            mp_min = form.mp_min.data 
        if(form.mp_max.data):
            mp_max = form.mp_max.data 
    else:
        if(form.mp_min.data):
            print(form.mp_min.data)
            mp_min = float(form.mp_min.data) * 1000 / 745.7 
        if(form.mp_max.data):
            mp_max = float(form.mp_max.data) * 1000 / 745.7
        # 1kw = 1000watts, 745.7watts = 1hp
    
    # 9.81nm = 1kgm
    if(form.torque_unit.data == '1'): 
        if(form.t_min):
            t_min = form.t_min.data 
        if(form.t_max):
            t_max = form.t_max.data
    else: 
        if(form.t_min):
            t_min = float(form.t_min.data) * 9.81 
        if(form.t_max):
            t_max = float(form.t_max.data) * 9.81
        
    return ed_min, ed_max, mp_min, mp_max, t_min, t_max

# sql quary to select base on filter condition
def filtered_search(filters):
    try:
        return db.session.query(Prediction).filter(and_(*filters)).order_by(Prediction.predict_on.desc()).limit(5).all()
    except Exception as error:
        db.session.rollback()
        flash(error, 'danger')
        return 0

# api to get latest top 5 prediction records in database
@app.route('/api/get_recent',  methods=['GET'])
def api_get_recent_history():
    filter = []
    history = filtered_search(filter)
    data = {}
    i = 0
    for hist in history:
        h = {'id' : hist.id,
            'userID': hist.userID,
            'year_purchase': hist.year_purchase,
            'engine_displacement': hist.engine_displacement,
            'max_power' : hist.max_power, 
            'torque' : hist.torque,
            'brand' : hist.brand,
            'fuel' : hist.fuel,
            'owner': hist.owner,
            'pre_price': hist.pred_price,
            'predict_on': hist.predict_on}
        data[str(i)]  = h
        i += 1
    
    result = jsonify(data)
    return result 

# api to get latest top 5 prediction record base on filter condition
@app.route('/api/search_recent_history', methods=['GET', 'POST'])
def api_search_recent_history():
    data = request.get_json()
    yp_min = data['yp_min']
    yp_max = data['yp_max']
    ed_min = data['ed_min']
    ed_max = data['ed_max']
    mp_min = data['mp_min']
    mp_max = data['mp_max']
    t_min = data['t_min']
    t_max = data['t_max']
    brands = data['brands']
    fuels = data['fuels']
    owners = data['owners']
    
    filter = formatFilter(yp_min, yp_max, ed_min, ed_max, mp_min, mp_max, t_min, t_max, brands, fuels, owners)
    history = filtered_search(filter)
    data = {}
    i = 0
    for hist in history:
        h = {'id' : hist.id,
            'userID': hist.userID,
            'year_purchase': hist.year_purchase,
            'engine_displacement': hist.engine_displacement,
            'max_power' : hist.max_power, 
            'torque' : hist.torque,
            'brand' : hist.brand,
            'fuel' : hist.fuel,
            'owner': hist.owner,
            'pre_price': hist.pred_price,
            'predict_on': hist.predict_on}
        data[str(i)]  = h
        i += 1
    
    result = jsonify(data)
    return result 








