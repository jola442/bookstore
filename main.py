import psycopg2
from random import randint
import requests
from prettytable import PrettyTable

DATABASE = "Bookstore"
USER_ID = 'userid'
PASSWORD = 'password'
AREACODES = [204, 226, 236, 249, 250, 289,
             306, 343, 365, 367,
             403, 416, 418, 431, 437, 438, 450,
             506, 514, 519, 548, 579, 581, 587, 
             604, 613, 639, 647,
             705, 709, 778, 780, 782, 
             807, 819, 825, 867, 873, 
             902, 905]
EMAIL_SERVICES = ["@gmail.com", "@yahoo.com", "@icloud.com", "@outlook.com"]
SALES_TAX = 0.13
api = "https://www.googleapis.com/books/v1/volumes?&key=AIzaSyBu8qslMt65MSFTbfCXy0qZfIcweZmdAmg"

#Connecting to the DB  
try:
    conn = psycopg2.connect( host="localhost", port=5432, dbname=DATABASE, user=USER_ID, password=PASSWORD)
    cur = conn.cursor() 
except Exception as sqlErr:
    print("Exception : ", sqlErr)


def userRegister(fName: str, lName: str, email: str, passwd: str, bAddr:str, sAddr: str, phoneNum: list) -> tuple:
    try:
        cur.execute('''insert into "user"(first_name, last_name, email_address, password, billing_address, shipping_address)
                        values(%s, %s, %s, %s, %s, %s)''', 
                        (fName, lName, email, passwd, bAddr, sAddr))
        conn.commit()

    except Exception as sqlErr:
        print("Could not insert tuple", sqlErr)
        conn.rollback()
        
 
    try:
        cur.execute('''select *
                        from "user"
                        where email_address = %s''', 
                        (email,))
        #the first column of the the first tuple returned
        user = cur.fetchone()
    except Exception as sqlErr:
        print("Could not retrieve tuple")
        conn.rollback()
            
        
            
    
    for i in range(len(phoneNum)):
        try:
            cur.execute('''insert into user_phone
                            values(%s, %s)''',
                            (user[0], phoneNum[i]))
            conn.commit()
            
        except Exception as sqlErr:
            print("Could not insert tuple", sqlErr)
            conn.rollback()
            
    
    return user

def ownerRegister(email:str, passwd: str) -> bool:
    try:
        cur.execute('''insert into owner(email_address, password)
                        values(%s, %s)''', (email, passwd))
        conn.commit()
        return True
        
    except Exception as sqlErr:
        print("Could not insert tuple", sqlErr)
        return False

     

def userSignIn(email:str, passwd:str) -> tuple:
    try:
        cur.execute('''select *
                        from "user"
                        where email_address = %s and password = %s''', 
                        (email, passwd))
        #the first column of the the first tuple returned
        user = cur.fetchone()

    except Exception as sqlErr:
        print("Could not retrieve tuple", sqlErr)
        conn.rollback()
        
    finally:
        return user

def ownerSignIn(email:str, passwd:str) -> bool:
    try:
        cur.execute('''select owner_id
                        from owner
                        where email_address = %s and password = %s''', 
                        (email, passwd))
        owner = cur.fetchone()
        if(owner):
            return True
        else:
            return False
 
    except Exception as sqlErr:
        print("Could not retrieve tuple", sqlErr)
        conn.rollback()
        return False

# This function generates an n number string
def generateNumber(n)->str:
    result = ''
    for i in range(n):
        result += str(randint(0, 9))
    return result

def displayBook(book: tuple):
    print()
    authors = []
    authors.append(book[8] + " " + book[9])
    print("-------------------------")
    print("        BOOK", )
    print("-------------------------")
    print("Title:", book[2])
    print("ISBN:", book[1])
    print("Genre:", book[3])
    print("Price:", book[5])
    print("In Stock:", book[4])
    print("Page Count:", book[6])
    print("Publisher Name:", book[10])
    print("Author(s): ", end='')

    for i in range(len(authors)):
        if i == len(authors)-1:
            print(authors[i])
        else:
            print(authors[i] + ", ", end='')
    print("_________________________")
    print()

