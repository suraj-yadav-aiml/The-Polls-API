# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
- Install dependencies: `uv sync`
- Activate virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
- Copy environment variables: `cp .env.example .env` (then configure REDIS_URL and REDIS_TOKEN)

### Running the Application
- Start development server: `uvicorn main:app --reload`
- Server runs on: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs (Swagger UI) or http://127.0.0.1:8000/redoc

### Deployment
- Deployed on Vercel using `vercel.json` configuration
- Uses `@vercel/python` build for the FastAPI application

## Project Architecture

### Core Structure
- **main.py**: FastAPI application entry point with router configuration and exception handling
- **app/api/**: API route handlers organized by domain
  - `polls.py`: Poll creation and retrieval endpoints
  - `votes.py`: Voting functionality
  - `danger.py`: Destructive operations (poll deletion)
  - `exceptions.py`: Custom exception handlers
- **app/models/**: Pydantic data models for validation
  - `Polls.py`: Poll and PollCreate models
  - `Votes.py`: Vote model with voter information
  - `Choice.py`: Poll option model
  - `Results.py`: Result aggregation models
- **app/services/**: Business logic and data access
  - `utils.py`: Redis operations for polls, votes, and results

### Data Storage
- Uses Upstash Redis for persistent storage
- Data patterns:
  - `poll:{poll_id}`: Stores serialized Poll objects
  - `vote:{poll_id}`: Hash storing votes by voter email
  - `vote_count:{poll_id}`: Hash storing vote counts by choice_id

### Key Features
- Poll creation with 2-5 choices and optional expiration
- Duplicate vote prevention via email tracking
- Real-time vote counting and result aggregation
- Voting by choice ID or numerical label
- Poll status filtering (active/expired/all)

### Dependencies
- **FastAPI**: Web framework with automatic API documentation
- **Pydantic**: Data validation and serialization
- **Upstash Redis**: Cloud Redis database for data persistence
- **uvicorn**: ASGI server for development
- **uv**: Fast Python package installer and dependency manager

### Environment Variables
Configure in `.env` file:
- `REDIS_URL`: Upstash Redis connection URL
- `REDIS_TOKEN`: Upstash Redis authentication token