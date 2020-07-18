var channel = pusher.subscribe(sessionID);
var membersChannel = pusher.subscribe('presence-'+sessionID);
var cardsDict = {};
var deck = {};
var deckPointer = 0;
var playerOrder;
var playerPointer;

function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

channel.bind('new-deck', (data) => {
	deck[sessionID] = data;
	playerOrder = Object.keys(membersChannel.members.members);
	shuffle(playerOrder);
	playerPointer = 0;
});
channel.bind('player-hit', (data) => {
	let player = data['player']['id'];
	cardsDict[player] = deck[sessionID][deckPointer];
	deckPointer++;
});
channel.bind('player-stay', (data) => {
	if (playerPointer == (playerOrder.length - 1)) {
		playerPointer = 0;
	} else {
		playerPointer++;
	}
	// Here is where we would do the visual changes IF WE HAD ANY
});

$(() => {
	// animation for when a card is dealt to a player
	function dealCard(playerID) {
		let newcard = document.createElement('img');
		newcard.className += ' card card-deal';
		newcard.src = cardDisplayImage;
		// We need to change the translate parameter based on how many players are playing and where the player is shown
		document.getElementById('game-display').appendChild(newcard);
		setTimeout(() => {
			newcard.style.transform = 'translate(2em)';
		}, 200);
	}

	$('#hit-btn').on('click', () => {
		let url = '/blackjack/action/' + sessionID;
		let dataType = 'json';
		let data = JSON.stringify({'action':'hit', 'player':membersChannel.members.me});
		$.ajax({
	        type: "POST", 
	        url: url, //localhost Flask
	        data : JSON.stringify(data),
	        contentType: "application/json",
	    });
	    dealCard(membersChannel.members.me);
	})
	$('#stay-btn').on('click', () => {
		let url = '/blackjack/action/' + sessionID;
		let dataType = 'json';
		let data = JSON.stringify({'action':'stay'});
		$.ajax({
	        type: "POST", 
	        url: url, //localhost Flask
	        data : JSON.stringify(data),
	        contentType: "application/json",
	    });
	})
	$('#new-deck-btn').on('click', () => {
		let url = '/blackjack/action/' + sessionID;
		let dataType = 'json';
		let data = JSON.stringify({'action':'new_game'});
		$.ajax({
	        type: "POST", 
	        url: url, //localhost Flask
	        data : JSON.stringify(data),
	        contentType: "application/json",
	    });
	    document.getElementById('game-display').innerHTML = '';
	})
})