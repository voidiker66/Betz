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

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
    # pusher_client is obtained through pusher.Pusher( ... )
    auth = pusher_client.authenticate(
        channel=request.form['channel_name'],
        socket_id=request.form['socket_id'],
        custom_data={'user_id':request.form['socket_id']} # temp because I have no idea how to create new users - this will create new user on each page refresh
    )
    return json.dumps(auth)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blackjack/action/<sessionID>', methods=['POST'])
def blackjackAction(sessionID):
    try:
        data = json.loads(request.json)
        if data['action'] == 'hit':
            pusher_client.trigger(sessionID, 'player-hit', {'player':data['player']})
            return jsonify({'status' : 'success'})
        elif data['action'] == 'stay':
            pusher_client.trigger(sessionID, 'player-stay')
            return jsonify({'status' : 'success'})
        elif data['action'] == 'new_game':
            deck = Deck()
            pusher_client.trigger(sessionID, 'new-deck', deck.get_shuffled_deck())
            return jsonify({'status' : 'success'})
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