def displayOrder(order: tuple):
    if(order):
        print("-------------------------")
        print("        ORDER", )
        print("-------------------------")
        print("Order Number:", order[0])
        print("Order Date:", order[2])
        print("Total:", order[3])
        print("Shipping Address:", order[4])
        print("Billing Address:", order[5])
        print("Order status:", order[6])
        print("_________________________")
        print()

def displayUserMenu():
    print("0. Exit the store")
    print("1. Search books by ISBN-13")
    print("2. Search books by Title")
    print("3. Search books by Author")
    print("4. Search books by Genre")
    print("5. Checkout")
    print("6. Track order")
        
def displayOwnerMenu():
    print("0. Exit the store")
    print("1. Search books by ISBN-13")
    print("2. Search books by Title")
    print("3. Search books by Author")
    print("4. Search books by Genre")
    print("5. Add a new book")
    print("6. Remove a book")
    print("7. Generate sales vs expenditure report")
    print("8. Generate sales per genre report")
    print("9. Generate sales per author report")

def displayCart(cart:list, curTotal):
    print("-------------------------")
    print("        YOUR CART")
    for i in range(len(cart)):
        print("_________________________")
        print("Item", i+1)
        print("_________________________") 
        print("Title:", cart[i]["title"])
        print("ISBN:", cart[i]["ISBN"])
        print("Price:", cart[i]["price"])
        print("Quantity:", cart[i]["inCartQuantity"])
    
    # print("-------------------------")
    # print("Subtotal:", curTotal)
    # print("-------------------------")
    # print("Tax: %.2f" % curTotal * 0.13)
    # print("-------------------------")
    # print("Total: %.2f" % curTotal * 1.13)
    print("-------------------------")
    print("Total: %.2f" % curTotal)
    print("-------------------------")


def searchByAuthor(author: str) -> bool:
    fName = author.split()[0]
    lName = author.split()[1] if len(author.split()) > 1 else ''
    try:
        cur.execute('''select *
                        from (book join author using (ISBN)) join publisher using (publisher_id) 
                        where first_name = %s and last_name = %s''', 
                        (fName, lName,))

        results = cur.fetchall()
        if(len(results) > 0):
            print()
            
            for book in results:
                displayBook(book)
            
            return True
        else:
            print("No search results")
            return False
    
    except Exception as sqlErr:
        print("Could not retrieve tuple", sqlErr)
        conn.rollback()
        return False

def searchByGenre(genre: str) -> bool:
    try:
        cur.execute('''select *
                        from (book join author using (ISBN)) join publisher using (publisher_id)
                        where genre = %s''', 
                        (genre,))
      

        results = cur.fetchall()
        if(len(results) > 0):
            print()
            
            for book in results:
                displayBook(book)
            
            return True
        else:
            print("No search results")
            return False
    
    except Exception as sqlErr:
        print("Could not retrieve tuple", sqlErr)
        conn.rollback()
        return False

def searchByTitle(title: str) -> bool:
    try:
        cur.execute('''select *
                        from (book join author using (ISBN)) join publisher using (publisher_id)
                        where title = %s''', 
                        (title,))

        results = cur.fetchall()
        if(len(results) > 0):
            print()
            
            for book in results:
                displayBook(book)
            
            return True
        else:
            print("No search results")
            return False
    
    except Exception as sqlErr:
        print("Could not retrieve tuple", sqlErr)
        conn.rollback()
        return False


def searchByISBN(isbn: str) -> tuple:
    try:
        cur.execute('''select *
                        from (book join author using(ISBN)) join publisher using (publisher_id) 
                        where ISBN = %s''', 
                        (isbn,))
        #the first column of the the first tuple returned
        book = cur.fetchone()
        if(book  != None):
            displayBook(book)
        else:
            print("No search results")

    except Exception as sqlErr:
        print("Could not retrieve tuple", sqlErr)
        conn.rollback()
    
    finally:
        return book

