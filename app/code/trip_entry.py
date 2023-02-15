from app import *


@app.route('/trip_entry', methods=['GET', 'POST'])
def trip_entry():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        vehicle = request.form['trip']
        start_time = request.form['start-time']
        end_time = request.form['end-time']
        start_odometer = request.form['start-odometer']
        end_odometer = request.form['end-odometer']
        print(vehicle,start_time,end_time,start_odometer,end_odometer)
        cursor.execute("insert into trip_entry(vehicle,start_time,end_time,start_odometer,end_odometer) values (%s,"
                       "%s,%s,%s,%s)",[vehicle, start_time, end_time,start_odometer,end_odometer])
        mysql.connection.commit()
        print("hie")
    return render_template('user/trip-entry.html')
