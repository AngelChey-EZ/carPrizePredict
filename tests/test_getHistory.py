import pytest
from flask import json

@pytest.mark.parametrize("en", [
    [1],
])
def test_userHistory(client, en, capsys):
    with capsys.disabled():
        response = client.get(f'/api/get_my_prediction_history/{en[0]}')
        res_data = json.loads(response.get_data(as_text=True))
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        assert len(res_data)
        
@pytest.mark.xfail(reason='invalid user id')
@pytest.mark.parametrize("en", [
    [0],
    [None]
])
def test_userHistory_invalidUser(client, en, capsys):
    test_userHistory(client, en, capsys)
    
# test if getting latest top 5 prediction from database without any filter is successful
def test_recentHist(client, capsys):
    with capsys.disabled():
        response = client.get(f'/api/get_recent')
        res_data = json.loads(response.get_data(as_text=True))
        
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        # should return 5 result
        assert len(res_data) == 5
        assert res_data['0']['predict_on'] > res_data['1']['predict_on']
        assert res_data['1']['predict_on'] > res_data['2']['predict_on']
        assert res_data['2']['predict_on'] > res_data['3']['predict_on']
        assert res_data['3']['predict_on'] > res_data['4']['predict_on']

# test min search
@pytest.mark.parametrize("en", [
    [2015, 'yp_min', 'year_purchase'],
    [1500, 'ed_min', 'engine_displacement'],
    [150, 'mp_min', 'max_power'],
    [300, 't_min', 'torque'],
])
def test_Search_History_min(client, en, capsys, none_Data_for_search):
    with capsys.disabled():
        data = none_Data_for_search
        
        data[en[1]] = en[0]
        response = client.post('/api/search_recent_history', data=json.dumps(data),content_type = 'application/json')
        res_data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        # should return 5 result
        for r in res_data:
            assert float(res_data[r][en[2]]) >= en[0] 
        # check prediction date
        for i in range(len(res_data)-1):
            assert res_data[str(i)]['predict_on'] > res_data[str(i+1)]['predict_on']
            
# test max search
@pytest.mark.parametrize("en", [
    [2010, 'yp_max', 'year_purchase'],
    [1500, 'ed_max', 'engine_displacement'],
    [100, 'mp_max', 'max_power'],
    [100, 't_max', 'torque'],
])
def test_Search_History_max(client, en, capsys, none_Data_for_search):
    with capsys.disabled():
        data = none_Data_for_search
        
        data[en[1]] = en[0]
        response = client.post('/api/search_recent_history', data=json.dumps(data),content_type = 'application/json')
        res_data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        for r in res_data:
            assert float(res_data[r][en[2]]) <= en[0] 
        
        for i in range(len(res_data)-1):
            assert res_data[str(i)]['predict_on'] > res_data[str(i+1)]['predict_on']
            
# min max search test
@pytest.mark.parametrize("en", [
    [2010, 'yp_min', 2020, 'yp_max', 'year_purchase'],
    [1500, 'ed_min', 2000, 'ed_max', 'engine_displacement'],
    [150, 'mp_min', 300, 'mp_max', 'max_power'],
    [100, 't_min', 300, 't_max', 'torque'],
])
def test_Search_History_minmax(client, en, capsys, none_Data_for_search):
    with capsys.disabled():
        data = none_Data_for_search
        
        data[en[1]] = en[0]
        data[en[3]] = en[2]
        response = client.post('/api/search_recent_history', data=json.dumps(data),content_type = 'application/json')
        res_data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        for r in res_data:
            assert float(res_data[r][en[4]]) >= en[0] 
            assert float(res_data[r][en[4]]) <= en[2] 
        
        for i in range(len(res_data)-1):
            assert res_data[str(i)]['predict_on'] > res_data[str(i+1)]['predict_on']
            
# cat search test
@pytest.mark.parametrize("en", [
    ['brands', ['Audi', 'BMW', 'Jaguar']],
    ['fuels', ['Diesel', 'Petrol']],
    ['owners', ['Test_Drive_Car', 'Second_Owner']],
])
def test_Search_History_cat(client, en, capsys, none_Data_for_search):
    with capsys.disabled():
        data = none_Data_for_search
        
        data[en[0]] = en[1]
        response = client.post('/api/search_recent_history', data=json.dumps(data),content_type = 'application/json')
        res_data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        for r in res_data:
            assert res_data[r][en[0]] in en[1]
        
        for i in range(len(res_data)-1):
            assert res_data[str(i)]['predict_on'] > res_data[str(i+1)]['predict_on']
            
# test unfound search
@pytest.mark.parametrize("en", [
    [2050, 'yp_min', 'year_purchase'],
    [5000, 'ed_min', 'engine_displacement'],
    [1000, 'mp_min','max_power'],
    [5000, 't_min', 'torque'],
])
def test_Search_History_max(client, en, capsys, none_Data_for_search):
    with capsys.disabled():
        data = none_Data_for_search
        
        data[en[1]] = en[0]
        response = client.post('/api/search_recent_history', data=json.dumps(data),content_type = 'application/json')
        res_data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        assert len(res_data) == 0