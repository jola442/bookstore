## Description
This is a text interface desktop application that allows clients to browse and purchase books. The system is implemented using Python and PostgreSQL. It provides different functionalities depending on whether the user is an owner or a customer. Owners can choose to exit the store, search books by various criteria, add new books, remove books, generate reports on sales and expenditure, and more. They can also manually input information about a new book or retrieve information from the Google Books API. Customers can also exit the store, search for books by various criteria, add books to their cart, and checkout. They can also track their orders after they have been placed. The entity-relationship diagram and normalized relation schemas can be found on the github page of this project. Created using PostgreSQL and Python.

## 


## Run Instructions and General Information
books.json contains information about the first 5 books added in SQL/relationsInsertFile and is used solely for testing purposes.

You may add more books to this json file by running addBook.py.

Required python modules: psycopg2, random, requests, PrettyTable.

Edit lines 6, 7 and 8 to specify the name of the database, your user ID and password respectively.

Copy and paste all text from the SQL files into pgAdmin and run it.

Run main.py.

You may choose to be an owner or a user but not both. You are required to register or sign in to access the bookstore.

After that you are given a menu of options.

As a user, you must search by ISBN-13 to add a book to your cart.

Once you checkout, you are given an order number with which you can track your order.

On the day the order is placed, the order status is "At warehouse".

One day after the order is placed, the order status is "In transit".

Three days after the order is placed, the order status is "Delivered".

SQL/relationsInsertSQL inserts data for the order relation that tests this functionality.

As an owner, when adding books you may choose to add an actual book from the internet using the Google Books API or manually enter in book data.

In both cases, you would still have to enter the genre, price, stock_quantity and publisher_percentage for the book.

## Database Design Details
### Entity-Relationship Diagram
<img width="365" alt="image" src="https://user-images.githubusercontent.com/51683551/200884439-2a5dc2bd-36a1-4356-aa0a-36477370b3d6.png">

### Database Schema Diagram
<img width="362" alt="image" src="https://user-images.githubusercontent.com/51683551/200885100-9f6fe4eb-9049-4dc4-b79d-09a5466273a5.png">


## Demo
### Bookstore Owner view
<img width="188" alt="image" src="https://user-images.githubusercontent.com/51683551/200885696-84ab935e-71d0-40fe-97a3-62ae85feeb9f.png">

## Customer view
<img width="275" alt="image" src="https://user-images.githubusercontent.com/51683551/200886224-b9b76519-a44c-4236-8173-0cc17aa0db6d.png">



