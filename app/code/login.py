from app import *

@app.route("/admin/login", methods=["POST", "GET"])
def login():
    ip_address = flask.request.remote_addr
    print(ip_address)
    if request.method == 'POST' and 'admin' in request.form and 'pwd' in request.form:
        user = request.form['admin']
        passwd = request.form['pwd']
        print(user,passwd)
        password = hashlib.md5(passwd.encode())
        pwd=password.hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login WHERE admin_username = '%s' AND admin_password= '%s'"%(user,passwd))
        user = cursor.fetchone()
        print(user)
        if user:
            if user['admin_usertype']=='data_entry':

                session['user_type'] = 'data_entry'
                session['id'] = user['admin_id']
                session['name'] = user['admin_name']

                #return redirect(url_for('data_entry_home'))
                return jsonify({'success' : 'data_entry'})

            elif user['admin_usertype']=='admin':
                print('admin')
                session['user_type'] = 'admin'
                session['id'] = user['admin_id']
                session['name'] = user['admin_name']
                return jsonify({'success' : 'admin'})
        else:
            return jsonify({'success': 'error'})


    if(not session.get("id") is None):
        if(session.get("user_type") == 'data_entry'):
            return redirect(url_for('dashboard'))
        elif(session.get("user_type") == 'admin'):
            return redirect(url_for('admin_analytics_home'))


    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




@app.errorhandler(404)
def page_not_found(e):

    app.logger.info("Page not found: {request.url}")

    return redirect(url_for('student_home'))


@app.errorhandler(403)
def page_not_founds(e):

    app.logger.info("Page not found: {request.url}")

    return redirect(url_for('student_home'))
