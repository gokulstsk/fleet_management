from app import *


@app.route('/fuel_entry', methods=['GET', 'POST'])
def fuel_entry():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        vehicle = request.form['vehicle']
        litre = request.form['Liters']
        cost = request.form['cost']
        litre_cost = request.form['Cpl']
        print(vehicle, litre, cost, litre_cost)
        cursor.execute("insert into fuel_entry(vehicle,liters,fuel_cost,cost_per_liter) values (%s,%s,%s,%s)",
                       [vehicle, litre, cost, litre_cost])
        mysql.connection.commit()
        print("next")
    return render_template('user/fuel-entry.html')
