import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="travel"
)
cursor = conn.cursor()

# Function to create a new user
def create_user(username, password):
    # Check if user with the same username already exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        messagebox.showerror("Error", "User with the same username already exists.")
        return

    # Insert user into the database
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    messagebox.showinfo("Success", "User created successfully.")

# Function to authenticate a user
def authenticate_user(username, password):
    # Check if username and password match in the database
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    return user is not None

# Function to update user password
def update_password(username, new_password):
    # Update user password
    cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
    conn.commit()
    messagebox.showinfo("Success", "Password updated successfully.")

# Function to delete a user
def delete_user(username):
    # Delete user from the database
    cursor.execute("DELETE FROM users WHERE username=%s", (username,))
    conn.commit()
    messagebox.showinfo("Success", "User deleted successfully.")

# Function to create a new user - GUI version
def create_user_gui():
    def submit_user():
        username = username_entry.get()
        password = hashlib.sha256(password_entry.get().encode()).hexdigest()
        create_user(username, password)

    create_window = tk.Toplevel(root)
    create_window.title("Create User")

    tk.Label(create_window, text="Username:").pack()
    username_entry = tk.Entry(create_window)
    username_entry.pack()

    tk.Label(create_window, text="Password:").pack()
    password_entry = tk.Entry(create_window, show="*")
    password_entry.pack()

    submit_button = tk.Button(create_window, text="Submit", command=submit_user)
    submit_button.pack()

# Function to authenticate a user - GUI version
def authenticate_user_gui():
    def login_user():
        username = username_entry.get()
        password = hashlib.sha256(password_entry.get().encode()).hexdigest()
        if authenticate_user(username, password):
            messagebox.showinfo("Success", "Login successful.")
            main_menu()
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=login_user)
    login_button.pack()

# Function to display the main menu
def main_menu():
    main_window = tk.Toplevel(root)
    main_window.title("Main Menu")

    tk.Label(main_window, text="Welcome to the Travel Planner App!").pack()

    generate_report_button = tk.Button(main_window, text="Generate Report", command=generate_report)
    generate_report_button.pack()

    create_itinerary_button = tk.Button(main_window, text="Create Itinerary with Budget and Save", command=create_itinerary_with_budget_and_save)
    create_itinerary_button.pack()

    destinations_button = tk.Button(main_window, text="Input Destinations", command=destinations)
    destinations_button.pack()

    search_destinations_button = tk.Button(main_window, text="Search Destinations", command=search_destinations_gui)
    search_destinations_button.pack()

    logout_button = tk.Button(main_window, text="Logout", command=root.deiconify)
    logout_button.pack()

# Function to handle user logout
def logout():
    conn.close()
    root.destroy()

# Function to handle search destinations - GUI version
def search_destinations_gui():
    def search():
        location = location_entry.get()
        budget = budget_entry.get()
        activities = activities_entry.get()
        weather = weather_entry.get()

        search_results = search_destinations(location, budget, activities, weather)

        search_window = tk.Toplevel(root)
        search_window.title("Search Results")

        tk.Label(search_window, text="Search Results:").pack()
        for idx, destination in enumerate(search_results, start=1):
            tk.Label(search_window, text=f"{idx}. {destination}").pack()

    search_window = tk.Toplevel(root)
    search_window.title("Search Destinations")

    tk.Label(search_window, text="Enter Location:").pack()
    location_entry = tk.Entry(search_window)
    location_entry.pack()

    tk.Label(search_window, text="Enter Budget:").pack()
    budget_entry = tk.Entry(search_window)
    budget_entry.pack()

    tk.Label(search_window, text="Enter Activities:").pack()
    activities_entry = tk.Entry(search_window)
    activities_entry.pack()

    tk.Label(search_window, text="Enter Weather:").pack()
    weather_entry = tk.Entry(search_window)
    weather_entry.pack()

    search_button = tk.Button(search_window, text="Search", command=search)
    search_button.pack()

# Function to generate report
def generate_report():
    # Execute query to fetch destinations data
    cursor.execute("SELECT * FROM destinations")
    destinations_data = cursor.fetchall()

    # Print destinations data
    print("Destinations:")
    print("ID\tLocation\tBudget\tActivities\tWeather")
    for destination in destinations_data:
        print(f"{destination[0]}\t{destination[1]}\t{destination[2]}\t{destination[3]}\t{destination[4]}")

    print()

    # Execute query to fetch users data
    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()

    # Print users data
    print("Users:")
    print("ID\tUsername\tPassword")
    for user in users_data:
        print(f"{user[0]}\t{user[1]}\t{user[2]}")

