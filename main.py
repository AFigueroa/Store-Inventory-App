import os
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import send_from_directory
import hashlib
import mysql.connector
from werkzeug import secure_filename

from flask import jsonify
import json
import urllib

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

app.secret_key = "blindporcupine"

# Verify an uploaded files name
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


'''
    Initial route...
'''
@app.route("/")
def index():

    if not session.has_key("logged"):
        session['logged'] = "false"

    # Display All Items
    db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="itemsdb")
    cvar = db.cursor()
    data = 'empty'
    try:
        cvar.execute("SELECT itemId, itemName, itemDescription, itemWidth, itemLength, itemHeight, itemWeight FROM items WHERE active = 1")
        data = cvar.fetchall()
    except mysql.connector.Error:
        data = "Something went wrong: {}".format(err)
        return render_template('serverError.html', pagedata=data)

    return render_template('showItems.html', pagedata=data)

'''
    Show Details view
'''
@app.route("/item/<itemId>")
def item(itemId):

    # Display Item where name is itemName
    db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="itemsdb")
    cvar = db.cursor()

    try:
        cvar.execute('SELECT itemId from items where itemId = %s', (itemId, ))
        data = cvar.fetchall()
    except mysql.connector.Error as err:
        data = "Something went wrong: {}".format(err)
        return render_template('serverError.html', pagedata=data)
    if data:
        itemId = int(data[0][0])
    else:
        data = 'Error-404: No items where found with that name.'
        return render_template('serverError.html', pagedata=data)
    try:
        cvar.execute("SELECT itemId, itemName, itemDescription, itemWidth, itemLength, itemHeight, itemWeight FROM items WHERE active = 1 and itemId = %s", (itemId, ))
        data = cvar.fetchall()
    except mysql.connector.Error as err:
        data = "Something went wrong: {}".format(err)
        return render_template('serverError.html', pagedata=data)

    try:
        cvar.execute("SELECT pictureUrl FROM pictures WHERE itemId = %s", (itemId, ))
        urls = cvar.fetchall()
    except mysql.connector.Error as err:
        data = "Something went wrong: {}".format(err)
        return render_template('serverError.html', pagedata=data)

    imgNames = []
    for imgUrl in urls:
        imgNames.append(imgUrl[0])

    allData = [data, imgNames]

    return render_template('itemDetails.html', pagedata=allData)


'''
    Add Item Form route
'''
@app.route("/addform")
def addform():
    if session['logged'] != "true":
        return redirect("/loginform")
    else:
        return render_template('addform.html')

'''
    Add Item Action route
'''
@app.route("/addaction", methods=["POST"])
def addaction():
    if session['logged'] == 'true':
        if request.form:
            userId = session['userId']
            name = request.form['name']
            session['itemName'] = name
            description = request.form['description']
            width = request.form['width']
            length = request.form['length']
            height = request.form['height']
            weight = request.form['weight']

            checkStr = str(userId)+name+description+str(width)+str(length)+str(height)+str(weight)

            if "'" in checkStr or '"' in checkStr or ',' in checkStr:
                data = 'Invalid characters inside form fields.'
                return render_template('addform.html', pagedata=data)
            else:
                try:
                    db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="itemsdb")
                    cvar = db.cursor()
                    sql = '''
                    INSERT INTO items(userid, itemName, itemDescription, itemWidth, itemLength, itemHeight, itemWeight)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                    '''
                    cvar.execute(sql, (userId, name, description, width, length, height, weight))
                    db.commit()
                except mysql.connector.Error:
                    data = "An error occurred while adding item. Make sure the item's name is unique"
                    return render_template('addform.html', pagedata=data)

                # Request the files
                uploaded_files = request.files.getlist("images[]")

                #Initiate an empty array
                filenames = []
                try:
                    sql ='SELECT itemId from items where itemName = %s'
                    cvar.execute(sql, (name, ))
                    data = cvar.fetchall()
                except mysql.connector.Error:
                    data = 'Broken link in item name.'
                    return render_template('serverError.html', pagedata=data)

                if data[0]:
                    itemId = int(data[0][0])
                else:
                    data = 'No item with such name found.'
                    return render_template('serverError.html', pagedata=data)

                for file in uploaded_files:

                    # Check if the file is one of the allowed types/extensions
                    if file and allowed_file(file.filename):

                        # Make the filename safe, remove unsupported chars
                        filename = secure_filename(file.filename)

                        # Prepare file name with uploads folder url
                        url = 'uploads/'+filename

                        sql = '''
                        INSERT INTO pictures(itemId, pictureUrl)
                        VALUES(%s, %s)
                        '''
                        try:
                            cvar.execute(sql, (itemId, url))
                            db.commit()
                        except mysql.connector.Error:
                            data = "Added item successfully but failed to upload it's images. Please add them through the details page."
                            return render_template('addSuccess.html', pagedata=data)
                        # Move the file form the temporal folder to the upload

                        # folder we setup
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                        # Save the filename into a list, we'll use it later
                        filenames.append(filename)
                        data = 'The item and its pictures where succesfully uploaded.'
                        return render_template('addSuccess.html', pagedata=data)
                    else:
                        data = 'One or more files submitted was in an un-allowed format extension.'
                        return render_template('addform.html', pagedata=data)
                # Load an html page with a link to each uploaded file

                # Add the item successfully


    else:
        return redirect("/loginform")

