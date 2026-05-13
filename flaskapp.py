# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

cart = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        genre = request.form['genre']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name:", f_name + " "+ l_name, ":", "Favorite Genre:", genre)
        
        flash('User added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to delete:", name)
        
        flash('User deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/view-cart')
def view_cart():
    full_cart = []

    for item_name in cart:
        query = "SELECT * FROM Inventory WHERE description = %s"
        result = execute_query(query, (item_name,))

        if result:
            full_cart.append(result[0])   # add the full row dict

    return render_template('view_cart.html', items=full_cart)



@app.route('/store-items', methods=['GET', 'POST'])
def store_items():
    if request.method == 'POST':
        item_name = request.form['item_name']
        #Check if in database
        query = "SELECT * FROM Inventory WHERE description = %s"
        result = execute_query(query, (item_name,))
        if result:
            # Item exists, so add to cart
            cart.append(item_name)  # add the row dictionary
            flash(f'Added "{item_name}" to cart!', 'success')
        else:
            # Item does not exist, so notify user
            flash(f'Item "{item_name}" is not sold here', 'danger')

        return redirect(url_for('store_items'))
    else:
        query = "SELECT * FROM Inventory LIMIT 50"
        items_list = execute_query(query)
        return render_template('store_items.html', items=items_list)



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
