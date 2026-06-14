# Travel Deal Management System using Flask

A simple Flask REST API for managing travel deals. This project allows users to create, update, delete, view, search, filter, sort, and track travel deals.

The project is built using **Python**, **Flask**, **Flask-SQLAlchemy**, and **SQLite**.

---

## Features

* Create a new travel deal
* Update an existing travel deal
* Delete a travel deal
* View all travel deals
* View a single travel deal by ID
* Search travel deals by destination, platform, or travel type
* Filter travel deals by minimum and maximum price
* Sort travel deals by supported fields
* View recently accessed deals
* View popular deals by successful view count
* View basic in-memory API usage statistics
* Input validation
* Query parameter validation
* Partial and case-insensitive searching
* API activity logging
* Proper JSON responses
* Proper HTTP status codes
* SQLite database using Flask-SQLAlchemy
* Modern SQLAlchemy select statements
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
python3 -m venv .venv
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
python3 app.py
```

The server will start at:

```txt
http://127.0.0.1:5000
```

---

## API Description

| Method | Endpoint           | Description                                          | Request Body Required | Query Parameters                         | Success Status |
| ------ | ------------------ | ---------------------------------------------------- | --------------------- | ---------------------------------------- | -------------- |
| GET    | `/`                | Health check route to verify that the API is running | No                    | No                                       | `200 OK`       |
| POST   | `/deals/`          | Create a new travel deal                             | Yes                   | No                                       | `201 Created`  |
| GET    | `/deals/`          | Get all travel deals                                 | No                    | No                                       | `200 OK`       |
| GET    | `/deals/search`    | Search travel deals                                  | No                    | `destination`, `platform`, `travel_type` | `200 OK`       |
| GET    | `/deals/filter`    | Filter travel deals by budget                        | No                    | `min_price`, `max_price`                 | `200 OK`       |
| GET    | `/deals/sort`      | Sort travel deals                                    | No                    | `sort_by`, `order`                       | `200 OK`       |
| GET    | `/deals/recent`    | Get recently viewed deals                            | No                    | No                                       | `200 OK`       |
| GET    | `/deals/popular`   | Get popular deals by view count                      | No                    | No                                       | `200 OK`       |
| GET    | `/deals/<deal_id>` | Get a single travel deal by ID                       | No                    | No                                       | `200 OK`       |
| PUT    | `/deals/<deal_id>` | Update a travel deal by ID                           | Yes                   | No                                       | `200 OK`       |
| DELETE | `/deals/<deal_id>` | Delete a travel deal by ID                           | No                    | No                                       | `200 OK`       |
| GET    | `/stats`           | Get basic in-memory API usage statistics             | No                    | No                                       | `200 OK`       |


---

## API Examples

### Search Deals

Search supports partial and case-insensitive matching.

```http
GET /deals/search?destination=dubai
GET /deals/search?platform=booking
GET /deals/search?travel_type=budget
```

### Filter Deals by Budget

```http
GET /deals/filter?min_price=1000
GET /deals/filter?max_price=5000
GET /deals/filter?min_price=1000&max_price=5000
```

### Sort Deals

```http
GET /deals/sort?sort_by=price&order=asc
GET /deals/sort?sort_by=rating&order=desc
```

Supported sort fields:

```txt
destination, price, platform, rating, travel_type
```

Supported sort orders:

```txt
asc, desc
```

### Recently Viewed Deals

```http
GET /deals/recent
```

Recently viewed deals are tracked when a deal is successfully fetched using:

```http
GET /deals/<deal_id>
```

The recent list is stored in memory and keeps the latest 5 viewed deals. It resets when the server restarts.

### Popular Deals

```http
GET /deals/popular
```

Popular deals are tracked when a deal is successfully fetched using:

```http
GET /deals/<deal_id>
```

Each popular deal includes a `view_count`. The popular list is stored in memory and resets when the server restarts.

### Update a Deal

```http
PUT /deals/1
```

```json
{
  "destination": "Cox's Bazar",
  "price": 5200,
  "platform": "Booking",
  "rating": 4.4,
  "travel_type": "Family"
}
```

Update requests require the full deal body and use the same validation rules as deal creation.

### Delete a Deal

```http
DELETE /deals/1
```

Deleted deals are removed from recently viewed and popular in-memory tracking.

### API Stats

```http
GET /stats
```

The stats response includes basic request counters:

```txt
total_requests, successful_requests, failed_requests
```

Request counters are stored in memory and reset when the server restarts.


---

## Validation Rules

| Field         | Rule                                                      |
| ------------- | --------------------------------------------------------- |
| `destination` | Required and cannot be empty                              |
| `price`       | Required and must be a positive number                    |
| `platform`    | Required and cannot be empty                              |
| `rating`      | Required and must be between 1 and 5                      |
| `travel_type` | Must be one of: `Budget`, `Luxury`, `Adventure`, `Family` |

These rules apply to both `POST /deals/` and full-body `PUT /deals/<deal_id>` requests.


### Query Parameter Validation

| Feature | Rule |
| ------- | ---- |
| Search | At least one search parameter is required |
| Search | Search values cannot be empty |
| Search | `travel_type` must be one of: `Budget`, `Luxury`, `Adventure`, `Family` |
| Filter | At least one price filter is required |
| Filter | `min_price` and `max_price` must be numbers |
| Filter | `min_price` cannot be negative |
| Filter | `max_price` cannot be negative |
| Filter | `max_price` cannot be smaller than `min_price` |
| Sort | `sort_by` is required |
| Sort | `sort_by` must be one of: `destination`, `price`, `platform`, `rating`, `travel_type` |
| Sort | `order` must be `asc` or `desc` |


---

## Logging

The API uses Python logging to track important application events.

Logged events include:

* Incoming API requests
* Successful operations
* Validation failures
* Not found responses
* Failed database operations

Logging levels used:

```txt
logging.info()
logging.warning()
logging.error()
```


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
    ├── stats.py
    └── validators.py
```
