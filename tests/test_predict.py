from application.dbTables import Prediction
import pytest
from flask import json

# expected fail entry
@pytest.mark.xfail(reason='missing value and wrong userID')
@pytest.mark.parametrize("entrylist", [
    [None, 1000, 54, 34, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, None, 54, 34, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, 1000, None, 34, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, 1000, 54, None, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, 1000, 54, 34, None, 'Petrol', 'First_Owner', None],
    [2020, 1000, 54, 34, 'Ford', None, 'First_Owner', None],
    [2020, 1000, 54, 34, 'Ford', 'Petrol', None, None],
    [2020, 1000, 54, 34, 'Ford', 'Petrol', 'First_Owner', 7]
])
def test_Data(entrylist, capsys):
    with capsys.disabled():
        pred = Prediction(
            year_purchase= entrylist[0],
            engine_displacement= entrylist[1],
            max_power= entrylist[2],
            torque= entrylist[3],
            brand= entrylist[4],
            fuel= entrylist[5],
            owner= entrylist[6],
            userID = entrylist[7]
            )
        assert pred.year_purchase == entrylist[0]
        assert pred.engine_displacement== entrylist[1]
        assert pred.max_power== entrylist[2]
        assert pred.torque== entrylist[3]
        assert pred.brand== entrylist[4]
        assert pred.fuel== entrylist[5]
        assert pred.owner== entrylist[6]
        assert pred.userID == entrylist[7]

# testing on success entry
@pytest.mark.parametrize("entrylist", [
    [2000, 1000, 54, 34, 'Ford', 'Petrol', 'First_Owner', 1],
    [2020, 1000, 54, 34, 'Ford', 'Petrol', 'First_Owner', None]
])
def test_sucess(entrylist, capsys):
    test_Data(entrylist, capsys)
    
# out of range entry 
@pytest.mark.xfail(reason='values out of range')
@pytest.mark.parametrize("entrylist", [
    [1900, 1000, 54, 34, 'Ford', 'Petrol', 'First_Owner', 1],
    [2025, 1000, 54, 34, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, 50, 54, 34, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, 5000, 54, 34, 'Ford', 'Petrol', 'First_Owner', 1],
    [2020, 1000, 20, 34, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, 1000, 700, 34, 'Ford', 'Petrol', 'First_Owner', 1],
    [2020, 1000, 54, 20, 'Ford', 'Petrol', 'First_Owner', None],
    [2020, 1000, 54, 5000, 'Ford', 'Petrol', 'First_Owner', 1]
    
])
def test_outOfRange(entrylist, capsys):
    test_Data(entrylist, capsys)
    
# test invald range for different unit, edited validateForm function from route
# so that could directly insert data
@pytest.mark.parametrize("en", [
    [50, '1', 54, '1', 50, '1', 'Number must be between 100 and 4500 for unit cubic centimeter(cc)!'],
    [5000, '1', 54, '1', 50, '1', 'Number must be between 100 and 4500 for unit cubic centimeter(cc)!'],
    [0.05, '2', 54, '1', 50, '1', 'Number must be between 0.1 and 5.0 for unit liter(L)!'],
    [6.0, '2', 54, '1', 50, '1', 'Number must be between 0.1 and 5.0 for unit liter(L)!'],
    [1000, '1', 20, '1', 50, '1', 'Number must be between 30 and 600 for unit hourse power(hp)!'],
    [1000, '1', 700, '1', 50, '1', 'Number must be between 30 and 600 for unit hourse power(hp)!'],
    [1000, '1', 20, '2', 50, '1', 'Number must be between 22.3 and 450 for unit kilowatts(kw)!'],
    [1000, '1', 500, '2', 50, '1', 'Number must be between 22.3 and 450 for unit kilowatts(kw)!'],
    [1000, '1', 54, '1', 20, '1', 'Number must be between 30 and 3500 for unit newton meter(Nm)!'],
    [1000, '1', 54, '1', 4000, '1', 'Number must be between 30 and 3500 for unit newton meter(Nm)!'],
    [1000, '1', 54, '1', 2, '2', 'Number must be between 3 and 360 for unit kilogram force meter(kgm)!'],
    [1000, '1', 54, '1', 400, '2', 'Number must be between 3 and 360 for unit kilogram force meter(kgm)!'],
    
])
def test_withDiffUnit(en):
    errors = []
    value1 = en[0]
    value2 = en[2]
    value3 = en[4]
    if(en[1]=='1'):
        if(value1 < 100 or value1 > 4500):
            errors.append('Number must be between 100 and 4500 for unit cubic centimeter(cc)!')
    else:
        if(value1 <0.1 or value1 >5.0):
            errors.append('Number must be between 0.1 and 5.0 for unit liter(L)!')
    
    if(en[3] == '1'):
        if(value2 < 30 or value2 > 600):
            errors.append('Number must be between 30 and 600 for unit hourse power(hp)!')
    else:
        if(value2 <22.3 or value2 >450):
            errors.append('Number must be between 22.3 and 450 for unit kilowatts(kw)!')
    
    if(en[5] == '1'):
        if(value3 < 30 or value3 > 3500):
            errors.append('Number must be between 30 and 3500 for unit newton meter(Nm)!')
    else:
        if(value3 <3 or value3 >360):
            errors.append('Number must be between 3 and 360 for unit kilogram force meter(kgm)!')
            
    assert errors[0] == en[6]

# test predict api, add predict record api and delete record api
@pytest.mark.parametrize("entrylist", [
    [2000, 1000, 54, 65, 'Toyota', 'Diesel', 'Second_Owner', None, 119175],
    [2020, 1630, 150, 248, 'Kia', 'CNG', 'Second_Owner', 1, 2401034]
])
def test_predentryAPI(client, entrylist, capsys):
    with capsys.disabled():
        input = {
            'year_purchase': entrylist[0],
            'engine_displacement': entrylist[1],
            'max_power': entrylist[2],
            'torque': entrylist[3],
            'brand': entrylist[4],
            'fuel': entrylist[5],
            'owner': entrylist[6],
            'userID': entrylist[7],
        }
        
        res = client.post('/api/predict', data = json.dumps(input), content_type = 'application/json')
        res_body = json.loads(res.get_data())
        assert res_body['pre_price'] == entrylist[8]
        input['pred_price'] = res_body['pre_price']
        
        response = client.post('/api/addPred', data = json.dumps(input), content_type = 'application/json')
        response_body = json.loads(response.get_data())
        assert response_body['id'] 
        
        # delete user if sucessfully added to let the test repeatable
        if response_body['id'] != None :
            res2 = client.get(f'/api/delete_pred/{response_body['id']}')
        
            assert res2.status_code == 200
            assert res2.headers['Content-Type'] == 'application/json'
            response2_body = json.loads(res2.get_data(as_text=True))
            assert response2_body['result'] == 'ok'
    
