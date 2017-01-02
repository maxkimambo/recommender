import json
from flask import Flask, url_for, jsonify
from config_loader import ConfigLoader

cfg = ConfigLoader()
config = cfg.get_config()
host = config.get('server').get('host')
port = config.get('server').get('port')

app = Flask(__name__)


@app.route('/')
def api_root():

    data = [
        {
            'id': 1,
            'title': 'Buy groceries',
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        },
        {
            'id': 2,
            'title': u'Learn Python',
            'description': u'Need to find a good Python tutorial on the web',
            'done': False
        }
    ]
    return jsonify({'data': data})


@app.route('/recommender')
def api_recommender():

    return "recommendations"

if __name__ == '__main__':
    app.run(host=host, port=port)
