from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.instantmemo


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/message', methods=["POST"])
def set_message():
    username_receive = request.form['username_give']
    contents_receive = request.form['contents_give']

    doc = {
        'username': username_receive,
        'contents': contents_receive,
        'created_at': datetime.now()
    }

    db.messages.insert_one(doc)

    return jsonify({'result': 'success', 'msg': 'Successfully posted!'})


@app.route('/message', methods=["GET"])
def get_messages():
    date_now = datetime.now()
    date_before = date_now - timedelta(days=1)
    messages = list(db.messages.find({'created_at': {'$gte': date_before, '$lte': date_now}}, {'_id': False}).sort('created_at', -1))
    return jsonify({'result': 'success', 'messages': messages})


@app.route('/message/edit', methods=["POST"])
def edit_message():
    username_receive = request.form['username_give']
    contents_receive = request.form['contents_give']

    db.messages.update_one({'username': username_receive}, {
                           '$set': {'contents': contents_receive, 'created_at': datetime.now()}})
    return jsonify({'result': 'success', 'msg': 'Successfully edited memo!'})


@app.route('/message/delete', methods=['POST'])
def delete_message():
    username_receive = request.form['username_give']
    db.messages.delete_one({'username': username_receive})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)