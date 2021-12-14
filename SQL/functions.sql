-- This function gets the number of days since an order was placed. It is used to determine the status of an order.
CREATE or REPLACE FUNCTION get_days_since_order(order_num int)
	returns double precision
	language plpgsql
as
$$
declare
	d double precision;
begin
	select extract(day from now()-order_date) into d
	from "order"
    where order_number = order_num;
	return d;
end;
$$;

--This function gets the quantity of a book that was sold a month from when the function is called.
--It is used for the restock trigger function
CREATE or REPLACE FUNCTION get_quantity_sold_in_previous_month()
	returns int
	language plpgsql
as
$$
declare
	quantity_sold int;
begin
	select sold_quantity into quantity_sold
	from "order" join contains using (order_number)
	where date_trunc('month',order_date) = date_trunc('month', current_date - interval '1' month);
    return quantity_sold;
end;
$$;

-- This is a trigger function that restocks a book that has fallen below a specified threshold with the amount of that book sold in the previous month
CREATE OR REPLACE FUNCTION restock()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.stock_quantity < 10 THEN
		NEW.stock_quantity = NEW.stock_quantity + get_quantity_sold_in_previous_month();
	END IF;
	
	RETURN NEW;
END;
$$