def placeOrder(cart:list, curTotal, uid, sAddr, bAddr) -> bool:
    try:
        cur.execute('''insert into "order"(user_id, total, shipping_address, billing_address)
                        values(%s, %s, %s, %s) returning order_number''', (uid, curTotal, sAddr, bAddr))
        conn.commit()
        orderNum = cur.fetchone()[0]

        for i in range(len(cart)):
            cur.execute('''insert into contains
                            values(%s, %s, %s)''', (orderNum, cart[i]["ISBN"], cart[i]["stockQuantity"]))
            conn.commit()

            cur.execute('''update book
                            set stock_quantity = %s
                            where ISBN = %s''', (cart[i]["stockQuantity"]-cart[i]["inCartQuantity"], cart[i]["ISBN"]))
            conn.commit()
        print("Order number:", orderNum)
        print("Order placed! You should receive an email of your receipt shortly")

        
    except Exception as sqlErr:
        print("Could not insert tuple", sqlErr)

def getOrder(orderNum: int, user: tuple) -> tuple:
    try:
        cur.execute('''select get_days_since_order(%s)''', (orderNum,))
        conn.commit()

        daysSinceOrder = cur.fetchone()[0]
        # print(daysSinceOrder)

        if daysSinceOrder != None:
            if daysSinceOrder >= 1 and daysSinceOrder < 3:
                cur.execute('''update "order"
                                set order_status = %s
                                where order_number = %s''', ('In transit', orderNum))
                conn.commit()
            elif daysSinceOrder >= 3:
                cur.execute('''update "order"
                set order_status = %s
                where order_number = %s''', ('Delivered', orderNum))
                conn.commit()
        else:
            print("This order does not exist")
            order = None
            return

        cur.execute('''select *
                    from "order"
                    where order_number = %s''', (orderNum,))
        conn.commit()
        order = cur.fetchone()

        if(user[0] != order[1]):
            order = None
            print("You can only view the status of orders you made")
        

    except Exception as sqlErr:
        print("Could not retrieve tuple", sqlErr)
    
    finally:
        return order

#This function retrieves a book with the specified ISBN from the internet using the Google Books API
def getBook(isbn: str) -> dict:
    parameters = {
        "q": "isbn:"+isbn

    }
    response = requests.get(api, params=parameters)
    results = response.json()
    try:
        bookDict = results["items"][0]
    #If the first element of the items list DNE then no results were returned
    except KeyError:
        print("This IBN does not exist")
        return {}

    bookData = bookDict["volumeInfo"]
    return bookData
    
