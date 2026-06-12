# Travel Deal Management System using Flask

A simple Flask REST API for managing travel deals. This project allows users to create travel deals, view all deals, and view a single deal by ID.

The project is built using **Python**, **Flask**, **Flask-SQLAlchemy**, and **SQLite**.

---

## Features

* Create a new travel deal
* View all travel deals
* View a single travel deal by ID
* Input validation
* Proper JSON responses
* Proper HTTP status codes
* SQLite database using Flask-SQLAlchemy
* Modular project structure


---

## Tech Stack

| Technology       | Purpose               |
| ---------------- | --------------------- |
| Python           | Programming language  |
| Flask            | Web framework         |
| Flask-SQLAlchemy | ORM/database handling |
| SQLite           | Local database        |
| Postman          | API testing           |

---

## Setup Instructions

### Clone the project

```bash
git clone https://github.com/rangonroyutsab/travel-deal-api-rangon.git
cd travel-deal-api-rangon
```

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

For Linux/macOS:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the project

Copy the example config file:

```bash
cp config.example.py config.py
```

The default database configuration uses SQLite:

```txt
sqlite:///deals.db
```

### Run the project

```bash
python app.py
```

The server will start at:

```txt
http://127.0.0.1:5000
```

---

## API Description

| Method | Endpoint           | Description                                          | Request Body Required | Success Status |
| ------ | ------------------ | ---------------------------------------------------- | --------------------- | -------------- |
| GET    | `/`                | Health check route to verify that the API is running | No                    | `200 OK`       |
| POST   | `/deals/`          | Create a new travel deal                             | Yes                   | `201 Created`  |
| GET    | `/deals/`          | Get all travel deals                                 | No                    | `200 OK`       |
| GET    | `/deals/<deal_id>` | Get a single travel deal by ID                       | No                    | `200 OK`       |


---

## Validation Rules

| Field         | Rule                                                      |
| ------------- | --------------------------------------------------------- |
| `destination` | Required and cannot be empty                              |
| `price`       | Required and must be a positive number                    |
| `platform`    | Required and cannot be empty                              |
| `rating`      | Required and must be between 1 and 5                      |
| `travel_type` | Must be one of: `Budget`, `Luxury`, `Adventure`, `Family` |


---

## Postman Collection

A Postman collection is included in the project:


[postman/travel-deal-api.postman_collection.json](https://github.com/rangonroyutsab/travel-deal-api-rangon/blob/main/postman/travel-deal-api.postman_collection.json)


Import this file into Postman to test the API endpoints.


---

## Project Structure

```txt
.
├── app.py
├── config.example.py
├── database
│   ├── db.py
│   └── models.py
├── instance
│   └── deals.db
├── postman
│   └── travel-deal-api.postman_collection.json
├── README.md
├── requirements.txt
├── routes
│   ├── deal_routes.py
├── services
│   ├── deal_service.py
└── utils
    └── validators.py
```