'''
    Show one Uploaded
'''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

'''
    Update Item Form route
'''
@app.route("/updateform/<itemId>")
def updateform(itemId):
    if session['logged'] != "true":
        return redirect("/loginform")
    else:

        db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="itemsdb")
        cvar = db.cursor()

        cvar.execute("SELECT * FROM items WHERE itemId = %s", (itemId, ))
        data = cvar.fetchall()

        return render_template('updateform.html', pagedata=data)


'''
    Update Action route
'''
@app.route("/updateaction", methods=["POST"])
def updateaction():
    if session['logged'] == "false":
        return redirect("/loginform")
    else:
        name = request.form['name']
        description = request.form['description']
        width = request.form['width']
        length = request.form['length']
        height = request.form['height']
        weight = request.form['weight']
        itemId = request.form['id']

        checkStr = str(itemId)+name+description+str(width)+str(length)+str(height)+str(weight)

        if "'" in checkStr or '"' in checkStr:
            msg = 'Invalid characters inside form fields.'
            data = [msg, itemId]
            return render_template('updateError.html', pagedata=data)
        else:
            db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="itemsdb")
            cvar = db.cursor()
            sql = '''
            UPDATE items
            set itemName = %s, itemDescription = %s, itemWidth = %s, itemLength = %s, itemHeight = %s, itemWeight = %s
            where itemId = %s
            '''
            try:
                cvar.execute(sql, (name, description, width, length, height, weight, itemId))
                db.commit()
                return redirect("/")
            except mysql.connector.Error:
                data = 'Critical error: Update function is broken. Please call the server administrator.'
                return render_template('updateError.html', pagedata=data)


'''
    Login Form route
'''
@app.route("/loginform")
def loginform():
    return render_template('loginform.html')

'''
    Login Action route
'''
@app.route("/loginaction", methods=["POST", "GET"])
def loginaction():
    username = request.form['username']
    password = request.form['password']

    checkStr = str(username)+str(password)

    if "'" in checkStr or '"' in checkStr:
        data = 'Invalid characters inside form fields.'
        return render_template('loginform.html', pagedata=data)
    else:
        db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="itemsdb")
        cvar = db.cursor()
        try:
            cvar.execute("SELECT userId, username from users WHERE username = %s and password = %s", (username, password))
            data = cvar.fetchall()
            if (cvar.rowcount > 0):
                session['logged'] = "true"
                session['userId'] = str(data[0][0])
                session['username'] = data[0][1]
                return redirect("/")
            else:
                session['logged'] = "false"
                data = 'Wrong username and password combination.'
                return render_template('loginform.html', pagedata=data)
        except mysql.connector.Error:
            data = 'Error: Login connection failed. Please try again. If error persists please contact your server administrator'
            return render_template('loginform.html', pagedata=data)


'''
    Logout Action route
'''
@app.route("/logoutaction")
def logoutaction():
    session['logged'] = 0
    return redirect('/')

'''
    Delete Action route
'''
@app.route("/deleteaction/<itemId>")
def deleteaction(itemId):
    if session['logged'] == "false":
        return redirect("/loginform")
    else:
        db = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="itemsdb")
        cvar = db.cursor()
        cvar.execute("UPDATE items set active = 0 where itemId = %s", (itemId, ))
        db.commit()
        return redirect("/")

'''
    ...End of Routing
'''
if __name__ == '__main__':
    app.run(debug=True)