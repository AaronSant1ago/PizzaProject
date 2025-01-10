from flask import Flask, request, render_template, g, redirect, url_for
from initialize_data import initialize_database
import sqlite3
import re

#setup basic database
initialize_database()

#flask app setup
app = Flask(__name__)
DATABASE = "database.db"

#regex to only allow letters or spaces no special characters
def is_valid_input(input_string):
    return bool(re.match(r"^[A-Za-z\s]+$", input_string))

#helper function to get the database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

#close the database connection when the app context ends
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return render_template("home.html")

################################################ MANAGER STUFF
@app.route("/manager", methods=["POST", "GET"])
def manager_page():
    db = get_db()
    cursor = db.cursor()
    
    #fetch all names from toppings 
    cursor.execute("SELECT name FROM toppings")
    toppings = [row[0] for row in cursor.fetchall()]
    
    action_message = ""  # Initialize the action message

    #handle all post requests
    if request.method == "POST":
        if "remove" in request.form:
            selected_topping = request.form.get("selectedTopping")
            if selected_topping and is_valid_input(selected_topping) and remove_from_db(selected_topping):
                action_message = f"Successfully removed topping: {selected_topping}"
            else:
                action_message = f"Invalid or non-existent topping: {selected_topping}."
        elif "add" in request.form:
            new_topping = request.form.get("newTopping")
            if new_topping and is_valid_input(new_topping):
                cursor.execute("SELECT name FROM toppings WHERE LOWER(name) = ?", (new_topping.strip().lower(),))
                existing_topping = cursor.fetchone()
                if existing_topping:
                    action_message = f"Topping '{new_topping}' is already in the system."
                else:
                    if add_to_db(new_topping):
                        action_message = f"Successfully added topping: {new_topping}"
                    else:
                        action_message = f"Error adding topping '{new_topping}'."
            else:
                action_message = "Invalid or empty topping name."
        elif "update" in request.form:
            selected_topping = request.form.get("selectedTopping")
            updated_topping = request.form.get("updateTopping")
            if selected_topping and updated_topping and is_valid_input(selected_topping) and is_valid_input(updated_topping):
                if(updateTopping(selected_topping, updated_topping)):
                    action_message = f"Successfully updated topping: {selected_topping} to {updated_topping}"
                else:
                    action_message = f"Error updating topping '{selected_topping}'."
            else:
                action_message = "Invalid or empty selected topping and/or new topping."

    cursor.execute("SELECT name FROM toppings")
    toppings = [row[0] for row in cursor.fetchall()]
        
    return render_template("managerPage.html", toppings=toppings, action_message=action_message)

def add_to_db(topping):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM toppings WHERE name = ?", (topping,))
        if cursor.fetchone():
            return False
        cursor.execute("INSERT INTO toppings (name) VALUES (?)", (topping,))
        db.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding to DB: {e}")
        return False

def remove_from_db(topping):
    try:
        db = get_db()
        cursor = db.cursor()
        topping = topping.strip().lower()
        cursor.execute("SELECT name FROM toppings WHERE LOWER(name) = ?", (topping,))
        row = cursor.fetchone()
        if row:
            cursor.execute("DELETE FROM toppings WHERE LOWER(name) = ?", (topping,))
            db.commit()
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Error removing from DB: {e}")
        return False

def updateTopping(old_topping, new_topping):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM toppings WHERE LOWER(name) = ?", (old_topping.strip().lower(),))
        row = cursor.fetchone()
        if row:
            cursor.execute("SELECT name FROM toppings WHERE LOWER(name) = ?", (new_topping.strip().lower(),))
            existing_topping = cursor.fetchone()
            if existing_topping:
                return False
            else:
                cursor.execute("UPDATE toppings SET name = ? WHERE LOWER(name) = ?", (new_topping.strip(), old_topping.strip().lower()))
                db.commit()
                return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Error updating topping: {e}")
        return False

######################################## END OF Manager Code

