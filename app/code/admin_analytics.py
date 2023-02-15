#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from re import sub

from MySQLdb.cursors import Cursor
from app import *


@app.route("/admin_analytics/home", methods=["POST", "GET"])
def admin_analytics_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        home = arr.array('i', [0, 0, 0, 0])

        admin_name = session.get('name')
        print(admin_name)
        cursor.execute('SELECT * FROM course_session_details')
        home[0] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM student_details')
        home[1] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM course_details')
        home[2] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM faculty_details')
        home[3] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/index.html', admin_name=admin_name, count=home, subject=subject,
                               course=course)
    else:
        return redirect(url_for('login'))


########################################### subject table ##########################################

@app.route("/admin_analytics/subject", methods=["POST", "GET"])
def admin_analytics_subject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')

        cursor.execute('SELECT * FROM course_dept inner join department on course_dept.dept_id=department.dept_id')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()

        return render_template('admin_analytics/subject.html', subject=subject, admin_name=admin_name, course=course)
    else:
        return redirect(url_for('login'))


####################################### subject table end ############################################



@app.route('/admin/course/select', methods=['GET', 'POST'])
def admin_entry_course_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        print('hi1')
        course_id = request.form['course_id']
        cur.execute(
            "SELECT * FROM course_details,subject WHERE course_details.subject_id=subject.subject_id and course_id = %s",
            [course_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                'course_id': rs['course_id'],
                'subject_name': rs['subject_name'],
                'course_name': rs['course_name'],
                'course_grade': rs['course_grade'],
                'course_duration': rs['course_duration'],
                'no_of_session': rs['no_of_session'],

                'course_approval_status': rs['course_approval_status'],
                'course_description': rs['course_description']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


@app.route("/admin/course/change", methods=["POST", "GET"])
def admin_entry_course_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        index = request.args.get('a')
        print('option1'+index)
        course_code = request.form['cid'+index]
        course_id = request.form['id'+index]
        lesson_id = request.form['l'+index]
        subject_id=str(lesson_id[1])
        lesson_id=str(lesson_id[0])
        remarks = ''
        try:
            check1 = int(request.form['option1' + index])
        except:
            check1 = 0
        try:
            check2 = int(request.form['option2' + index])
        except:
            check2 = 0
        try:
            check3 = int(request.form['option3' + index])
        except:
            check3 = 0
        try:
            check4 = int(request.form['option4' + index])
        except:
            check4 = 0
        try:
            check5 = int(request.form['option5' + index])
        except:
            check5 = 0
        addRemarks = request.form['ta'+index]
        nfrs=0
        if check1 + check2 + check3 + check4 + check5 < 50 :
            status="rejected"
            remarks += " Rejected entries : "
            remarks += 'Unit-' + subject_id + " --> "
            if check1 == 0:
                nfrs+=10
                remarks += "LectureMaterial-"+lesson_id+" | "
            if check2 == 0:
                nfrs+=10
                remarks += "LessonPlan-"+lesson_id+" | "
            if check3 == 0:
                nfrs+=10
                remarks += "LectureVideo-"+lesson_id+" | "
            if check4 == 0:
                nfrs+=10
                remarks += "DiscourseLink-"+lesson_id+" | "
            if check5 == 0:
                nfrs+=10
                remarks += "DiscussionQuestion-"+lesson_id+" | "
            remarks += addRemarks
        else:
            status="approved"
            remarks = "-"
        print(check1, check2, check3, check4, check5, remarks)
        cursor.execute(f'update course_details set course_status="{status}", course_enroll_status = "{remarks} ", nfrs = "{nfrs}" where course_id={course_id}')
        cursor.execute(f'update faculty_details set  nfrs = nfrs+ "{nfrs}" where faculty_id=4')
        mysql.connection.commit()
    return redirect(url_for('admin_analytics_one_course',a=course_code))
    # return jsonify("success")


#########################################  Course Table ###############################################

@app.route("/admin_analytics/course/update", methods=["POST", "GET"])
def admin_entry_course_update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        subject_id = request.args.get('course_id')
        cursor.execute('delete from course_details where course_id=%s;', [subject_id])
        mysql.connection.commit()
        flash("Deleted ♥️")
        return redirect(url_for('admin_analytics_course'))
    else:
        return redirect(url_for('login'))



@app.route("/admin_analytics/course/registered", methods=["POST", "GET"])
def admin_entry_course_registered():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        id = session.get('id')
        count = arr.array('i', [0, 0, 0])
        admin_name = session.get('name')
        subject_id = request.args.get('course_id')
        # if request.method == 'POST':
        #     adminid=session.get('id')
        #     subjectid = request.form['subjectid']
        #     cname = request.form['cname']
        #     grade = request.form['grade']
        #     cduration = request.form['duration']
        #     nosession = request.form['session']
        #     description = request.form['coursedes']
        #     try:
        #         cursor.execute("INSERT INTO course_details (subject_id, course_grade,course_name,course_description,course_duration,no_of_session,admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",[subjectid, grade,cname,description,cduration,nosession,adminid])
        #         mysql.connection.commit()
        #         return jsonify('success')
        #     except Exception as  Ex:
        #         return jsonify('error')

        if subject_id:
            cursor.execute(
                'SELECT * FROM course_enroll_details,student_details Where course_enroll_details.student_id=student_details.student_id and course_enroll_details.course_id=%s',
                [subject_id, ])
            course = cursor.fetchall()
            cursor.execute(
                'SELECT * FROM course_enroll_details,student_details Where course_enroll_details.student_id=student_details.student_id and course_enroll_details.course_id=%s',
                [subject_id, ])
            count[0] = len(cursor.fetchall())
            # cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s and course_details.course_status="open"',[subject_id,])
            # count[1] = len(cursor.fetchall())
            # cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id and subject.subject_id=%s and course_details.course_status="close"',[subject_id,])
            # count[2] = len(cursor.fetchall())


        else:
            cursor.execute(
                'SELECT * FROM course_enroll_details,student_details Where course_enroll_details.student_id=student_details.student_id')
            course = cursor.fetchall()
            cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
            count[0] = len(cursor.fetchall())

        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute(
            'SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',
            [id])
        notifi = cursor.fetchall()
        return render_template('admin_analytics/course_registered.html', course=course, subject=subject, count=count,
                               admin_name=admin_name, notifi=notifi, id=subject_id)
    else:
        return redirect(url_for('login'))


@app.route("/admin_analytics/course", methods=["POST", "GET"])
def admin_analytics_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')

        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()

        for i in range(len(course)):
            # course[i]['course_description'] = html.unescape(course[i]['course_description'])
            print(course[i]['course_description'], i)

        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()

        return render_template('admin_analytics/course.html', course=course, subject=subject, admin_name=admin_name)
    else:
        return redirect(url_for('login'))


@app.route("/admin_analytics/one_course", methods=["POST", "GET"])
def admin_analytics_one_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')
        subject_id=request.args.get('a')

        cursor.execute(f'SELECT * FROM course_details Where course_details.course_code="{subject_id}" and course_details.course_status="pending" ')
        course = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute(f'SELECT * FROM course_dept where course_code = "{subject_id}"')
        dept = cursor.fetchall()

        return render_template('admin_analytics/course.html', course=course, subject=subject, admin_name=admin_name,dept=dept)
    else:
        return redirect(url_for('login'))


@app.route("/admin_analytics/approval_course", methods=["POST", "GET"])
def admin_approval_course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        course_id = int(request.args.get('a'))
        status = request.args.get('b')
        print(course_id)
        print(status)
        print(type(course_id))

        cursor.execute('update course_details set course_approval_status=%s Where course_id=%s', (status, course_id))
        mysql.connection.commit()
        return redirect(url_for('admin_analytics_course'))


####################################### Course table end ############################################



######################################  Session And Attendance end ##################################

@app.route("/admin_analytics/analysis_attendance", methods=["POST", "GET"])
def admin_analytics_sess_attd():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')
        course_id = request.args.get('a')
        print(course_id)
        course_name = request.args.get('b')
        cursor.execute('SELECT  sd.student_name,sd.student_contact,sd.student_email,cd.course_name,cd.course_id,csd.session_name,sa.satt_present FROM student_details sd LEFT JOIN student_attendance sa ON sd.student_id = sa.student_id LEFT JOIN course_session_details csd ON csd.session_id = sa.session_id LEFT JOIN course_details cd ON cd.course_id=csd.course_id WHERE cd.course_id=%s',[course_id])
        course = cursor.fetchall()
        return render_template('admin_analytics/analysis_attendance.html', course=course)
    else:
        return redirect(url_for('login'))





#########################################  session Table ###############################################


@app.route("/admin_analytics/session", methods=["POST", "GET"])
def admin_analytics_session():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')
        course_id = request.args.get('a')
        print(course_id)
        course_name = request.args.get('b')

        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()



        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        if course_id == None:
            cursor.execute(
                'SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=course_session_details.course_id')
            sess = cursor.fetchall()
        else:

            cursor.execute(
                'SELECT * FROM course_session_details,faculty_details,course_details WHERE course_session_details.faculty_id=faculty_details.faculty_id and course_details.course_id=%s and course_session_details.course_id=%s',
                (course_id, course_id))
            sess = cursor.fetchall()

        for i in range(len(sess)):
            # sess[i]['session_discription'] = html.unescape(sess[i]['session_discription'])
            print(sess[i]['session_discription'], i)

        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        return render_template('admin_analytics/course session table.html', session=sess, subject=subject,
                               course=course, faculty=faculty, admin_name=admin_name)
    else:
        return redirect(url_for('login'))

@app.route('/admin/session/select', methods=['GET', 'POST'])
def admin_entry_session_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print("hi")
    if request.method == 'POST':
        print('hi1')
        session_id = request.form['session_id']
        cur.execute(
            "SELECT * FROM course_details,course_session_details,faculty_details WHERE course_session_details.course_id=course_details.course_id and course_session_details.faculty_id=faculty_details.faculty_id and session_id = %s",
            [session_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                'session_id': rs['session_id'],
                'course_name': rs['course_name'],
                'session_name': rs['session_name'],
                'faculty_name': rs['faculty_name'],
                'session_status': rs['session_status'],
                'session_date':rs['session_date'],
                'session_starttime': rs['session_starttime'],
                'session_endtime': rs['session_endtime'],
                'session_discription': rs['session_discription']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)

@app.route("/admin/session/change", methods=["POST", "GET"])
def admin_entry_session_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        print('hi')
        session_id = request.form['session_id'],
        print(session_id)
        # course_name = request.form['course_name'],
        session_name = request.form['session_name']
        # faculty_name = request.form['faculty_name']
        session_status = request.form['session_status']
        #status = request.form['status']
        session_starttime = request.form['session_starttime']
        session_date = request.form['session_date']
        session_endtime = request.form['session_endtime']
        print(session_starttime)
        session_discription = request.form['test']
        cursor.execute('update course_session_details set session_date=%s,session_name = %s ,session_status=%s , session_starttime=%s ,session_endtime=%s ,session_discription=%s where session_id=%s',[ session_date,session_name, session_status, session_starttime,session_endtime, session_discription, session_id])
        mysql.connection.commit()
    return jsonify('success')
####################################### Session table end ############################################


#########################################  Faculty Table ###############################################


@app.route("/admin_analytics/faculty", methods=["POST", "GET"])
def admin_analytics_faculty():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')

        cursor.execute('SELECT * FROM faculty_details')
        faculty = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/Faculty table.html', faculty=faculty, subject=subject,
                               admin_name=admin_name, course=course)
    else:
        return redirect(url_for('login'))


####################################### Faculty table end ############################################


#########################################  Student Table ###############################################


@app.route("/admin_analytics/student", methods=["POST", "GET"])
def admin_analytics_student():
    if 'id' in session and session.get("user_type") == 'admin':
        admin_name = session.get('name')
        course_id = request.args.get('a')
        count = arr.array('i', [0, 0, 0, 0])
        print(course_id)
        school_id = request.args.get('school_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if school_id:
            cursor.execute(
                'SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s',
                [school_id, ])
            student = cursor.fetchall()
            cursor.execute(
                'SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s',
                [school_id, ])
            count[0] = len(cursor.fetchall())

            cursor.execute(
                'SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s and student_details.account_status="allow"',
                [school_id, ])
            count[1] = len(cursor.fetchall())
            cursor.execute(
                'SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s and student_details.account_status="block"',
                [school_id, ])
            count[2] = len(cursor.fetchall())
            cursor.execute(
                'SELECT * FROM student_details,school_details where school_details.school_id=student_details.school_id and student_details.school_id=%s and student_details.account_status="waiting"',
                [school_id, ])
            count[3] = len(cursor.fetchall())
            return render_template('admin_analytics/details_table.html', student=student, count=count,admin_name=admin_name)
        cursor.execute('SELECT * FROM student_details,school_details where  student_details.school_id =  school_details.school_id   order by student_name ASC')
        student = cursor.fetchall()
        cursor.execute('SELECT * FROM school_details')
        school = cursor.fetchall()
        cursor.execute('SELECT * FROM subject')
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM course_details,subject Where course_details.subject_id=subject.subject_id')
        course = cursor.fetchall()
        return render_template('admin_analytics/student details table.html', subject=subject, student=student,
                               admin_name=admin_name, course=course, school=school)
    else:
        return redirect(url_for('login'))




####################################### Student table end ############################################


@app.route('/admin_analytics/student/select', methods=['GET', 'POST'])
def admin_entry_student_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        student_id = request.form['student_id']
        print(student_id)
        cur.execute("SELECT * FROM student_details,school_details where student_details.school_id=school_details.school_id and student_id = %s", [student_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'student_id': rs['student_id'],
                    'student_name': rs['student_name'],
                    'student_contact': rs['student_contact'],
                    'school_name': rs['school_name'],
                    'school_board': rs['school_board'],
                    'school_pincode': rs['school_pincode'],
                    'student_email': rs['student_email'],
                    'student_grade': rs['student_grade'],
                    'student_whatsapp': rs['student_whatsapp'],
                    'student_profile': rs['student_profile'],
                    'account_status': rs['account_status'],
                   'student_idcard': rs['student_idcard'],
                    'url_path':app.static_url_path
                    }
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


@app.route("/admin_analytics/student/change", methods=["POST", "GET"])
def admin_entry_student_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        student_contact = request.form['student_contact']
        student_email = request.form['student_email']
        student_whatsapp = request.form['student_whatsapp']
        status = request.form['status']

        cursor.execute(
            'update student_details set student_name=%s, student_contact = %s ,student_email=%s , student_whatsapp=%s , account_status=%s where student_id=%s',
            [student_name, student_contact, student_email, student_whatsapp, status, student_id])
        mysql.connection.commit()
    return jsonify('success')


####################################### school table  ############################################
@app.route("/admin_analytics/school_details", methods=["POST", "GET"])
def admin_entry_school_details():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        count = arr.array('i', [0, 0, 0, 0])

        id = session.get('id')
        status = request.args.get('status')

        admin_name = session.get('name')
        if request.method == 'POST':
            adminid = session.get('id')
            school_name = request.form['school_name']
            school_state = request.form['school_state']
            school_district = request.form['school_district']
            school_pincode = request.form['school_pincode']
            school_board = request.form['school_board']
            school_contact = request.form['school_contact']

            try:
                cursor.execute(
                    "INSERT INTO school_details (school_name, school_state ,school_district,school_pincode,school_board,school_contact) VALUES (%s, %s, %s, %s, %s, %s)",
                    [school_name, school_state, school_district, school_pincode, school_board, school_contact])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')
        if (status):
            cursor.execute('SELECT * FROM school_details where school_status=%s', [status, ])
            school = cursor.fetchall()

        else:
            cursor.execute('SELECT * FROM school_details')
            school = cursor.fetchall()
        cursor.execute('SELECT * FROM school_details')
        count[0] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM school_details where school_status="approved"')
        count[1] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM school_details where school_status="decline"')
        count[2] = len(cursor.fetchall())
        cursor.execute('SELECT * FROM school_details where school_status="notapproved"')
        count[3] = len(cursor.fetchall())
        print(count[2])
        # cursor.execute('SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',[id])
        # notifi = cursor.fetchall()
        return render_template('admin_analytics/school_details.html', school=school, count=count, admin_name=admin_name)
    else:
        return redirect(url_for('login'))


@app.route('/admin_analytics/school_details/select', methods=['GET', 'POST'])
def admin_entry_school_details_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        school_id = request.form['school_id']
        print(school_id)
        cur.execute("SELECT * FROM school_details where school_id = %s", [school_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'school_id': rs['school_id'],
                    'school_name': rs['school_name'],
                    'school_state': rs['school_state'],
                    'school_district': rs['school_district'],
                    'school_pincode': rs['school_pincode'],
                    'school_board': rs['school_board'],
                    'school_contact': rs['school_contact'],
                    'school_status': rs['school_status']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


@app.route("/admin_analytics/school_details/change", methods=["POST", "GET"])
def admin_entry_school_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        school_id = request.form['school_id']
        print("faculty_id"+ school_id)
        school_name = request.form['school_name']
        school_state = request.form['school_state']
        school_district = request.form['school_district']
        school_pincode = request.form['school_pincode']
        school_contact = request.form['school_contact']
        school_status = request.form['school_status']

        cursor.execute('update school_details set school_name=%s, school_state = %s ,school_district=%s,school_pincode=%s,school_contact=%s,school_status=%s where school_id=%s', [school_name,school_state,school_district,school_pincode,school_contact,school_status,school_id])
        mysql.connection.commit()
    return jsonify('success')

####################################### school table end ############################################


#########################################  attendance details ###############################################
@app.route("/admin_analytics/attendance", methods=["POST", "GET"])
def attendance():
    if 'id' in session and session.get("user_type") == 'admin':
        session_id = request.args.get('b')
        admin_name = session.get('name')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT sd.student_name,sd.student_grade,sd.student_contact,sa.satt_present,ssf.stu_session_willingness,ssf.stu_session_feedback,ssf.stu_session_timestamp FROM student_attendance sa LEFT JOIN student_details sd ON sd.student_id = sa.student_id LEFT JOIN student_session_feedback ssf ON ssf.student_id = sa.student_id AND ssf.satt_id = sa.satt_id WHERE sa.session_id =%s ',
            [session_id])
        attendance = cursor.fetchall()
        cursor.execute("SELECT  sd.session_name from course_session_details sd  where  session_id=%s",[session_id])
        course = cursor.fetchall()
        print(attendance)
        cursor.execute("SELECT count(satt_present) as present from student_attendance  where satt_present='YES' and  session_id=%s",[session_id])
        present = cursor.fetchone()

        cursor.execute(
            "SELECT count(satt_present) as absent from student_attendance  where satt_present='NO' and  session_id=%s",
            [session_id])
        absent = cursor.fetchone()

        return render_template('admin_analytics/attendance.html', attendance=attendance, admin_name=admin_name,
                               course = course ,present=present, absent=absent)
    else:
        return redirect(url_for('login'))


#########################################  attendance details end ###############################################


#########################################  User Table ###############################################


@app.route("/admin_analytics/adminuser", methods=["POST", "GET"])
def admin_analytics_user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        id = session.get('id')
        admin_name = session.get('name')
        if request.method == 'POST':
            adminid = session.get('id')
            name = request.form['name']
            username = request.form['username']
            passwd = request.form['passwd']
            password = hashlib.md5(passwd.encode())
            password.hexdigest()
            user_type = request.form['user_type']

            try:
                cursor.execute(
                    "INSERT INTO admin (admin_name, admin_username ,admin_password,admin_usertype) VALUES (%s, %s, %s,%s)",
                    [name, username,password.hexdigest(), user_type])
                mysql.connection.commit()
                return jsonify('success')
            except Exception as Ex:
                return jsonify('error')
        cursor.execute('SELECT * FROM admin')
        user = cursor.fetchall()
        cursor.execute(
            'SELECT * FROM notification,admin where notification_from=admin.admin_id and notification.admin_id=%s and notification_status="unread" LIMIT 4',
            [id])
        notifi = cursor.fetchall()
        return render_template('admin_analytics/admin_user.html', user=user, admin_name=admin_name, notifi=notifi)
    else:
        return redirect(url_for('login'))


@app.route("/admin_analytics/adminuser/update", methods=["POST", "GET"])
def admin_analytics_user_update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if 'id' in session and session.get("user_type") == 'admin':
        if request.method == "POST":
            if request.form.get("delete"):
                result = request.form
                id = result["delete"]
                cursor.execute('delete from admin where admin_id=%s;', [id])
                mysql.connection.commit()
                flash("Deleted ♥️")
                return redirect(url_for('admin_analytics_user'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_analytics/adminuser/select', methods=['GET', 'POST'])
def admin_analytics_user_select():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        print(admin_id)
        cur.execute("SELECT * FROM admin where admin_id = %s", [admin_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                'admin_id': rs['admin_id'],
                'admin_name': rs['admin_name'],
                'admin_username': rs['admin_username'],
                'admin_password': rs['admin_password'],
                'admin_status': rs['admin_status'],
                'admin_usertype': rs['admin_usertype']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)


@app.route("/admin_analytics/adminuser/change", methods=["POST", "GET"])
def admin_analytics_user_change():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        admin_id = request.form['admin_id']
        admin_name = request.form['admin_name']
        admin_username = request.form['admin_username']

        admin_password = request.form['admin_password']
        password = hashlib.md5(admin_password.encode())
        pwd=password.hexdigest()
        admin_status = request.form['status']
        admin_usertype = request.form['user_type']

        cursor.execute(
            'update admin set admin_name=%s, admin_username = %s ,admin_password=%s ,admin_status=%s , admin_usertype = %s where admin_id=%s',
            [admin_name, admin_username, pwd, admin_status, admin_usertype, admin_id])
        mysql.connection.commit()
    return jsonify('success')

####################################### User table end ############################################
