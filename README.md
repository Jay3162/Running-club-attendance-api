A Python-based REST API for managing running activity, tracking attendance, and generating simple performance insights.

Overview

Runner API is designed to support runners and organisers by providing a system to:

Register users and manage running events
Track attendance at runs and meetups
View historical activity
Generate basic analytics such as total runs, streaks, and best performances

Core Entities
User – represents a runner or participant
Event – a scheduled run or meetup
Attendance – links users to events they’ve attended
Club – groups users and events together

Features
CRUD operations for core entities
Attendance tracking for events
Historical run data retrieval
Basic analytics (e.g. total runs, streak tracking)

Tech Stack
Python
FastAPI
SQLite (with plans for PostgreSQL)
Pydantic (for data validation)

Architecture & Design
Refactored endpoint logic into a repository layer to improve separation of concerns
Implementing data validation to ensure integrity and prevent unintended field manipulation
Designing the API with scalability in mind, with future database expansion planned

Running the Project

python -m fastapi dev main.py

Then head to:
http://127.0.0.1:8000/docs

Current Status

This project is actively in development.
Upcoming improvements include:

Database integration (PostgreSQL)
Enhanced analytics features
Authentication and user roles
Deployment