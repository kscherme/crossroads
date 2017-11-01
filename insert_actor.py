from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def _insert_actor(name):
    query = "INSERT INTO Actors (name)" \
            "VALUES(%s)"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def main():
    _insert_actor('test_actor')

if __name__ == '__main__':
    main()
