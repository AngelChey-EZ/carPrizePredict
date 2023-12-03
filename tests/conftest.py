import pytest
from application import app as flask_app

@pytest.fixture
def app():
    yield flask_app
    
@pytest.fixture
def client(app):
    print(app.static_url_path)
    return app.test_client()

@pytest.fixture
def none_Data_for_search():
    data = {
            'yp_min' : None,
            'yp_max' : None,
            'ed_min' : None,
            'ed_max' : None,
            'mp_min' : None,
            'mp_max' : None,
            't_min' : None,
            't_max' : None,
            'brands' :None,
            'fuels' : None,
            'owners' : None,
        }
    return data
