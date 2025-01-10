import pytest
from pizzaProject import app, initialize_database

#testing overall website functionality
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#pages
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Pizza Application" in response.data
    assert b"Manager Page" in response.data 
    assert b"Chef Page" in response.data   

def test_invalid_route(client):
    response = client.get('/invalid-route')
    assert response.status_code == 404
    assert b"404 Not Found" in response.data

def test_manager_page(client):
    response = client.get('/manager')
    assert response.status_code == 200
    assert b"Manage Pizza Toppings" in response.data  

def test_chef_page(client):
    response = client.get('/chef')
    assert response.status_code == 200
    assert b"Manage Pizzas" in response.data   

#testing database init
def test_initialize_database():
    initialize_database()

#testing text input with SQL injection
def test_sql_injection_on_manager_page(client):
    injection_payload = "' OR '1'='1' --"

    response = client.post('/manager', data={'newTopping': injection_payload})

    assert response.status_code == 200
    assert b"Manage Pizza Toppings" in response.data  
    assert b"Invalid or empty selected topping and/or new topping." not in response.data 

def test_sql_injection_on_chef_page(client):
    injection_payload = "' OR '1'='1' --"

    response = client.post('/chef', data={'newPizzaName': injection_payload})

    assert response.status_code == 200
    assert b"Manage Pizzas" in response.data  
    assert b"Invalid pizza name or toppings." not in response.data 