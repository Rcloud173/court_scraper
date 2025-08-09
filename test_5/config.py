# import sqlite3

# # Connect to the database
# conn = sqlite3.connect("judgments.db")

# # Create a cursor
# cursor = conn.cursor()

# # Run the query
# cursor.execute("SELECT COUNT(*) FROM judgments;")
# result = cursor.fetchone()

# # Print the result
# print("Total judgments:", result[0])

# # Clean up
# conn.close()

# config.py
import pathlib

# Project base directory
BASE_DIR = pathlib.Path(__file__).resolve().parent

# Database path
DB_PATH = BASE_DIR / "database" / "judgments.db"

# Ensure database folder exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