def addBook(isbn: str) -> bool:
    try:
        cur.execute('''select ISBN
                    from book
                    where ISBN = %s''', (isbn,))
        conn.commit()
        book = cur.fetchone()
        # print("Searched for book")

        if(book):
            print("This book already exists!")
            return
        else:
            genre = input("Enter a genre: ")
            quantity = input("How many would you like to add? ")
            insertType = input("Would you like to insert an actual book? y or n: ").lower().strip()

            while True:
                try:
                    price = float(input("Enter the price: "))
                    pubPercentage = float(input("What percentage of sales go to the publisher?"))
                    break
                except ValueError:
                    print("Please enter an actual number...")

            if(insertType == 'y'):
                book = getBook(isbn)
                if(book):
                    try:
                        title = book["title"]
            
                        authors = book["authors"]
    
                        numPages = book["pageCount"]
            
                        pub = book["publisher"]
                    except KeyError:
                        print("Information about the title, authors, number of pages and or the publisher of this book could not be retrieved")
                        return
                        
                    
                
                    print("Retrieved book")
            else:
                pub = input("Enter the publisher name: ")
                title = input("Enter the title of the book: ")
                while True:
                    try:
                        numPages = int(input("Enter the number of pages"))
                        numAuthors = int(input("How many authors?"))
                        break
                    except ValueError:
                        print("Please enter a number...")

                i = 0
                authors = []
                while True and numAuthors > 0:
                    author = input("Please enter author number %d:" % (i+1))
                    authors.append(author)
                    i += 1
                    if(i == numAuthors):
                        break

            print("Trying to check for publisher")
            cur.execute('''select publisher_id
                            from publisher
                            where name = %s''', (pub,))
            conn.commit()
            print("Checked for publisher")

            publisher = cur.fetchone()
            #if the publisher is already in the DB
            if(publisher):
                pub_id = publisher[0]
            else:
                #Generate a random VALID phone number
                pubPhone = str(AREACODES[randint(0, len(AREACODES))-1]) + generateNumber(7) 

                #Generate an email with the publisher name and a random email service
                pubEmail = '_'.join(pub.split()) + EMAIL_SERVICES[randint(0, len(EMAIL_SERVICES))-1]
                cur.execute('''insert into publisher(name, email_address, institution_no, transit_no, account_no)
                                values(%s, %s, %s, %s, %s) returning publisher_id''',
                                (pub, pubEmail, generateNumber(3), generateNumber(5), generateNumber(7)))
                conn.commit()
                # print("Inserted publisher")
                pub_id = cur.fetchone()[0]

                cur.execute('''insert into publisher_phone
                                values(%s, %s)''', (pub_id, pubPhone))
                conn.commit()
                # print("Inserted publisher phone")

            cur.execute('''insert into book
                values(%s, %s, %s, %s, %s, %s, %s, %s)''',
                (isbn, pub_id, title, genre, quantity, price, numPages, pubPercentage))
            conn.commit()
            print("Inserted book")

            for author in authors:
             
                first_name = author.split()[0]
                #if the author has a middle name then make sure the last name is assigned properly
                if len(author.split()) == 1:
                    last_name = ''
                elif len(author.split()) == 2:
                    last_name = author.split()[1]
                else:
                    last_name = author.split()[2]

                cur.execute('''insert into author
                                values(%s, %s, %s)''',
                                (isbn, first_name, last_name))
                
            
            conn.commit()
            print("Inserted authors")



                    

                    
                
    except Exception as sqlErr:
        print("Could not insert tuple", sqlErr)


def removeBook(isbn:str):
    try:
        cur.execute('''delete from book
                        where ISBN = %s''', (isbn,))
        conn.commit()
    
    except Exception as sqlErr:
        print("Could not delete tuple", sqlErr)
    
    print("Removed book with ISBN:", isbn)

def generateSalesPerGenreReport()->tuple:
    results = None
    try:
        cur.execute("select * from sales_per_genre")
        conn.commit()
        results = cur.fetchall()
        
    except Exception as sqlErr:
        print("An error occured", sqlErr)

    finally:
        return results

def generateSalesPerAuthorReport()->tuple:
    results = None
    try:
        cur.execute("select * from sales_per_author")
        conn.commit()
        results = cur.fetchall()
        
    except Exception as sqlErr:
        print("An error occured", sqlErr)

    finally:
        return results

def generateSalesVsExpenditureReport()->tuple:
    results = None
    try:
        cur.execute("select * from sales_vs_expenditure") 
        conn.commit()
        results = cur.fetchall()
        
    except Exception as sqlErr:
        print("An error occured", sqlErr)

    finally:
        return results

def displaySalesPerGenreReport(report:tuple):
    if(report):
        t = PrettyTable(['Genre', 'Sales($)'])
        for i in range(len(report)):
            t.add_row([report[i][0], report[i][1]])

    print(t)

def displaySalesPerAuthorReport(report:tuple):
    if(report):
        t = PrettyTable(['First Name', 'Last Name', 'Sales($)'])
        for i in range(len(report)):
           t.add_row([report[i][0], report[i][1], report[i][2]])

    print(t)

