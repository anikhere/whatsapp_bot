import psycopg2
import os

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="YourNewPassword123",   # <-- your new password
        port=5432
    )
