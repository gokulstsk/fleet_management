from app import *


@app.route('/issue_entry', methods=['GET', 'POST'])
def issue_entry():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print("hi")
    if request.method == "POST":
        vehicle = request.form['vehicle']
        place = request.form['place']
        issue = request.form['Issue']
        print(vehicle, place, issue)
        cursor.execute("insert into issue_entry(vehicle,place,issue) values (%s,%s,%s)",
                       [vehicle, place, issue])
        mysql.connection.commit()
        print("next")
    return render_template('user/issue-entry.html')
