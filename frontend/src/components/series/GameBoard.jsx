import React from 'react'
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import Hand from "./react-playing-cards/src/PlayingCard/Hand/Hand";
import Trick from './Trick'
import PreviousTrick from './PreviousTrick'
import GameScore from './GameScore'





class GameBoard extends React.Component {
    // lifecycle methods
    constructor(props) {
        super(props)
        this.state = {
            game_id: this.props.game_id,
            position: null,
            players: null,
            current_user: props.current_user,
            left_hand:  null,
            right_hand: null,
            top_hand: null,
            hand:  null,
            previous_trick:  null,
            game_completed:  false,
            end_game_popup:  false
        }

        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
//         this.isPlayerTurn = this.isPlayerTurn.bind(this)

    }

    closeGameOnClick(){
        console.log("YYYYY", this.state)
        this.setState({
            game_completed:  false,
            end_game_popup:  false
            })
        console.log("Sending message to close the game", this.state.game.series.id)
        this.sendSocketMessage({action: "create_game", series_id: this.state.game.series.id})
//         this.setState({
//             game_completed:  false,
//             end_game_popup:  false
//             })
     }

    onDoubleClick(card){
            var card_dict = this.convertStringToCard(card)

            this.sendSocketMessage({action: "play_card",
                 game_id: this.state.game_id, number:card_dict["number"], suit:card_dict["suit"], trick_id: this.state.game.current_trick.id})
    }

    doNothingonDoubleClick(keys){
//         console.log("Do Nothing")
    }


    componentDidMount() {
        this.getGame()
    }



    componentWillUnmount() {
        this.serverRequest.abort();
    }

    _getCardSize() {
        return 100
//         let cardSize = window.innerWidth / this.state.hand.length;
//         return this.state.layout !== "spread" || cardSize > 100 ? 100 : cardSize;
    }

    _getHandPositions() {
        return {
            top:{'transform' : 'translateY(-30%) rotate(180deg)', 'right': '50%', 'top': "5%", 'position': 'absolute'},
            bottom:{'bottom': '-5%', 'right': '50%', 'position': 'absolute', 'height' : '30%'},
            left:{'bottom': '40%','right': '90%', 'position': 'absolute', 'transform': 'rotate(90deg)' },
            right:{'bottom': '40%','left': '90%', 'position': 'absolute', 'transform': 'rotate(270deg)' }
            }
           }
    checkSeriesComplete(game){
        if (game.series){
            if (game.series.completed == true){
                window.location.href = '/lobby';
            }
        }
    }

    setStateWithGameResult(game){
        this.checkSeriesComplete(game)
        var ordered_players = this.orderPlayers(game.players)
        this.setState({
                game: game,
                game_id: game.id,
                current_player: ordered_players[0],
                players: ordered_players,
                hand: this.unplayedCards(ordered_players[0].hand),
                left_hand: this.unplayedCards(ordered_players[1].hand),
                right_hand: this.unplayedCards(ordered_players[2].hand),
                top_hand: this.unplayedCards(ordered_players[3].hand),
                current_trick : {
                    cards: this.orderCardsInTrick(game.current_trick.cards, ordered_players),
                    winner: this.winnerDirection(game.current_trick.winner, ordered_players),
                    closed: game.current_trick.closed,
                    number: game.current_trick.number
                    },
               previous_trick : this.orderCardsInTrick(game.previous_trick.cards, ordered_players),
               game_completed: this.isGameCompleted(this.state.game_completed , game.completed, game.current_trick.winner)
            })
            console.log("Current Game State !", this.state)
    }


    isGameCompleted(current_value, new_value, winner){
        if (winner){
            return (current_value || new_value)
        }else {
            return (new_value)
        }
    }


    // custom methods
    getGame(){
         const game_url = 'http://127.0.0.1:8000/game-from-id/' + this.props.game_id
         this.serverRequest = $.get(game_url, function (result) {
            console.log("Game Result", result)
            this.setStateWithGameResult(result.game)
        }.bind(this))
    }

     handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
        console.log("Incoming Game Data !!!!!!!", result)
        this.setStateWithGameResult(result)
    }

    convertCardToString(card){
        var suitMap = { 'spade': "s", 'heart': "h", 'diamond': "d", "club":"c" };
        var numberMap = { 'ace': "1", 'two': "2", 'three': "3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9", "ten":"10", "jack":"j", "queen":"q", "king":"k" };
        return numberMap[card.number] + suitMap[card.suit]
    }

    convertStringToCard(card){
        var suit = card[card.length-1]
        var number =  card.slice(0, -1)

        var suitMap = { "s":'spade', "h":'heart', "d":'diamond', "c":"club"};
        var numberMap = { "1":'ace', "2":'two', "3":'three', "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine", "10": "ten", "j":"jack", "q":"queen", "k":"king"};
        return {"number": numberMap[number] , "suit": suitMap[suit]}
    }

    unplayedCards(cards){
        var unplayed = []
        for (let i = 0; i < cards.length; i++) {
            if (cards[i].played == false){
                unplayed.push(this.convertCardToString(cards[i]))
            }
        }
        return unplayed
    }

    currentPlayerIndex(players){
        for (let i = 0; i < players.length; i++) {
                if (players[i].user == this.state.current_user.id){
                    return i
                }
             }
    }

    orderPlayers(players){
        if (players){
             var current_player_ind = this.currentPlayerIndex(players)
             return [
                players[(0 + current_player_ind) % 4],
                players[(1 + current_player_ind) % 4],
                players[(2 + current_player_ind) % 4],
                players[(3 + current_player_ind) % 4]
                ]
        }else{
            return null
            }
    }

    orderCardsInTrick(cards, players){
    var ordered_trick = [null, null, null, null]
    if (cards){
        for (let i = 0; i < cards.length; i++) {
            for (let j = 0; j < players.length; j++) {
                if (cards[i].user == players[j].user){
                    ordered_trick[j] = this.convertCardToString(cards[i])
                    }
                }
            }
        }
        return ordered_trick


    }

    winnerDirection(winner, players){
        if (winner){
            var directionMap = { "0": "bottom", '1': "left", '2': "top", "3":"right" };
            console.log("Winner", winner, players)
            for (let j = 0; j < players.length; j++) {
                if (winner == players[j].id){
                    return directionMap[j]
                }
            }
        }else{
            return null
        }
    }




    sendSocketMessage(message){
        // sends message to channels back-end
       const socket = this.refs.socket
       socket.state.ws.send(JSON.stringify(message))
    }

