# FreeVendorRestaurant
Food Vendor Django

A web application developed using Django framework, that provides a platform for food vendors to sell their products online. 
I created this project with Django , including working with Geodjango, gdal, PostGIS spatial database, PayPal payment gateway, 
and many other features.

Features
- Show the distance between the user's location and restaurants
- Vendors can only see the products from their menu, not from other vendors
- Vendors can set the opening hours of their restaurants
- User will receive emails after placing orders, to activate the account and reset password
- Vendors will receive emails after receiving orders
- Implemented Cart functionalities with AJAX requests
- Implemented Google Autocomplete field
- Implemented ManyToMany Relationships in vendor models
- Integrated PayPal payment gateway

Requirements
- Python 3.x
- Django 3.x
- PostgreSQL
- GDAL
- Geodjango

Installation

Clone the repository:

- $ git clone https://github.com/nandvaghela/foodvendordjango.com.git

Change into the project directory:

- $ cd foodvendordjango.com

Create and activate a virtual environment:
- $ python -m venv venv
- $ source venv/bin/activate

Install the required packages:

- $ pip install -r requirements.txt

Migrate the database:

- $ python manage.py migrate

Run the development server:

- $ python manage.py runserver

Open your browser and navigate to http://localhost:8000/ to see the application in action.

Contributing
Contributions are welcome! If you find a bug or want to suggest a new feature, feel free to open an issue or submit a pull request.
