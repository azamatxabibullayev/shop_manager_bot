import sqlite3
from config import DATABASE


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_number INTEGER UNIQUE,
            name TEXT,
            details TEXT,
            registration_certificate TEXT, 
            contract_pdf TEXT,            
            cadastre_pdf TEXT,              
            lease_contract_pdf TEXT,       
            photo TEXT,                     
            area REAL                       
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id INTEGER,
            month TEXT,                      
            area REAL,                      
            rate REAL,                       
            calculated_amount REAL,          
            previous_balance REAL,           
            paid_amount REAL,                
            due_amount REAL,                 
            tax_amount REAL,                 
            FOREIGN KEY(shop_id) REFERENCES shops(id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS electricity_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id INTEGER,
            month TEXT,
            previous_reading INTEGER,       
            current_reading INTEGER,         
            used INTEGER,                    
            rate INTEGER,                    
            calculated_amount INTEGER,       
            paid_amount INTEGER,            
            balance INTEGER,                 
            overpayment INTEGER,             
            FOREIGN KEY(shop_id) REFERENCES shops(id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id INTEGER,
            month TEXT,
            service_total REAL,            
            service_received REAL,          
            monthly_collection REAL,         
            yearly_collection REAL,         
            unpaid_shops TEXT,               
            FOREIGN KEY(shop_id) REFERENCES shops(id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
