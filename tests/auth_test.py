from app.auth.forms import login_form, register_form, profile_form, security_form, user_edit_form

"""This test the homepage"""

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200
    
def test_success_register_login_logout(client, application):
    assert client.get("/register").status_code == 200
    response = client.post("/register", data={"email": "test@example.com", "password": "abcdef", "confirm": "abcdef"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdef"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_dashboard_access(client, application):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login?next=%2Fdashboard" == response.headers["Location"]
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdef"})
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b'Welcome' in response.data
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_invalid_login(client, application):
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdeg"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
    response = client.post("/login", data={"email": "test@example.co", "password": "abcdef"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_already_registered(client, application):
    response = client.post("/register", data={"email": "test@example.com", "password": "abcdef", "confirm": "abcdef"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
    assert b'Already Registered' in client.get("/register", data={"email": "test@example.com", "password": "abcdef", "confirm": "abcdef"}).data


