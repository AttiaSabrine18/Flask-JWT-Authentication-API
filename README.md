# Flask JWT Authentication API

## Description
This is a RESTful API built with Flask that provides user authentication and management features using JWT (JSON Web Tokens). The application includes endpoints for user login, signup, and fetching users data, all protected by token-based authentication.
## Features

- **User Signup:** Register a new user with a hashed password.
- **User Login:** Authenticate a user and issue a JWT token.
- **Get All Users:** Retrieve a list of all users (requires authentication).

## Technologies Used

- **Flask:** A micro web framework for Python.
- **Flask-CORS:** Middleware for handling Cross-Origin Resource Sharing (CORS).
- **Flask-Bcrypt:** Extension for hashing passwords.
- **Flask-Marshmallow:** Integration of Marshmallow for object serialization.
- **PyJWT:** A library for encoding and decoding JSON Web Tokens.
- **SQLAlchemy:** ORM for database operations.
- **dotenv:** For loading environment variables from a `.env` file.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install the dependencies:**

    ```bash
    pip install flask flask_sqlalchemy flask_marshmallow flask_cors python-dotenv mysql-connector-python flask_bcrypt pyjwt
    ```

5. **Create a `.env` file:**

    ```bash
    SECRET_KEY=your_secret_key
    DATABASE_URI=your_database_uri
    ```

6. **Run the application:**

    ```bash
    python app.py
    ```

## API Endpoints

### `POST /signup`

Registers a new user.

### `POST /login`
Registers a new user.
Responses:
201 Created: Token issued successfully.
401 Unauthorized: Missing email or password.
403 Forbidden: Incorrect password or user does not exist.
GET /user
Fetches all users. Requires a valid JWT token.
logged a  user.
### `POST /user`
Headers:

x-access-token: JWT token

Responses:

200 OK: List of users.
401 Unauthorized: Token is missing or invalid.

