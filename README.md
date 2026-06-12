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

## Project Structure

```txt
.
├── app.py
├── config.example.py
├── config.py
├── database
│   ├── db.py
│   ├── __init__.py
│   └── models.py
├── instance
│   └── deals.db
├── postman
│   └── travel-deal-api.postman_collection.json
├── README.md
├── requirements.txt
├── routes
│   ├── deal_routes.py
│   └── __init__.py
├── services
│   ├── deal_service.py
│   └── __init__.py
└── utils
    ├── __init__.py
    └── validators.py
```

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

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate virtual environment

For Linux/macOS:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the project

Copy the example config file:

```bash
cp config.example.py config.py
```

The default database configuration uses SQLite:

```txt
sqlite:///deals.db
```

### 5. Run the project

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

## API Details

### Health Check

```http
GET /
```

Example response:

```json
{
  "message": "Travel Deals API in running!"
}
```

---

### Create Travel Deal

```http
POST /deals/
```

Request body:

```json
{
  "destination": "Dubai",
  "price": 5000,
  "platform": "Booking",
  "rating": 4.5,
  "travel_type": "Luxury"
}
```

Success response:

```json
{
  "success": true,
  "message": "Deal created successfully",
  "data": {
    "id": 1,
    "destination": "Dubai",
    "price": 5000,
    "platform": "Booking",
    "rating": 4.5,
    "travel_type": "Luxury"
  }
}
```

---

### Get All Deals

```http
GET /deals/
```

Success response:

```json
{
  "success": true,
  "message": "Deals fetched successfully",
  "data": [
    {
      "id": 1,
      "destination": "Dubai",
      "price": 5000,
      "platform": "Booking",
      "rating": 4.5,
      "travel_type": "Luxury"
    }
  ]
}
```

---

### Get Single Deal

```http
GET /deals/1
```

Success response:

```json
{
  "success": true,
  "message": "Deal fetched successfully",
  "data": {
    "id": 1,
    "destination": "Dubai",
    "price": 5000,
    "platform": "Booking",
    "rating": 4.5,
    "travel_type": "Luxury"
  }
}
```

If the deal is not found:

```json
{
  "success": false,
  "Message": "Deal not found"
}
```

---

## Validation Rules

| Field         | Rule                                                      |
| ------------- | --------------------------------------------------------- |
| `destination` | Required and cannot be empty                              |
| `price`       | Required and must be a positive number                    |
| `platform`    | Required and cannot be empty                              |
| `rating`      | Required and must be between 1 and 5                      |
| `travel_type` | Must be one of: `Budget`, `Luxury`, `Adventure`, `Family` |

Example validation error:

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "price": "Price must be a positive number"
  }
}
```

---

## Postman Collection

A Postman collection is included in the project:

```txt
postman/travel-deal-api.postman_collection.json
```

Import this file into Postman to test the API endpoints.

---

## Notes

* The database file is stored inside the `instance/` folder.
* Tables are created automatically when the app starts.
* `config.py` is for local configuration.
* `config.example.py` is provided as a sample configuration file.
