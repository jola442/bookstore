import requests
import json
# import psycopg2
# from random import randint
from os.path import exists

areaCodes = [204, 226, 236, 249, 250, 289,
             306, 343, 365, 367,
             403, 416, 418, 431, 437, 438, 450,
             506, 514, 519, 548, 579, 581, 587, 
             604, 613, 639, 647,
             705, 709, 778, 780, 782, 
             807, 819, 825, 867, 873, 
             902, 905]
# MINQUANTITY = 10
# MAXQUANTITY = 20
# MINPERCENTAGE = 10
# MAXPERCENTAGE = 20

# prices = [9.99, 10.99, 11.99, 12.99, 13.99, 14.99, 15.99, 16.99, 17.99, 18.99, 19.99, 20.00]
api = "https://www.googleapis.com/books/v1/volumes?&key=AIzaSyBu8qslMt65MSFTbfCXy0qZfIcweZmdAmg"


#generate a random n number string
# def generateNumber(n):
#     result = ''
#     for i in range(n):
#         result += str(randint(0, 9))
#     return result

#sample isbn 9780063078505
#9780525620754
#9780553496673
def main():
    while True:
        choice = input("Would you like to enter an ISBN? y or n: ").lower().strip()
        if(choice == 'y'):
            isbn = input("Please enter an ISBN: ").strip()
            parameters = {
                "q": "isbn:"+isbn

            }
            response = requests.get(api, params=parameters)
            results = response.json()
            try:
                bookDict = results["items"][0]
                print(bookDict)
            except KeyError:
                print("This IBN does not exist")
                break
            # print(bookData.keys())
            # print(bookData["saleInfo"])
            bookData = bookDict["volumeInfo"]
            title = bookData["title"]
            authors = bookData["authors"]
            num_pages = bookData["pageCount"]
            publisher = bookData["publisher"]
            # publisher_phone_number = str(areaCodes[randint(0, len(areaCodes)-1)]) + generateNumber(7)

            newBookDict = {isbn: {"ISBN": isbn, "title": title, "authors": authors, "num_pages": num_pages, "publisher": publisher}}
            
            #convert to json
            newJSON = json.dumps(newBookDict, indent=4)

            file_exists = exists("./books.json")
            if(not file_exists):
                try:
                    f = open("books.json", mode = 'w')
                    f.write(newJSON)
                    print("Created book.json with book titled:", newBookDict[isbn]["title"])
                # except:
                #     print("An error occured")
                
                finally:
                    f.close()
            
            else:
                with open("books.json", 'r+') as file:
                    file_data = json.load(file)
                    file_data.update(newBookDict)
                    print("Added book with title:", newBookDict[isbn]["title"])
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
