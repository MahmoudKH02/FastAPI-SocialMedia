# FastAPI Social Media API

A RESTful API for a social media platform built with FastAPI, PostgreSQL, and SQLAlchemy. This API allows users to create posts, vote on posts, and manage user accounts with authentication.

## Features

- **User Management**
  - Create new user accounts
  - Retrieve user information
  - Secure password hashing

- **Post Management**
  - Create, read, update, and delete posts
  - Filter posts by search term
  - Pagination support

- **Voting System**
  - Upvote/downvote posts
  - Prevent duplicate votes

- **Authentication**
  - JWT token-based authentication
  - Protected routes for authenticated users only

- **CORS Support**
  - Configurable CORS policies

## Technologies Used

- Python 3.x
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Passlib (password hashing)
- JWT (authentication)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-social-media.git
   cd fastapi-social-media

 2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Create a .env file based on .env.example and configure your database credentials.
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication
* `POST /login` - Authenticate user and get access token

### Users
* `POST /users` - Create a new user
* `GET /users/{id}` - Get user by ID

### Posts

* `GET /posts` - Get all posts (with optional search filtering)
* `POST /posts` - Create a new post (authenticated)
* `GET /posts/{id}` - Get a specific post
* `PUT /posts/{id}` - Update a post (authenticated, owner only)
* `DELETE /posts/{id}` - Delete a post (authenticated, owner only)

### Votes
* `POST /votes` - Create/remove a vote on a post (authenticated)

## Configuration
The application can be configured through environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

## Database Setup
1. Create a PostgreSQL database
2. Update the connection string in your environment variables
3. The application will automatically create tables on first run

## Testing
To test the API, you can use tools like:

- Postman
- cURL
- FastAPI's built-in Swagger UI at `/docs`
- ReDoc at `/redoc`
