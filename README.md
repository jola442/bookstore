books.json contains information about the first 5 books added in SQL/relationsInsertFile and is used solely for testing purposes
You may add more books to this json file by running addBook.py
Required python modules: psycopg2, random, requests, PrettyTable.
Edit lines 6, 7 and 8 to specify the name of the database, your user ID and password respectively.

Copy and paste all text from the SQL files into pgAdmin and run it
Run main.py
You may choose to be an owner or a user but not both. You are required to register or sign in to access the bookstore.
After that you are given a menu of options.
As a user, you must search by ISBN-13 to add a book to your cart
Once you checkout, you are given an order number with which you can track your order
On the day the order is placed, the order status is "At warehouse".
One day after the order is placed, the order status is "In transit".
Three days after the order is placed, the order status is "Delivered".
SQL/relationsInsertSQL inserts data for the order relation that tests this functionality.
As an owner, when adding books you may choose to add an actual book from the internet using the Google Books API or manually enter in book data.
In both cases, you would still have to enter the genre, price, stock_quantity and publisher_percentage for the book.



