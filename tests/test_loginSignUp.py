from application.dbTables import Users 
import pytest
from flask import json


# invalid entry, min length, more than max less
@pytest.mark.xfail(reason='unacceptanle length')
@pytest.mark.parametrize("entrylist", [
    ['12345678901234567890123', '12345678901234567890123'],
    ['123', '123']
])
def test_invalidData(entrylist, capsys):
    with capsys.disabled():
        login = Users(userName= entrylist[0],password= entrylist[1])
        assert login.userName == entrylist[0]
        assert login.password == entrylist[1]

# test login ------------------------------------------------------------------------------------------------------------

# unfound user, unmatch username and password
# sucess login,  match username and password
@pytest.mark.parametrize("entrylist", [
    ['notExistUsername', 'notExistPassword', None],
    ['testUsername', 'testUsername', 1]
])
def test_login(client, entrylist, capsys):
    with capsys.disabled():
        user = {
            'userName': entrylist[0],
            'password': entrylist[1]
        }
        response = client.post('/api/login', data = json.dumps(user), content_type = 'application/json')
        response_body = json.loads(response.get_data())
        assert response_body['id'] == entrylist[2]
        
# test sign up ------------------------------------------------------------------------------------------------------------
# duplicate user record
@pytest.mark.xfail(reason='duplicate user record')
@pytest.mark.parametrize("entrylist", [
    ['testUsername', 'testUsername', 'duplicate entry, unable to proceed']
])
def test_signup(client, entrylist, capsys):
    with capsys.disabled():
        user = {
            'userName': entrylist[0],
            'password': entrylist[1]
        }
        response = client.post('/api/signup', data = json.dumps(user), content_type = 'application/json')
        response_body = json.loads(response.get_data())
        assert response_body['error'] == entrylist[2]
        assert response_body['id'] 
        
        # delete user if sucessfully added to let the test repeatable
        if response_body['id'] != None :
            res2 = client.get(f'/api/delete/{response_body['id']}')
        
            assert res2.status_code == 200
            assert res2.headers['Content-Type'] == 'application/json'
            response2_body = json.loads(res2.get_data(as_text=True))
            assert response2_body['result'] == 'ok'
        
# success signup
@pytest.mark.parametrize("entrylist", [
    ['newUser', 'newUser' , None],
])
def test_successSignup(client, entrylist, capsys):
    test_signup(client, entrylist, capsys)
