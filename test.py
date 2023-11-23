import pytest
from app import app, db, User, Movie


# Setup the Flask test client and init the database
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        db.drop_all()


# Helper function to login a user
def login(client, username, password):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


# Helper function to logout a user
def logout(client):
    return client.get("/logout", follow_redirects=True)


# Helper function to create a user
def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


# Helper function to create a movie
def create_movie(title, year):
    movie = Movie(title=title, year=year)
    db.session.add(movie)
    db.session.commit()
    return movie


# Parametrized test for user login
@pytest.mark.parametrize(
    "username, password, expected",
    [
        # Happy path test cases
        ("testuser", "testpassword", b"Login success."),
        # Error cases
        ("wronguser", "testpassword", b"Invalid username or password."),
        ("testuser", "wrongpassword", b"Invalid username or password."),
        # Edge cases
        ("", "testpassword", b"Invalid input."),
        ("testuser", "", b"Invalid input."),
    ],
    ids=[
        "happy-login",
        "error-wrong-username",
        "error-wrong-password",
        "edge-empty-username",
        "edge-empty-password",
    ],
)
def test_login(client, username, password, expected):
    # Arrange
    create_user("testuser", "testpassword")

    # Act
    response = login(client, username, password)

    # Assert
    assert expected in response.data


# Parametrized test for user logout
@pytest.mark.parametrize(
    "setup, expected",
    [
        # Happy path test case
        (True, b"Goodbye."),
        # Error case (user not logged in)
        (False, b"You should be redirected automatically to target URL: /login."),
    ],
    ids=["happy-logout", "error-not-logged-in"],
)
def test_logout(client, setup, expected):
    # Arrange
    if setup:
        create_user("testuser", "testpassword")
        login(client, "testuser", "testpassword")

    # Act
    response = logout(client)

    # Assert
    assert expected in response.data


# Parametrized test for creating a movie
@pytest.mark.parametrize(
    "title, year, expected",
    [
        # Happy path test cases
        ("New Movie", "2023", b"Item created."),
        # Error cases
        ("", "2023", b"Invalid input."),
        ("New Movie", "", b"Invalid input."),
        # Edge cases
        ("New Movie" * 10, "2023", b"Invalid input."),  # Title too long
        ("New Movie", "20", b"Invalid input."),  # Year too short
    ],
    ids=[
        "happy-create-movie",
        "error-empty-title",
        "error-empty-year",
        "edge-long-title",
        "edge-short-year",
    ],
)
def test_create_movie(client, title, year, expected):
    # Arrange
    create_user("testuser", "testpassword")
    login(client, "testuser", "testpassword")

    # Act
    response = client.post(
        "/", data=dict(title=title, year=year), follow_redirects=True
    )

    # Assert
    assert expected in response.data


# Parametrized test for editing a movie
@pytest.mark.parametrize(
    "new_title, new_year, movie_id, expected",
    [
        # Happy path test case
        ("Edited Movie", "2021", 1, b"Item updated."),
        # Error cases
        ("", "2021", 1, b"Invalid input."),
        ("Edited Movie", "", 1, b"Invalid input."),
        # Edge cases
        ("Edited Movie" * 10, "2021", 1, b"Invalid input."),  # Title too long
        ("Edited Movie", "21", 1, b"Invalid input."),  # Year too short
    ],
    ids=[
        "happy-edit-movie",
        "error-empty-new-title",
        "error-empty-new-year",
        "edge-long-new-title",
        "edge-short-new-year",
    ],
)
def test_edit_movie(client, new_title, new_year, movie_id, expected):
    # Arrange
    create_user("testuser", "testpassword")
    login(client, "testuser", "testpassword")
    movie = create_movie("Original Movie", "2020")

    # Act
    response = client.post(
        f"/movie/edit/{movie.id}",
        data=dict(title=new_title, year=new_year),
        follow_redirects=True,
    )

    # Assert
    assert expected in response.data


# Parametrized test for deleting a movie
@pytest.mark.parametrize(
    "movie_id, expected",
    [
        # Happy path test case
        (1, b"Item deleted."),
        # Error case (movie does not exist)
        (999, b"404 Not Found"),
    ],
    ids=["happy-delete-movie", "error-movie-not-found"],
)
def test_delete_movie(client, movie_id, expected):
    # Arrange
    create_user("testuser", "testpassword")
    login(client, "testuser", "testpassword")
    movie = create_movie("Movie to Delete", "2020")

    # Act
    response = client.post(f"/movie/delete/{movie.id}", follow_redirects=True)

    # Assert
    assert expected in response.data


# Parametrized test for 404 page
@pytest.mark.parametrize(
    "url, expected",
    [
        # Happy path test case
        ("/nonexistent", b"404 Not Found"),
    ],
    ids=["happy-404-page"],
)
def test_404_page(client, url, expected):
    # Act
    response = client.get(url)

    # Assert
    assert expected in response.data