def displaySalesVsExpenditureReport(report:tuple):
    if(report):
        t = PrettyTable(['ISBN', 'Title', 'Expenditure($)', 'Sales($)'])
        for i in range(len(report)):
           t.add_row([report[i][0], report[i][1], report[i][2], report[i][3]])
           
    print(t)
    



def main():
    print("Welcome to Look-Inna-Book-Store!!")
    print("1. Owner")
    print("2. User")
    owner = False
    badInput = True
    inMainMenu = False
    shoppingCart = []
    subTotal = 0
    
    

 
    while badInput:
        try:
            accountType = int(input("Select your course of action: "))

            if(accountType in [1,2]):
                break
            else:
                print("Please select 1 or 2...")
        except ValueError:
            print("Please select 1 or 2...")
    
    if(accountType == 1):
        owner = True
    
    print("1. Register")
    print("2. Sign-In")

    while badInput:
        try:
            entranceType = int(input("Select your course of action: "))
            if(entranceType in [1,2]):
                break
            else:
                print("Please select either 1 or 2")
                continue
        except ValueError:
            print("Please select 1 or 2: ")

    if(not owner):
        #If registering
        if(entranceType == 1):
            fName = input("First Name: ")
            lName = input("Last Name: ")
            email = input("Email Address: ")
            passwd = input("Password: ")
            sAddr = input("Shipping Address: ")
            bAddr = input("Billing Address: ")
            numPhones = int(input("How many phone numbers do you have? "))
            phoneNumbers = []
            i = 0
            while badInput and numPhones > 0:
                try:
                    phoneNum = int(input("Please enter phone number %d:" % (i+1)))
                    if(len(str(phoneNum)) < 10 or len(str(phoneNum)) > 11):
                        print("Please enter a 10 or 11 digit number")
                        continue
                    else:
                        if(int(str(phoneNum)[:3]) not in AREACODES):
                            print("Please enter a Canadian number")
                            continue
                        phoneNumbers.append(phoneNum)
                        i += 1
                        if(i == numPhones):
                            break
                except ValueError:
                    print("Please enter actual numbers...")
                



            userTuple = userRegister(fName, lName, email, passwd, sAddr, bAddr, phoneNumbers)
            if(userTuple):
                print("Congrats on becoming a member!")
            else:
                print("This account already exists")
                return
                
        
        #If user is signing in
        elif entranceType == 2:
            email = input("Email Address: ")
            passwd = input("Password: ")
            userTuple = userSignIn(email, passwd)
            if(userTuple):
                print("Welcome back!")

            else:
                print("Invalid login details")
                return
                
    
    #If owner
    else:
        #If registering
        if(entranceType == 1):
            email = input("Email Address: ")
            passwd = input("Password: ")
            if(ownerRegister(email, passwd)):
                print("Congrats on becoming an owner!")
            else:
                print("This account already exists")
                return
                
        
        #If signing in
        elif entranceType == 2:
            email = input("Email Address: ")
            passwd = input("Password: ")
            if(ownerSignIn(email, passwd)):
                print("Welcome back boss")
            else:
                print("Invalid login details")
                return
                
            
    inMainMenu = True
    while inMainMenu:
        if(owner):
            displayOwnerMenu()
            
        else:
            displayCart(shoppingCart, subTotal)
            displayUserMenu()
            
        
        while badInput:
            try:
                mainMenu = int(input("Please select an option: "))
                if(owner and mainMenu in [0,1,2,3,4,5,6,7,8,9] or (not owner and mainMenu in [0,1,2,3,4,5,6])):
                    break
                elif owner:
                    print("Please select an option from 0 to 9: ")
                else:
                    print("Please select an option from 0 to 6: ")
                continue
            except ValueError:
                print("Please enter actual numbers...")




        if(mainMenu == 0):
            break

        elif(mainMenu == 1):
            while badInput:
                try:
                    searchValue = int(input("Enter an ISBN: "))
                    if(len(str(searchValue))!=13):
                        print("Please enter a 13 digit number")
                        continue
                    else:
                        break
                except ValueError:
                    print("ISBNs don't have letters...")
                    continue
            bookTuple = searchByISBN(str(searchValue))

            print("0. Exit to Main Menu")
            #If the book is in the database
            if(bookTuple):
                print("1. Add to Cart")

                while badInput:
                    try:
                        buy = int(input("Please select an option: "))
                        break
                    except ValueError:
                        print("Please select 0 or 1")
                if(buy == 1):
                    while badInput:
                        try:
                            quantity = int(input("How many? "))
                            #If the customer wants to purchase more than what's in stock
                            if(quantity > bookTuple[4]):
                                print("The store does not have that many of this book")
                                continue
                            break
                        except ValueError:
                            print("Please choose an integer")
                    bookDict = {"ISBN": bookTuple[1], "title": bookTuple[2], "stockQuantity":bookTuple[4], "inCartQuantity": quantity, "price": bookTuple[5]}

                    foundBook = False
                    for i in range(len(shoppingCart)):
                        if shoppingCart[i]["ISBN"] == bookDict["ISBN"]:
                            shoppingCart[i]["inCartQuantity"]+=quantity
                            subTotal+= bookDict["price"]*quantity
                            foundBook = True
                            break
                    if(not foundBook):
                        subTotal+= bookDict["price"]*quantity
                        shoppingCart.append(bookDict)
            else:
                continue
                

        else:
            if mainMenu == 2:
                searchValue = input("Enter a book title: ")
                if searchByTitle(searchValue):
                    print("0. Exit to Main Menu")
                    
            elif mainMenu == 3:
                searchValue = input("Enter an author: ")
                if searchByAuthor(searchValue):
                    print("0. Exit to Main Menu")
                
            elif mainMenu == 4:
                searchValue = input("Enter a book genre: ")
                if searchByGenre(searchValue):
                    print("0. Exit to Main Menu")
            
            elif not owner:
                if mainMenu == 5:
                    if(len(shoppingCart)>0):
                        shippingAddr = input("Is your shipping address the same as your in profile? y or n: ")

                        if(shippingAddr == 'y'):
                            shippingAddr = userTuple[5]
                        else:
                            shippingAddr = input("Please enter the shipping address for the order")

                        billingAddr = input("Is your billing address the same as your in profile? y or n: ")

                        if(billingAddr == 'y'):
                            billingAddr = userTuple[6]
                        else:
                            billingAddr = input("Please enter the billing address for the order")
                        
                        placeOrder(shoppingCart, subTotal, userTuple[0], shippingAddr, billingAddr)
                        shoppingCart = []
                        subTotal = 0
                        continue
                    else:
                        print("Your cart is empty....")
                        continue
        
            
                elif mainMenu == 6:
                    while badInput:
                        try:
                            orderNum = int(input("What is the order number? : "))
                            break
                        except ValueError:
                            print("Please enter a number")
                    displayOrder(getOrder(orderNum, userTuple))
                    continue
                    

            
            else:
                if mainMenu in [5,6]:
                    while badInput:
                        try:
                            newBook = int(input("Enter an ISBN: "))
                            if(len(str(newBook))!=13):
                                print("Please enter a 13 digit number")
                                continue
                            else:
                                break
                        except ValueError:
                            print("ISBNs don't have letters...")
                            continue
                    if mainMenu == 5:
                        addBook(str(newBook))
                    elif mainMenu == 6:
                        removeBook(str(newBook))
                
                elif mainMenu == 7:
                    pass
                    report = generateSalesVsExpenditureReport()
                    displaySalesVsExpenditureReport(report)


                elif mainMenu == 8:
                    report = generateSalesPerGenreReport()
                    displaySalesPerGenreReport(report)
                

                
                elif mainMenu == 9:
                    report = generateSalesPerAuthorReport()
                    displaySalesPerAuthorReport(report)

                    


    
    print("Come again soon! :)")

            
      
                
            
            

    


            







main()
