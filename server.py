import json
from flask import Flask, url_for, jsonify
from config_loader import ConfigLoader

from UserRecommender import UserRecommender

rec = UserRecommender()


cfg = ConfigLoader()
config = cfg.get_config()
host = config.get('server')
port = config.get('port')

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


@app.route('/recommender/<user_id>')
def api_recommender(user_id):

    result = rec.get_top_n_combined_recommendations(user_id, 30)

    return jsonify({'data': result})

@app.route('/recommender/ar/<user_id>')
def api_ar_recommender(user_id):

    ar = rec.get_topN_ar_recommendations(user_id, 30)

    return jsonify({'data': ar})

@app.route('/recommender/cb/<user_id>')
def api_cb_recommender(user_id):

    cb = rec.get_topN_cb_recommendations(user_id, 30)

    return jsonify({'data': cb})
if __name__ == '__main__':
    app.run(host=host, port=port)
