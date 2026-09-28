# Kypson Mini RFQ Desk

A simple full-stack web application for managing packaging **Requests for Quotation (RFQs)**.

The application allows buyers to raise RFQs for packaging products, suppliers to submit quotes, and buyers to compare supplier quotes with the **lowest-priced quote automatically marked as Best Price**.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** MySQL
* **Frontend:** HTML, CSS
* **Templating:** Jinja2
* **Database Connector:** MySQL Connector/Python
* **Environment Variables:** python-dotenv

## Features

* View 5 seeded packaging products
* Raise an RFQ for a selected product
* View existing RFQs
* View RFQ details
* Add supplier quotes
* Display quotes sorted by unit price from lowest to highest
* Automatically mark the lowest quote as **Best Price**
* Validate buyer name, supplier name, quantity, unit price, delivery city, and delivery days
* Store all RFQ and quote data persistently in MySQL
* Responsive and simple HTML/CSS interface
* Empty state displayed when an RFQ has no supplier quotes

## Project Structure

```text
kypsonTask/
│
├── app.py
├── schema.sql
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── templates/
    ├── base.html
    ├── products.html
    ├── raise_rfq.html
    └── rfq_detail.html
```

> **Note:** `.env` is used locally for database credentials and must not be committed to GitHub.

## Database Setup

The application uses MySQL.

### 1. Open MySQL Workbench

Connect to your local MySQL server.

### 2. Run the database schema

Open `schema.sql` and execute it.

The script creates:

* `kypson_intern` database
* `products` table
* `rfqs` table
* `quotes` table
* 5 seeded packaging products

The required seeded products are:

1. Corrugated Boxes
2. Plastic Bottles
3. BOPP Bags
4. Woven PP Sacks
5. Shrink Film

## Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=kypson_intern
```

Replace `your_mysql_password` with your local MySQL root password.

Do not commit the `.env` file to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd kypsonTask
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Flask application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

Open this URL in a browser.

## Application Flow

### 1. Products Page

The home page displays the 5 packaging products.

Each product has a **Raise RFQ** button.

The page also displays existing RFQs with:

* Product
* Buyer
* Delivery city
* Number of quotes

### 2. Raise RFQ

The buyer can create an RFQ by entering:

* Buyer name
* Product
* Quantity
* Delivery city
* Optional notes

After successful submission, the application redirects to the RFQ detail page.

### 3. RFQ Detail

The RFQ detail page displays:

* Product
* Buyer
* Quantity
* Delivery city
* Category
* Notes, if provided

A supplier can submit:

* Supplier name
* Unit price
* Delivery days

### 4. Quote Comparison

All supplier quotes are displayed in ascending order of unit price.

The lowest-priced quote is automatically marked:

```text
Best Price
```

## Validation

The application validates the following:

* Buyer name cannot be empty
* Delivery city cannot be empty
* Supplier name cannot be empty
* Quantity must be greater than 0
* Unit price must be greater than 0
* Delivery days must be greater than 0
* A product must be selected

Validation errors are displayed on the same page without losing the submitted form values.

## Stretch Goal Implemented

### Empty State — "No quotes yet"

The **Empty State** stretch goal has been implemented.

When an RFQ has no supplier quotes, the RFQ Detail page displays:

```text
No quotes yet.
Supplier quotes will appear here once they are submitted.
```

After a supplier submits a quote, the empty-state message is replaced by the supplier quote list.

## Testing the Required Flow

The application can be tested using the following flow:

1. Open the Products page.
2. Select **Corrugated Boxes**.
3. Raise an RFQ with:

   * Buyer: `Isha`
   * Quantity: `5000`
   * City: `Ahmedabad`
4. Add the following supplier quotes:

### Quote 1

```text
Supplier: PackWell
Unit Price: 10
Delivery Days: 6
```

### Quote 2

```text
Supplier: BoxMart
Unit Price: 11.20
Delivery Days: 10
```

Expected result:

* BoxMart appears before PackWell.
* BoxMart is marked **Best Price**.
* Refreshing the page does not remove the RFQ or quotes because the data is stored in MySQL.

## Data Persistence

RFQs and supplier quotes are stored in MySQL.

Refreshing or restarting the Flask application does not remove previously created RFQs or quotes.

## Security / Configuration

Database credentials are stored in environment variables rather than directly in the Python source code.

The `.env` file should remain local and should not be uploaded to GitHub.

## Requirements

The project follows the assignment constraints:

* Python/Flask backend
* MySQL database
* HTML/CSS frontend
* No authentication
* No payments
* No orders
* No file uploads
* No admin panel
* No React or frontend framework
* Data persisted in MySQL
