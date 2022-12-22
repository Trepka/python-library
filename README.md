## About library script

Create_table.py is a simple script for create basic number of tables for library. Python version used 3.10.6, PostgreSQL version 15.

For use this script on your own machine you must make database.ini file with your own settings. 

```
[postgresql]
host=localhost
database=db_name
user=user
password=password
port=5433
```

### Database entity relationship model
![Database ER model](assets/images/erd.png)

### Tables description

1. Cupboards table includes information about all cupboards and shelfs
    - shlef_id unique key for every cupboard and shelf combination
    - cupboard_id cupboadr number
    - shelf shelf number for single cumpoard
2. Books table store information about every single book
    - book_id unique integer key for our DB
    - ISBN identifier for every book
    - title 
    - author
    - publisher
    - year when book was published
    - jenre
    - shelf_id is foreign key for cupboards.shelf_id key
3. Readers table store all necessary information about every reader
    - reader_id
    - first_name
    - second_name
    - birth_date
    - reg_date date whe reader register in library
    - email is domain made data type "email"
    - phone_number is domain made data type "phone_number"
4. Orders table store all records when readers take book from library
    - order_id 
    - receive_date date when reader take book from library
    - return_date date when reader must return book
    - reader_id foreign key for readers.reader_id
    - book_id is foreign key for books.books_id

### Join query for database

Query returns reader name, phone number, book ID and title, cupboard and shelf for this book where return date between '2022-12-01' AND '2022-12-31'

```
SELECT r.first_name readerName,
r.phone_number phone,
o.book_id bookID,
o.return_date returnDate,
b.title title,
cup.cupboard_id,
cup.shelf shelf
FROM readers r
JOIN orders o ON r.reader_id = o.reader_id
JOIN books b ON o.book_id = b.book_id
JOIN cupboards cup ON cup.shelf_id = b.shelf_id
WHERE o.receive_date BETWEEN '2022-12-01' AND '2022-12-31';
```