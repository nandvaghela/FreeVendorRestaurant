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

Demo Images

- Home Page
<img width="1512" alt="Screenshot 2023-01-22 at 6 03 39 PM" src="https://user-images.githubusercontent.com/45141940/218844361-11d1bee4-57ab-460f-a5e2-82142215c3eb.png">
- Login
<img width="1512" alt="Screenshot 2023-01-22 at 7 15 21 PM" src="https://user-images.githubusercontent.com/45141940/218845002-6d3470c0-6f52-4eec-9793-3e02e29de5e3.png">
- Register
<img width="1512" alt="Screenshot 2023-01-22 at 7 15 35 PM" src="https://user-images.githubusercontent.com/45141940/218845111-d51496e3-dc19-422c-9397-bd1d2c1b12e2.png">
- Register Vendor
<img width="1512" alt="Screenshot 2023-01-22 at 7 15 50 PM" src="https://user-images.githubusercontent.com/45141940/218845287-71fcb9bc-6547-4d93-a135-032fe0b368c2.png">
- Distance between User and nearby restaurants
<img width="1512" alt="Screenshot 2023-02-14 at 4 59 23 PM" src="https://user-images.githubusercontent.com/45141940/218872970-e4afec42-20aa-4c27-ad98-8eb477d4d0af.png">

- Restaurant Menu
<img width="1512" alt="Screenshot 2023-01-22 at 5 30 53 PM" src="https://user-images.githubusercontent.com/45141940/218871475-055926d7-45a2-4dfc-b021-17b790a351f0.png">
- Cart
<img width="1512" alt="Screenshot 2023-01-22 at 5 31 17 PM" src="https://user-images.githubusercontent.com/45141940/218871592-1495cbf6-a334-46b6-ac01-a8a21ff863b3.png">
- Order
<img width="1512" alt="Screenshot 2023-01-22 at 5 31 27 PM" src="https://user-images.githubusercontent.com/45141940/218870774-a2d1fa8e-a713-45a5-bf6c-37c411bf4369.png">
- Order Completed
<img width="1512" alt="Screenshot 2023-01-22 at 5 32 07 PM" src="https://user-images.githubusercontent.com/45141940/218870804-34576eae-7980-4f18-b1c8-a7bef2296725.png">
- Manage Restaurant page for Vendor
<img width="1512" alt="Screenshot 2023-01-22 at 5 29 40 PM" src="https://user-images.githubusercontent.com/45141940/218870906-3928b48d-cc90-4543-9634-0c69bf424505.png">
- Vendor's received Order page
  <img width="1512" alt="Screenshot 2023-01-22 at 5 29 26 PM" src="https://user-images.githubusercontent.com/45141940/218873293-ae0e10e4-520c-4403-860d-0009b269ea9a.png">

- Manage Menu page for Vendor
<img width="1512" alt="Screenshot 2023-01-22 at 5 29 53 PM" src="https://user-images.githubusercontent.com/45141940/218870943-045c61fe-be6f-40f7-ab0d-966ec518c567.png">

Contributing

Contributions are always welcome! If you find a bug or want to suggest a new feature, feel free to open an issue or submit a pull request.
