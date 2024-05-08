import tkinter as tk
from tkinter import messagebox, simpledialog
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
    """
    Create a new user in the database.
    """
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        messagebox.showerror("Error", "User with the same username already exists.")
        return
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    messagebox.showinfo("Success", "User created successfully.")

# Function to authenticate a user
def authenticate_user(username, password):
    """
    Authenticate a user.
    """
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    return user is not None

# Function to update user password
def update_password(username, new_password):
    """
    Update user's password.
    """
    cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
    conn.commit()
    messagebox.showinfo("Success", "Password updated successfully.")

# Function to delete a user
def delete_user(username):
    """
    Delete a user from the database.
    """
    cursor.execute("DELETE FROM users WHERE username=%s", (username,))
    conn.commit()
    messagebox.showinfo("Success", "User deleted successfully.")

# Function to create a new user - GUI version
def create_user_gui():
    """
    GUI for creating a new user.
    """
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
    """
    GUI for authenticating a user.
    """
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
    """
    Display the main menu.
    """
    main_window = tk.Toplevel(root)
    main_window.title("Main Menu")

    tk.Label(main_window, text="Welcome to the Travel Planner App!").pack()

    generate_report_button = tk.Button(main_window, text="Generate Report", command=generate_report_gui)
    generate_report_button.pack()

    create_itinerary_button = tk.Button(main_window, text="Create Itinerary with Budget and Save", command=create_itinerary_with_budget_and_save)
    create_itinerary_button.pack()

    destinations_button = tk.Button(main_window, text="Input Destinations", command=input_destinations)
    destinations_button.pack()

    search_destinations_button = tk.Button(main_window, text="Search Destinations", command=search_destinations_gui)
    search_destinations_button.pack()

    logout_button = tk.Button(main_window, text="Logout", command=logout)
    logout_button.pack()

# Function to handle user logout
def logout():
    """
    Handle user logout.
    """
    conn.close()
    root.destroy()

# Function to generate report - GUI version
def generate_report_gui():
    """
    Generate report GUI.
    """
    # Execute query to fetch itineraries data
    cursor.execute("SELECT * FROM itineraries")
    itineraries_data = cursor.fetchall()

    report = "Itineraries:\n"
    report += "ID\tDestination\tActivities\tStart Date\tEnd Date\tTransportation\tAccommodation\tBudget\n"
    for itinerary in itineraries_data:
        report += f"{itinerary[0]}\t{itinerary[1]}\t{itinerary[2]}\t{itinerary[3]}\t{itinerary[4]}\t{itinerary[5]}\t{itinerary[6]}\t{itinerary[7]}\n"

    report_window = tk.Toplevel(root)
    report_window.title("Generated Report")

    report_label = tk.Label(report_window, text=report)
    report_label.pack()

# Function to create a custom itinerary with budget tracking and save it to SQL
def create_itinerary_with_budget_and_save():
    """
    Create itinerary with budget tracking and save to SQL.
    """
    print("Welcome to Itinerary Creation with Budget Tracking and SQL Saving!")

    # Get user input for itinerary details
    num_destinations = int(simpledialog.askstring("Input", "How many destinations do you want to include in your itinerary?"))

    total_budget = float(simpledialog.askstring("Input", "Enter your total budget for the trip:"))
    remaining_budget = total_budget

    itinerary = []

    # Table creation query
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

    for i in range(num_destinations):
        destination = simpledialog.askstring("Input", f"Enter destination {i + 1}:")
        activities = simpledialog.askstring("Input", "Enter preferred activities separated by commas:")
        start_date = simpledialog.askstring("Input", "Enter start date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")
        transportation = simpledialog.askstring("Input", "Enter preferred transportation (e.g., flight, train):")
        accommodation = simpledialog.askstring("Input", "Enter preferred accommodation (e.g., hotel, Airbnb):")
        destination_budget = float(simpledialog.askstring("Input", f"Enter budget for {destination}:"))
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
def search_destinations(location=None, budget=None, activities=None, weather=None):
    """
    Search destinations based on filters.
    """
    # Base query
    query = "SELECT DISTINCT * FROM destination WHERE 1"

    # Add filters to the query
    if location:
        query += f" AND location LIKE '%{location}%'"
    if budget:
        if budget != 'none':
            query += f" AND budget <= {budget}"
    if activities:
        if activities != 'none':
            query += f" AND activities LIKE '%{activities}%'"
    if weather:
        if weather != 'none':
            query += f" AND weather LIKE '%{weather}%'"

    print("Query:", query)

    # Execute the query
    cursor.execute(query)
    destinations = cursor.fetchall()

    return destinations
# Function to search destinations based on filters
def search_destinations_gui():
    """
    GUI for searching destinations based on filters.
    """
    def search():
        # Get the input values
        location = location_entry.get()
        budget = budget_entry.get()
        activities = activities_entry.get()
        weather = weather_entry.get()
        
        # Call the search_destinations function with the provided filters
        destinations = search_destinations(location, budget, activities, weather)
        
        # Display the results in a new window
        results_window = tk.Toplevel(root)
        results_window.title("Search Results")
        
        if destinations:
            result_label = tk.Label(results_window, text="Search Results:")
            result_label.pack()
            
            for destination in destinations:
                destination_label = tk.Label(results_window, text=destination)
                destination_label.pack()
        else:
            no_results_label = tk.Label(results_window, text="No results found.")
            no_results_label.pack()

    search_window = tk.Toplevel(root)
    search_window.title("Search Destinations")

    # Create input fields for filters
    tk.Label(search_window, text="Location:").grid(row=0, column=0)
    location_entry = tk.Entry(search_window)
    location_entry.grid(row=0, column=1)

    tk.Label(search_window, text="Budget:").grid(row=1, column=0)
    budget_entry = tk.Entry(search_window)
    budget_entry.grid(row=1, column=1)

    tk.Label(search_window, text="Activities:").grid(row=2, column=0)
    activities_entry = tk.Entry(search_window)
    activities_entry.grid(row=2, column=1)

    tk.Label(search_window, text="Weather:").grid(row=3, column=0)
    weather_entry = tk.Entry(search_window)
    weather_entry.grid(row=3, column=1)

    search_button = tk.Button(search_window, text="Search", command=search)
    search_button.grid(row=4, columnspan=2)

def input_destinations():
    """
    Input destinations.
    """
    country = simpledialog.askstring("Input", "Enter the country (or 'none'):")

    example_query = f"""
    SELECT DISTINCT 
        d.location,
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
        destination d
    LEFT JOIN 
        attractions a ON d.id = a.destination_id
    LEFT JOIN 
        accommodations acc ON d.id = acc.destination_id
    LEFT JOIN 
        restaurants r ON d.id = r.destination_id
    LEFT JOIN 
        transportation_options t ON d.id = t.destination_id
    """

    if country.lower() != 'none':
        example_query += f" WHERE d.location LIKE '%{country}%'"

    cursor.execute(example_query)
    result = cursor.fetchall()

    seen_destinations = set()

    # Create a new window to display the search results
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")

    # Display the results in the new window
    if result:
        for row in result:
            destination = row[0]  # Assuming the first column is the destination name
            if destination not in seen_destinations:
                seen_destinations.add(destination)
                destination_label = tk.Label(results_window, text=row)
                destination_label.pack()
    else:
        no_results_label = tk.Label(results_window, text="No results found.")
        no_results_label.pack()


# Close the database connection when root window is closed
def on_closing():
    """
    Close the database connection when root window is closed.
    """
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