######################################## Chef Code
@app.route("/chef", methods=["POST", "GET"])
def chef_page():
    db = get_db()
    cursor = db.cursor()
    action_message = ""

    cursor.execute("SELECT name FROM toppings")
    toppings = [row[0] for row in cursor.fetchall()]

    if request.method == "POST":
        if "addPizza" in request.form:
            #clean up input
            new_pizza_name = request.form.get("newPizzaName").strip()
            topping1 = request.form.get("topping1")
            topping2 = request.form.get("topping2")
            topping3 = request.form.get("topping3")

            if new_pizza_name and topping1 and is_valid_input(new_pizza_name):
                try:
                    #check for duplicates before adding to table
                    cursor.execute("""
                        SELECT 1 FROM pizzas
                        WHERE (topping1 = ? AND (topping2 = ? OR topping2 IS NULL) AND (topping3 = ? OR topping3 IS NULL))
                    """, (topping1, topping2, topping3))

                    if cursor.fetchone():
                        action_message = "A pizza with the same combination of toppings already exists."
                    else:
                        #add to table
                        cursor.execute(
                            "INSERT INTO pizzas (name, topping1, topping2, topping3) VALUES (?, ?, ?, ?)",
                            (new_pizza_name, topping1, topping2, topping3)
                        )
                        db.commit()
                        action_message = f"Pizza '{new_pizza_name}' created successfully."
                except sqlite3.IntegrityError as e:
                    action_message = f"Error: {str(e)}"
            else:
                action_message = "Invalid pizza name or toppings."

        if "updatePizza" in request.form:
            #clean up all input
            oldPizza = request.form.get("pizzaSelect").strip()
            updated_name = request.form.get("pizzaUpdate").strip()
            topping4 = request.form.get("topping4")
            topping5 = request.form.get("topping5")
            topping6 = request.form.get("topping6")

            if updated_name and oldPizza and topping4 and is_valid_input(oldPizza) and is_valid_input(updated_name):
                try:
                    # Check if a pizza with the same toppings already exists
                    cursor.execute("""
                        SELECT 1 FROM pizzas
                        WHERE ((topping1 = ? AND (topping2 = ? OR topping2 IS NULL) AND (topping3 = ? OR topping3 IS NULL))
                        OR (topping1 = ? AND topping2 IS NULL AND topping3 IS NULL))
                        AND name != ?
                    """, (topping4, topping5, topping6, topping4, oldPizza))

                    #we will always fetch back 1 since the old pizza is still in there so if 2 come back that means its a duplicate
                    if cursor.fetchmany(2):
                        action_message = "A pizza with the same combination of toppings already exists."
                    else:
                        #update pizza with sql
                        cursor.execute("""
                            UPDATE pizzas
                            SET name = ?, topping1 = ?, topping2 = ?, topping3 = ?
                            WHERE name = ?
                        """, (updated_name, topping4, topping5, topping6, oldPizza))

                        db.commit()
                        action_message = f"Pizza '{updated_name}' updated successfully."
                #tell dev what went wrong
                except sqlite3.IntegrityError as e:
                    action_message = f"Error: {str(e)}"
            else:
                action_message = "Invalid input for pizza name or toppings."

        if "removePizza" in request.form:
            pizzaName = request.form.get("pizzaSelect").strip()
            if pizzaName and is_valid_input(pizzaName):
                try:
                    #check if pizza exists first
                    cursor.execute("SELECT name FROM pizzas WHERE name = ?", (pizzaName,))
                    row = cursor.fetchone()
                    
                    if row:
                        # delete it 
                        cursor.execute("DELETE FROM pizzas WHERE name = ?", (pizzaName,))
                        db.commit()
                        action_message = f"Pizza '{pizzaName}' successfully removed."
                    else:
                        action_message = f"Pizza '{pizzaName}' not found in the database."
                except sqlite3.Error as e:
                    action_message = f"Error removing pizza: {str(e)}"
            else:
                action_message = "Invalid input for pizza name."

    #refetch all pizzas for display
    cursor.execute("""
        SELECT pizzas.name, t1.name AS topping1, t2.name AS topping2, t3.name AS topping3
        FROM pizzas
        LEFT JOIN toppings t1 ON pizzas.topping1 = t1.name
        LEFT JOIN toppings t2 ON pizzas.topping2 = t2.name
        LEFT JOIN toppings t3 ON pizzas.topping3 = t3.name
    """)

    pizzas = cursor.fetchall()

    #return page
    return render_template("chefPage.html", pizzas=pizzas, toppings=toppings, action_message=action_message)


if __name__ == "__main__":
    #app.debug = True
    app.run(host="0.0.0.0", port=8080)

