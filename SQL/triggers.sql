-- This trigger restocks all books that have fallen below a specified threshold with the amount of the book sold in the previous month
CREATE TRIGGER restock_books
BEFORE UPDATE
ON book
FOR EACH ROW
EXECUTE PROCEDURE restock();