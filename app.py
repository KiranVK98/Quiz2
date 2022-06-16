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
    ds = "SELECT time,latitude FROM [dbo].[eq] WHERE latitude > {} and latitude < {}".format(
        deviation_away, deviation_towards)
    cursor.execute(ds)
    ftch = cursor.fetchall()
    print(ftch)
    return render_template('lat.html', dsp=ftch)


if __name__ == '__main__':  # only run if you run this file, not if you import other main.py file
    #os.environ['PYTHONPATH'] = os.getcwd()
    app.run(debug=True)
