import React from 'react'
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import Hand from "./react-playing-cards/src/PlayingCard/Hand/Hand";
import Trick from './Trick'


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
        }

        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
        this.isPlayerTurn = this.isPlayerTurn.bind(this)

    }

    onDoubleClick(card){
            console.log("DDDDDDDD", card, this.state.game_id)
            var card_dict = this.convertStringToCard(card)
            console.log("EEEEEE", card_dict["number"])
            console.log("FFFFFFF", card_dict["suit"])
            console.log("WWWWWW", this.state.game.current_trick.id)


//             this.find_card_id()
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


    // custom methods
    getGame(){
         const game_url = 'http://127.0.0.1:8000/game-from-id/' + this.props.game_id
         this.serverRequest = $.get(game_url, function (result) {
            console.log("Game Result", result)
            var players = this.orderPlayers(result.game.players)
            this.setState({
                game: result.game,
                current_player: players[0],
                players: players,
//              current_player: this.currentPlayer(result.game.players),
//              position: this.getPosition(result.game.players),
//              hand: this.currentPlayerHand(result.game.players),
                hand: this.unplayedCards(players[0].hand),
                left_hand: this.unplayedCards(players[1].hand),
                right_hand: this.unplayedCards(players[2].hand),
                top_hand: this.unplayedCards(players[3].hand),
                current_trick : this.orderCardsInTrick(result.game.current_trick.cards, players)
            })
        }.bind(this))
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


//     currentPlayerHand(players){
//     if (players){
//         for (let i = 0; i < players.length; i++) {
//             if (players[i].user == this.state.current_user.id){
//                 console.log("Current Player Hand", players[i].hand)
//                 return (
//                         this.unplayedCards(players[i].hand)
//                 )
//
//             }
//         }
//         }else{
//         return null}
//     }

//     currentPlayer(players){
//     if (players){
//         for (let i = 0; i < players.length; i++) {
//             if (players[i].user == this.state.current_user.id){
//                 console.log("Current Player", players[i])
//                 return (
//                         players[i]
//                 )
//
//             }
//         }
//         }else{
//         return null}
//     }




//      getPosition(players){
//         for (let i = 0; i < players.length; i++) {
//             if (players[i].username == this.state.current_user.username){
//                 return players[i].position
//             }
//         }
//     }


    handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
        this.setState({game: result.game,
//                        squares: result.squares
                       })

    }

    sendSocketMessage(message){
        console.log("KKKKKK", this.refs.socket)


        // sends message to channels back-end
       const socket = this.refs.socket
       socket.state.ws.send(JSON.stringify(message))
    }

    isPlayerTurn(){
        if (this.props.current_user.id == this.state.series.current_turn.id){
            return true
        }else{
            return false
        }
    }



    // ----  RENDER FUNCTIONS ---- //
    // --------------------------- //
    renderRow(row_num, cols) {

        let row = cols.map(function(square){

           // for each col, render a square for this row
           return <GameSquare game_creator={this.state.game.creator.id}
                              key={square.id}
                              owner={square.owner}
                              square_id={square.id}
                              possession_type={square.status}
                              loc_x={parseInt(square.col)}
                              loc_y={parseInt(square.row)}
                              sendSocketMessage={this.sendSocketMessage}
                              isPlayerTurn={this.isPlayerTurn}
                              />
        }.bind(this))

        return (
            <tr key={row_num}>{row}</tr>
        )
    }

    renderBoard() {
        // renders the obstruction grid/board
        // build by row and then by col, based on the height and width values
        let board = []
        let cur_row = -1
        // for each rown
        if (this.state.game != null && this.state.squares != null){
            // build the squares
            // if this is a new row, get the cols
            board = this.state.squares.map(function(square){
                if (square.row != cur_row){
                    // new row
                    cur_row = square.row
                    // get just current row cols
                    let row_cols = this.state.squares.filter(function(c){
                        if (c.row == cur_row){
                            return c
                        }
                    })
                    // with array of cols for this row, render it out
                    //board.push(this.renderRow(cur_row, row_cols))
                   return this.renderRow(cur_row, row_cols )
                }

             }, this)

        }else{
           board = <tr><td>'LOADING...'</td></tr>

        }
        return board
    }

    renderTrick() {
    var current_trick =  this.state.current_trick

        if (this.state.current_trick != null){
          return (
             <div >
                <Trick bottom_card = {current_trick[0]} left_card = {current_trick[1]} top_card = {current_trick[2]} right_card = {current_trick[3]}  />
             </div>
          )
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

//     currentTurn(){
//         if (this.state.game){
//             if (this.state.game.completed != null){
//                 // game is over
//                 return <h3>The Winner: <span className="text-primary">{(this.state.game.current_turn.username)}</span></h3>
//             }else{
//                 return <h3>Current Turn:
//                     <span className="text-primary">{(this.state.game.current_turn.username)}</span>
//                  </h3>
//             }
//
//         }
//     }


    render() {
        return (
            <div >


                   {this.renderHands()}

                   {this.renderTrick()}


            <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>
            </div>
        )
    }
}

GameBoard.propTypes = {
    current_user: PropTypes.object,
    game_id: PropTypes.number,
    socket: PropTypes.string
}

export default GameBoard