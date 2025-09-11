# The Polls API 🗳️

A simple, fast, and modern RESTful API built with FastAPI and Redis to create, manage, and vote on polls.

-----

## 🚀 Project Overview

**The Polls API** provides a complete backend solution for incorporating a polling system into any application. It allows users to create polls with multiple choices, cast votes, and view real-time results. The API is designed to be efficient and scalable, leveraging the speed of FastAPI for processing requests and Upstash Redis for persistent, low-latency data storage.

### ✨ Key Features

  * [cite\_start]**Create Polls**: Easily create new polls with a title, 2 to 5 choices, and an optional expiration date[cite: 21].
  * [cite\_start]**Vote**: Cast votes on active polls using either a unique choice ID or a simple numerical label[cite: 17, 19].
  * [cite\_start]**View Polls**: Retrieve a single poll by its ID or list all polls with filters for **active**, **expired**, or **all**[cite: 11, 12, 13].
  * [cite\_start]**Real-Time Results**: Get instant poll results, including total votes and a count for each choice, sorted by popularity[cite: 30].
  * [cite\_start]**Data Validation**: Robust data validation powered by Pydantic ensures data integrity and provides clear error messages[cite: 9].
  * [cite\_start]**Duplicate Vote Prevention**: Ensures that a voter (identified by email) can only vote once per poll[cite: 15].
  * [cite\_start]**Danger Zone**: Includes protected operations for irreversible data loss, such as deleting a poll and all its associated votes[cite: 4, 7].

-----

## 🛠️ Technologies & Frameworks

This project is built with a modern Python stack, focusing on performance and developer experience.

| Category             | Technology / Tool                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| **Language** | Python 3.12                                                                                     |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/)                                                        |
| **Database** | [cite\_start][Upstash Redis](https://upstash.com/redis) (for data storage) [cite: 26]                        |
| **Data Validation** | [Pydantic](https://docs.pydantic.dev/latest/)                                                   |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/)                                                             |
| **Dependency Mgmt.** | [uv](https://github.com/astral-sh/uv)                                                           |

-----

## 🔧 Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites

  * **Python 3.12+**
  * **Git**
  * **`uv`** (Python package installer). If you don't have it, install it with:
    ```bash
    pip install uv
    ```
  * **Upstash Redis Account**: You will need a Redis database URL and token. You can get one for free at [Upstash](https://upstash.com/).

### Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/suraj-yadav-aiml/the-polls-api.git
    cd the-polls-api
    ```

2.  **Create a virtual environment and install dependencies:**
    The project uses `uv` for fast dependency management. This command creates a virtual environment and installs all packages from `pyproject.toml`.

    ```bash
    uv sync
    ```

3.  **Activate the virtual environment:**

    ```bash
    source .venv/bin/activate
    # On Windows, use: .venv\Scripts\activate
    ```

4.  **Configure environment variables:**
    Create a `.env` file by copying the example file.

    ```bash
    cp .env.example .env
    ```

    Now, open the `.env` file and add your Upstash Redis credentials.

    ```env
    REDIS_URL="YOUR_UPSTASH_REDIS_URL"
    REDIS_TOKEN="YOUR_UPSTASH_REDIS_TOKEN"
    ```

-----

## Usage Guide

### Running the API Server

To start the API server, run the following command from the root directory:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables hot-reloading for development. The API will be available at `http://127.0.0.1:8000`.

### Interactive API Documentation

FastAPI provides automatic interactive documentation. Once the server is running, you can access it at:

  * **Swagger UI**: `http://127.0.0.1:8000/docs`
  * **ReDoc**: `http://127.0.0.1:8000/redoc`

### API Endpoints Examples

Here are some `curl` examples to interact with the API. Replace `YOUR_POLL_ID` and `YOUR_CHOICE_ID` with actual IDs returned by the API.

#### 1\. Create a Poll

  * **Endpoint**: `POST /polls/create`
  * Creates a new poll. The `expires_at` field is optional.

<!-- end list -->

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/polls/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "What is your favorite programming language?",
    "options": ["Python", "JavaScript", "Rust", "Go"],
    "expires_at": "2026-12-31T23:59:59Z"
}'
```

#### 2\. Get All Active Polls

  * **Endpoint**: `GET /polls/?poll_status=active`
  * Returns a list of all polls that have not expired. You can also use `expired` or `all`.

<!-- end list -->

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/polls/?poll_status=active' \
  -H 'accept: application/json'
```

#### 3\. Vote on a Poll by Choice ID

  * **Endpoint**: `POST /vote/{poll_id}/id`
  * Records a vote for a specific choice using its unique ID.

<!-- end list -->

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/vote/YOUR_POLL_ID/id' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "choice_id": "YOUR_CHOICE_ID",
    "voter": {
      "email": "user@example.com"
    }
}'
```

#### 4\. Vote on a Poll by Choice Label

  * **Endpoint**: `POST /vote/{poll_id}/label`
  * Records a vote using the numerical label of the choice (1, 2, 3, etc.).

<!-- end list -->

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/vote/YOUR_POLL_ID/label' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "choice_label": 1,
    "voter": {
      "email": "another.user@example.com"
    }
}'
```

#### 5\. Get Poll Results

  * **Endpoint**: `GET /polls/{poll_id}/result`
  * Retrieves the current results for a specific poll.

<!-- end list -->

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/polls/YOUR_POLL_ID/result' \
  -H 'accept: application/json'
```

#### 6\. Delete a Poll

  * **Endpoint**: `DELETE /polls/{poll_id}`
  * [cite\_start]**Warning**: This is an irreversible action that deletes the poll, all its votes, and its results[cite: 31].

<!-- end list -->

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/polls/YOUR_POLL_ID' \
  -H 'accept: application/json'
```

-----

## 📂 Project Structure

The project follows a modular structure to separate concerns and improve maintainability.

```
 Poll-Project/
  ├── app/
  │   ├── api/            # Contains API route handlers (endpoints).
  │   │   ├── polls.py    # Routes for creating and viewing polls.
  │   │   ├── votes.py    # Routes for casting votes.
  │   │   └── danger.py   # Routes for destructive operations.
  │   ├── models/         # Pydantic data models for validation.
  │   │   ├── Polls.py
  │   │   ├── Votes.py
  │   │   └── ...
  │   └── services/       # Business logic and database interactions.
  │       └── utils.py    # Functions to interact with Redis.
  ├── .env.example        # Example environment variables.
  [cite_start]├── main.py             # Main FastAPI application instance[cite: 1].
  [cite_start]├── pyproject.toml      # Project metadata and dependencies[cite: 5].
  └── requirements.txt    # Frozen dependency list.
```

-----


## 🙏 Credits & Acknowledgments

  * **Project Author**: [suraj-yadav-aiml](https://www.google.com/search?q=https://github.com/suraj-yadav-aiml)
  * Built with the amazing [FastAPI](https://fastapi.tiangolo.com/) framework.
  * Data persistence powered by [Upstash](https://upstash.com/).
