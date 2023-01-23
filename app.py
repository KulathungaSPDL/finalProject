from flask import Flask, render_template, Response, request
from cameraController import Video
from curl import CurlE
from sq import SqE
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb

app = Flask(__name__)

mydatabase = mysql.connector.connect(
    host = 'localhost', user = 'root',
    passwd = '', database = 'project')

mycursor = mydatabase.cursor()


# @app.route('/form')
# def form():
#     return render_template('form.html')
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'GET':
#         return "Login via the login Form"
#
#     if request.method == 'POST':
#         count = request.form['count']
#         cursor = mysql.connection.cursor()
#         # cursor.execute(''' INSERT INTO pushups VALUES(%s)''', (count))
#         cursor.execute("INSERT INTO 'pushups'('count') VALUES (%s)",(count))
#         mysql.connection.commit()
#         cursor.close()
#         return f"Done!!"


#home page
@app.route('/')
def Home():
    return render_template('home.html')

#index page
@app.route('/mainexpage')
def Mainexpage():
    return render_template('mainexpage.html')

# -----------------push ups start------------------
#index page
@app.route('/index')
def index():
    mycursor.execute('SELECT * FROM pushups WHERE id in (SELECT id FROM pushups WHERE date = (SELECT MAX(date) FROM pushups)) ORDER BY id DESC LIMIT 5')
    data = mycursor.fetchall()
    return render_template('index.html', output_data = data)

def gen(camera):
    while True:
        frame=camera.get_frame
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# -----------------push ups end------------------

# -----------------curl start------------------

#curl page
@app.route('/curl')
def Curl():
    mycursor.execute('SELECT * FROM curl WHERE id in (SELECT id FROM curl WHERE date = (SELECT MAX(date) FROM curl)) ORDER BY id DESC LIMIT 5')
    data = mycursor.fetchall()
    return render_template('curl.html', output_data = data)

def gen1(camera):
    while True:
        frame=camera.get_curl
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video1')
def video1():
    return Response(gen1(CurlE()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# -----------------curl end------------------
# -----------------sq start------------------

#sq page
@app.route('/sq')
def Sq():
    mycursor.execute('SELECT * FROM sq ORDER BY id DESC LIMIT 5')
    data = mycursor.fetchall()
    return render_template('sq.html', output_data = data)

def gen2(camera):
    while True:
        frame=camera.get_curl
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video2')
def video2():
    return Response(gen2(SqE()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# -----------------sq end------------------
#guide page
@app.route('/userguide')
def UserGuide():
    return render_template('userguide.html')

#push ups guide page
@app.route('/puguide')
def PushUpsGuide():
    return render_template('pushupsguide.html')

#curl guide page
@app.route('/curlguide')
def CurlGuide():
    return render_template('curlguide.html')

#sq guide page
@app.route('/sqguide')
def SqGuide():
    return render_template('sqguide.html')

#sq guide page
@app.route('/pradic')
def Pradic():
    mycursor.execute('SELECT * from pushups where id ="1"')
    data = mycursor.fetchall()
    if data==[]:
        mycursor.execute("SELECT * FROM pushups_p WHERE Day = 1")
        data = mycursor.fetchall()
        # print("empty")
    else:
        # print("not empty!")
        mycursor.execute("SELECT sum(count) FROM pushups WHERE id in (SELECT id FROM pushups WHERE date = (SELECT MAX(date) FROM pushups)) ORDER BY id DESC")
        data1 = mycursor.fetchall()
        output = []
        for row in data1:
            output.append(str(row[0]))
        # print(output[0])
        out = int(output[0])
        # print(output)
        # print(data)
        if (out<13):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 1")
            data = mycursor.fetchall()
        elif (out<17):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 2")
            data = mycursor.fetchall()
        elif (out<23):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 3")
            data = mycursor.fetchall()
        elif (out<=26):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 4")
            data = mycursor.fetchall()
        elif (out<34):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 5")
            data = mycursor.fetchall()
        elif (out<43):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 6")
            data = mycursor.fetchall()
        elif (out<46):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 7")
            data = mycursor.fetchall()
        elif (out<51):
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 8")
            data = mycursor.fetchall()
        else:
            mycursor.execute("SELECT * FROM pushups_p WHERE Day = 9")
            data = mycursor.fetchall()

    # mycursor.execute('SELECT * from sq where id ="1"')
    # data2 = mycursor.fetchall()
    # if data2==[]:
    #     mycursor.execute("SELECT * FROM sq_p WHERE Day = 1")
    #     data = mycursor.fetchall()
    #     # print("empty")
    # else:
    #     mycursor.execute(
    #         "SELECT sum(count) FROM sq WHERE id in (SELECT id FROM sq WHERE date = (SELECT MAX(date) FROM sq)) ORDER BY id DESC")
    #     data2 = mycursor.fetchall()
    #     output1 = []
    #     for row in data1:
    #         output1.append(str(row[0]))
    #     # print(output[0])
    #     out1 = int(output1[0])
    #     if (out1<13):
    #         mycursor.execute("SELECT * FROM pushups_p WHERE Day = 1")
    #         data = mycursor.fetchall()
    #     elif (out1<17):
    #         mycursor.execute("SELECT * FROM pushups_p WHERE Day = 2")
    #         data = mycursor.fetchall()



    return render_template('pradic.html', output_data=data)
app.run(debug=True)