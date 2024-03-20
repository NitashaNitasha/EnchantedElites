
def fetch_form_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Execute a SELECT query to fetch data from the FormData table
        cursor.execute("SELECT * FROM FormData")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print the fetched data
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print("Error fetching data from SQLite database:", e)

    finally:
        # Close the cursor and the connection
        if conn:
            conn.close()

# Call the function to fetch form data
fetch_form_data()