# Function to create a custom itinerary with budget tracking and save it to SQL
def create_itinerary_with_budget_and_save():
    print("Welcome to Itinerary Creation with Budget Tracking and SQL Saving!")

    # Get user input for itinerary details
    num_destinations = int(input("How many destinations do you want to include in your itinerary? "))

    total_budget = float(input("Enter your total budget for the trip: "))
    remaining_budget = total_budget

    itinerary = []

    for i in range(num_destinations):
        print(f"\nDestination {i + 1}:")
        destination = input("Enter destination: ")
        activities = input("Enter preferred activities separated by commas: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        transportation = input("Enter preferred transportation (e.g., flight, train): ")
        accommodation = input("Enter preferred accommodation (e.g., hotel, Airbnb): ")

        destination_budget = float(input(f"Enter budget for {destination}: "))
        remaining_budget -= destination_budget

        # Create a dictionary for each destination
        destination_info = {
            "Destination": destination,
            "Activities": activities,
            "Start Date": start_date,
            "End Date": end_date,
            "Transportation": transportation,
            "Accommodation": accommodation,
            "Budget": destination_budget
        }

        # Append the destination info to the itinerary list
        itinerary.append(destination_info)

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS itineraries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            destination VARCHAR(100) NOT NULL,
            activities TEXT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            transportation VARCHAR(100),
            accommodation VARCHAR(100),
            budget FLOAT NOT NULL
            );
            '''
        )
        # Insert data into SQL table
        cursor.execute("""
            INSERT INTO itineraries (destination, activities, start_date, end_date, transportation, accommodation, budget) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (destination, activities, start_date, end_date, transportation, accommodation, destination_budget))
        conn.commit()

    # Print the generated itinerary
    print("\nYour Custom Itinerary with Budget Tracking and SQL Saving:")
    for idx, destination_info in enumerate(itinerary, start=1):
        print(f"\nDestination {idx}:")
        for key, value in destination_info.items():
            print(f"{key}: {value}")

    print(f"\nRemaining budget after all destinations: ${remaining_budget:.2f}")

# Function to search destinations based on filters
def search_destinations(location=None, budget=None, activities=None, weather=None):
    # Base query
    query = "SELECT DISTINCT * FROM destination WHERE 1"

    # Add filters to the query
    if location:
        query += " AND location LIKE '%" + location + "%'"
    if budget:
        query += " AND budget <= " + str(budget)
    if activities:
        query += " AND activities LIKE '%" + activities + "%'"
    if weather:
        query += " AND weather LIKE '%" + weather + "%'"

    print("Query:", query)

    # Execute the query
    cursor.execute(query)
    destinations = cursor.fetchall()

    return destinations

# Function to get user input for destination
def get_user_input():
    print("Choose filters you want to apply (Enter 'none' if you don't want to apply a filter):")
    location = input("Enter the location (or 'none'): ")
    budget = input("Enter your budget (or 'none'): ")
    activities = input("Enter preferred activities (or 'none'): ")
    weather = input("Enter preferred weather (or 'none'): ")
    return location if location.lower() != 'none' else None, \
           float(budget) if budget.lower() != 'none' else None, \
           activities if activities.lower() != 'none' else None, \
           weather if weather.lower() != 'none' else None

# Function to input destinations
def destinations():
    # Get user input for country
    country = input("Enter the country (or 'none'): ")

    # Modify the example_query based on the user input
    example_query = f"""
    SELECT DISTINCT 
        d.location,
        d.budget,
        d.activities,
        d.weather,
        a.name AS attraction_name,
        a.description AS attraction_description,
        acc.name AS accommodation_name,
        acc.description AS accommodation_description,
        r.name AS restaurant_name,
        r.cuisine,
        t.mode AS transportation_mode,
        t.description AS transportation_description
    FROM 
        destinations d
    LEFT JOIN 
        attractions a ON d.id = a.destination_id
    LEFT JOIN 
        accommodations acc ON d.id = acc.destination_id
    LEFT JOIN 
        restaurants r ON d.id = r.destination_id
    LEFT JOIN 
        transportation_options t ON d.id = t.destination_id
    """

    # Add the WHERE clause to the query if location is provided
    if country.lower() != 'none':
        example_query += f"WHERE d.location LIKE '%{country}%'"

    # Execute the example query
    cursor.execute(example_query)
    result = cursor.fetchall()
    # Keep track of seen destinations
    seen_destinations = set()

    # Display the result, only print each destination once
    for row in result:
        destination = row[1]  # Assuming the second column is the destination name
        if destination not in seen_destinations:
            seen_destinations.add(destination)
            print(row)

# Close the database connection when root window is closed
def on_closing():
    conn.close()
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Travel Planner")

# Create buttons for different functionalities
create_user_button = tk.Button(root, text="Create User", command=create_user_gui)
create_user_button.pack()

login_button = tk.Button(root, text="Login", command=authenticate_user_gui)
login_button.pack()

# Bind the logout function to the root window closing event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main event loop
root.mainloop()