//     isPlayerTurn(){
//         if (this.props.current_user.id == this.state.series.current_turn.id){
//             return true
//         }else{
//             return false
//         }
//     }


    renderTrick() {
    if (this.state.current_trick){
        var trick_cards =  this.state.current_trick.cards

            if (trick_cards != null){
              return (
                 <div id="Trick"  >
                    <Trick bottom_card = {trick_cards[0]} left_card = {trick_cards[1]} top_card = {trick_cards[2]} right_card = {trick_cards[3]} winner = {this.state.current_trick.winner} />
                 </div>
              )
           }
       }
  }



    renderLeftHand(){
        if (this.state.left_hand){
            return(
                <div id='left' style={this._getHandPositions().left}>
                        <Hand hide={true} layout={"spread"} onDoubleClick={this.doNothingonDoubleClick.bind(this)} cards={this.state.left_hand} cardSize={0.8*this._getCardSize()}/>

                 </div>
            )
        }
    }

    renderRightHand(){
        if (this.state.right_hand){
            return(
                <div id='right' style={this._getHandPositions().right}>
                    <Hand hide={true} layout={"spread"} onDoubleClick={this.doNothingonDoubleClick.bind(this)} cards={this.state.right_hand} cardSize={0.8*this._getCardSize()}/>

                </div>
            )
        }
    }

    renderTopHand(){
        if (this.state.top_hand){
            return(
                 <div id='top' style={this._getHandPositions().top}>
                    <Hand hide={true} layout={"spread"} onDoubleClick={this.doNothingonDoubleClick.bind(this)} cards={this.state.top_hand} cardSize={1.2*this._getCardSize()}/>
                </div>
            )
        }
    }

    renderBottomHand(){
        if (this.state.hand){
            return(
                 <div id='bottom' style={this._getHandPositions().bottom}>
                     <Hand hide={false} onDoubleClick={this.onDoubleClick.bind(this)} layout={"spread"} cards={this.state.hand} cardSize={1.5*this._getCardSize()}/>
             </div>
            )
        }
    }


    renderHands() {
      return (
          <div>
             {this.renderLeftHand()}
             {this.renderRightHand()}
             {this.renderTopHand()}
             {this.renderBottomHand()}
          </div>
      );
  }

  trickHasCards(trick){
    if (trick==null){
        return false
        }
    if (trick.every(element => element === null)){
        return false
    } else {
    return true
    }
  }


  renderPreviousTrick(){
        var previous_trick = this.state.previous_trick

        if (this.trickHasCards(previous_trick)){
                return (
                    <div >
                        <PreviousTrick bottom_card = {previous_trick[0]} left_card = {previous_trick[1]} top_card = {previous_trick[2]} right_card = {previous_trick[3]}  />
                    </div>
                )
           }
    }



    updateGameComplete(){

        setTimeout(() => {
          if (this.state.game_completed){
            if (this.state.game_completed == true){
              this.setState({end_game_popup: this.state.game_completed})
            }
          };
        }, 6000)


    }


    renderGameScore(){

    if (this.state.end_game_popup==true){

        if (this.state.players!=null){

            var team1 = this.state.players[0].username.concat(" & " , this.state.players[2].username)
            var team2 = this.state.players[1].username.concat(" & " , this.state.players[3].username)


        return (
            <div >
{/*                     <GameScore score1={this.state.series.score1} score2={this.state.series.score2} team1={team1} team2={team2}/> */}
                    <GameScore score1={this.state.game.score1} score2={this.state.game.score2}
                               points1={this.state.game.points1} points2={this.state.game.points2}
                               series_score1={this.props.series_score1} series_score2={this.props.series_score2}
                               team1={team1} team2={team2} onClick={this.closeGameOnClick.bind(this)} />
            </div>
        )}
       }
    }

    renderCards(){
        var game_completed = false

        if (this.state.completed){
            if (this.state.game.completed == true){
                game_completed = true
            }
        }

        if (game_completed == false){
        return(
            <div >
                {this.renderHands()}
                {this.renderTrick()}
                {this.renderPreviousTrick()}
            </div>
            )
        }
    }


    render() {
        //console.log("Current GameBoard State", this.state)
        this.updateGameComplete()
        return (
            <div >

                   {this.renderCards()}
                   {this.renderGameScore()}


            <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>
            </div>
        )
    }
}


GameBoard.propTypes = {
    current_user: PropTypes.object,
    game_id: PropTypes.number,
    series_score1: PropTypes.number,
    series_score2: PropTypes.number,
    socket: PropTypes.string
}

export default GameBoard

