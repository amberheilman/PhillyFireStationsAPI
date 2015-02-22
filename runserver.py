from flask import Flask
import json

app = Flask(__name__)

@app.route('/stations')
def stations():
    data = {'station without id': 'no id'}
    return json.dumps(data)


@app.route('/stations/<id>')
def station(id):
    data = {'station': 'station with id'}
    return json.dumps(data)

@app.route('/incidents')
def incidents():
    data = {'incidents': 'no id'}
    return json.dumps(data)

@app.route('/incidents/<id>')
def incident(id):
    data = {'incidents': 'with id'}
    return json.dumps(data)


if __name__ == '__main__':
    app.run(port=80, debug=True)
