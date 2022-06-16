from flask import Flask, render_template, request
import pyodbc
import textwrap
from azure.storage.blob import BlobServiceClient, ContentSettings
server = 'kiran98.database.windows.net'
database = 'Assignment12'
username = 'kiran1998'
password = 'Omsrn@062466'
driver = '{ODBC Driver 17 for SQL Server}'

app = Flask(__name__)

sqlconnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server +
                               ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = sqlconnection.cursor()


connection_string = "DefaultEndpointsProtocol=https;AccountName=assigns1;AccountKey=FjfZ2UGw8oZx9cDaz2PJYqCtqMlyAXVuGt5Dq8TTcN1InDs8yUrgc8PIu48Xq8A7zku1SP0G+1hN+AStHhKtsQ==;EndpointSuffix=core.windows.net"
img_container = "uniqcontain"


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('index.html')


@app.route('/lat', methods=["POST", "GET"])
def lat():
    lat = str(request.form.get("lat"))
    degrees = str(request.form.get("long"))
    deviation_away = float(lat) - float(degrees)
    deviation_towards = float(lat) + float(degrees)
    ds = "SELECT time,latitude,longitude,id,place FROM [dbo].[eq] WHERE longitude > {} and longitude < {}".format(
        deviation_away, deviation_towards)
    cursor.execute(ds)
    ftch = cursor.fetchall()
    print(ftch)
    return render_template('lat.html', dsp=ftch)


@app.route('/val', methods=["POST", "GET"])
def long():
    N = str(request.form.get("N"))
    longitude_ranges = str(request.form.get("longss1"))
    longitude_rangel = str(request.form.get("longss2"))
    ds = "SELECT TOP {} * FROM [dbo].[q2eq] WHERE longitude BETWEEN {} AND {} ORDER BY mag DESC".format(
        N, longitude_ranges, longitude_rangel)
    ds1 = "SELECT TOP {} * FROM [dbo].[q2eq] WHERE longitude BETWEEN {} AND {} ORDER BY mag".format(
        N, longitude_ranges, longitude_rangel)
    cursor.execute(ds)
    ftch = cursor.fetchall()
    cursor.execute(ds1)
    ftch1 = cursor.fetchall()
    print(ftch)
    return render_template('long.html', dsp=ftch, dsp1=ftch1)


@app.route('/net', methods=["POST", "GET"])
def net():
    frmtime = str(request.form.get("t1"))
    totime = str(request.form.get("t2"))
    ds = "select TOP 5 * from [dbo].[q2eq] where time>='2022-06-16' and time_gmt > '{}:00' and time_gmt < '{}:00' ORDER BY mag DESC".format(
        frmtime, totime)
    ds1 = "select TOP 5 * from [dbo].[q2eq] where time>='2022-06-16' and time_gmt > '{}:00' and time_gmt < '{}:00' ORDER BY mag".format(
        frmtime, totime)
    cursor.execute(ds)
    ftch = cursor.fetchall()
    cursor.execute(ds1)
    ftch1 = cursor.fetchall()
    return render_template('tim.html', dsp=ftch, dsp1=ftch1)


if __name__ == '__main__':  # only run if you run this file, not if you import other main.py file
    #os.environ['PYTHONPATH'] = os.getcwd()
    app.run(debug=True)
