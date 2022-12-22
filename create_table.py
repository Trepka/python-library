import psycopg2
from config import config

def create_tables():
    commands = (
        """
        CREATE EXTENSION citext;
        CREATE DOMAIN email AS citext
        CHECK ( value ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );
        """,
        """
        CREATE DOMAIN phone_number AS TEXT
        CHECK(VALUE ~ '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$');
        """,
        """
        CREATE TABLE IF NOT EXISTS cupboards(
            shelf_id SERIAL PRIMARY KEY,
            cupboard_id INT NOT NULL,
            shelf INT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS books(
            book_id SERIAL PRIMARY KEY,
            ISBN BIGINT,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            publisher VARCHAR(255) NOT NULL,
            year INT NOT NULL,
            jenre VARCHAR(255) NOT NULL,
            shelf_id INT,
            CONSTRAINT fk_shelf
                FOREIGN KEY(shelf_id)
                    REFERENCES cupboards(shelf_id)
                    ON DELETE SET NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS readers(
            reader_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            second_name VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            reg_date DATE NOT NULL DEFAULT CURRENT_DATE,
            email email,
            phone_number phone_number
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders(
            order_id SERIAL PRIMARY KEY,
            receive_date DATE NOT NULL DEFAULT CURRENT_DATE,
            return_date DATE NOT NULL,
            reader_id SERIAL,
            book_id SERIAL,
            CONSTRAINT fk_reader_id
                FOREIGN KEY(reader_id)
                    REFERENCES readers(reader_id),
            CONSTRAINT fk_book_id
                FOREIGN KEY(book_id)
                    REFERENCES books(book_id)
        );
        """
    )

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)
        
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()