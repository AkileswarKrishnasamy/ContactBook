import mysql.connector
from mysql.connector import Error

class ContactBook:
    def __init__(self) -> None:
        # Pass your server connection details
        self.connection = self.create_server_connection("localhost", "root", "Auth(sql)","contacts")
        self.create_table()

    # Method to create table 
    def create_table(self)->None:
        sql_user ='''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        username TEXT,
        password TEXT
        );'''
        sql_contact = '''CREATE TABLE IF NOT EXISTS ContactBK(
        id INTEGER,
        name TEXT,
        phonenumber TEXT,
        email TEXT,
        city TEXT,
        contact_id INTEGER PRIMARY KEY AUTO_INCREMENT,
        FOREIGN KEY (id) REFERENCES users(id)
        );'''

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_user)
            cursor.execute(sql_contact)
            self.connection.commit()
            cursor.close()
            print("Tables created successfully")
        except Error as err:
            print(f"Error: '{err}'")

    # Method to login
    def login(self,user,passw):
        try:
            query = 'SELECT id FROM users WHERE username = %s AND password = %s;'
            cursor = self.connection.cursor()
            cursor.execute(query, (user, passw))
            result = cursor.fetchone()
            ContactBook.id = result[0]
            return True
        except:
            print("entered credentials are wrong")
            return False
    
    # Method to update contacts
    def update_contacts(self,id,name,phoneno,email,city,contactid):
        query = '''UPDATE ContactBK
        SET
            name = %s,
            phonenumber = %s,
            email = %s,
            city = %s
        WHERE
        id = %s AND contact_id= %s;'''
        try:

            cursor = self.connection.cursor()
            cursor.execute(query,(name,phoneno,email,city,id,contactid))
            self.connection.commit()
            return True
        except:
            return False
        
    # Method to manage contacts
    def manage_contacts(self):
        query = '''SELECT * FROM ContactBK WHERE id=%s'''
        try:

            cursor = self.connection.cursor()
            cursor.execute(query,(ContactBook.id,))
            return cursor.fetchall()
        except:
            print("No Contacts found")

    # Method to add contacts
    def add_contacts(self,name,phonenumber,email,city):
        query= '''INSERT INTO ContactBK (name, phonenumber, email, city,id) VALUES
                    (%s,%s,%s,%s,%s);
                    '''
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(name,phonenumber,email,city,ContactBook.id))
            self.connection.commit()
            cursor.close()
            print("Inserted Successfully")
            return True
        except Error as err:
            print(f"Error: '{err}'")
    
    # Method to delete contacts
    def delete_contacts(self,contactid,id):
        query = '''DELETE FROM ContactBK WHERE contact_id=%s AND id=%s'''
        try:

            cursor = self.connection.cursor()
            cursor.execute(query,(contactid,id))
            self.connection.commit()
            return True
        except:
            print("No Contact found")
    
    # Method to change password
    def change_password(self,old_passwowrd,new_password):
        cursor = self.connection.cursor()
        old_query = '''SELECT password FROM users WHERE id = %s'''
        cursor.execute(old_query,(ContactBook.id,))
        old = cursor.fetchone()
        if old_passwowrd == old[0]:
            try:
                new_query = '''UPDATE users SET password =%s WHERE id = %s'''
                cursor.execute(new_query,(new_password,ContactBook.id))
                self.connection.commit()
                return True
            except:
                return False

    # Method to create server connection
    def create_server_connection(self,host_name, user_name, user_password,db):
        self.connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database = db
             )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
    

    



if __name__ == "__main__":
    book = ContactBook()




