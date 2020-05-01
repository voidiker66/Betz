import os
import uuid
import pusher
import json

from flask import Flask,jsonify,request,render_template,Response,flash,redirect,url_for
from Deck import Deck

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

pusher_client = pusher.Pusher(
  app_id='993501',
  key='9e4e46968280f45cecfe',
  secret='37a0b0032cd15b74fa77',
  cluster='us2',
  ssl=True
)

deck = Deck()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blackjack/action/<sessionID>', methods=['POST'])
def blackjackAction(sessionID):
    try:
        data = json.loads(request.json)
        if data['action'] == 'hit':
            return jsonify({'status' : 'success'})
        elif data['action'] == 'stay':
            return jsonify({'status' : 'success'})
        # pusher_client.trigger(session, 'card-played', {'action': _action})
    except:
        return jsonify({'status':'failed'})

@app.route('/blackjack')
def blackjack():
    session = request.args.get('sessionID')
    if session == None:
        session = str(uuid.uuid1())
        return redirect('/blackjack?sessionID='+session)
    return render_template('blackjack.html', sessionID=session)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    #app.run(host='0.0.0.0', port=80)