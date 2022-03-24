import React from 'react'
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import Hand from "./react-playing-cards/src/PlayingCard/Hand/Hand";


class GameBoard extends React.Component {
    // lifecycle methods
    constructor(props) {
        super(props)
        this.hand_layout= "spread"
        this.state = {
            game: null,
            position: null,
            players: null,
            current_game: null,
            current_user: props.current_user,
            left_hand:  ["1d", "2c", "3s", "2h", "2d", "2c", "2s", "2h"],
            right_hand: ["1d", "2c", "3s", "2h", "2d", "2c", "2s", "2h"],
            top_hand: ["1d", "2c", "3s", "2h", "2d", "2c", "2s", "2h"],
            hand:  ["1d", "2c", "3s", "2h", "2d", "2c", "2s", "2h"],
        }

        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
        this.isPlayerTurn = this.isPlayerTurn.bind(this)

    }


    componentDidMount() {
        this.getGame()
    }


    componentWillUnmount() {
        this.serverRequest.abort();
    }

    _getCardSize() {
        let cardSize = window.innerWidth / this.state.hand.length;
        return this.state.layout !== "spread" || cardSize > 100 ? 100 : cardSize;
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
            this.setState({
                game: result.game,
//               position: this.getPosition(result.game.players),
                 players: result.game.players,
                 hand: this.currentPlayerHand(result.game.players)
            })
        }.bind(this))
    }

    convertCardToString(card){
        var suitMap = { 'spade': "s", 'heart': "h", 'diamond': "d", "club":"c" };
        var numberMap = { 'ace': "1", 'two': "2", 'three': "3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9", "ten":"10", "jack":"j", "queen":"q", "king":"k" };
        return numberMap[card.number] + suitMap[card.suit]
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

    currentPlayerHand(players){
    if (players){
        for (let i = 0; i < players.length; i++) {
            if (players[i].user == this.state.current_user.id){
                console.log("AAAAA", players[i].hand)
                return (
                        this.unplayedCards(players[i].hand)
                )

            }
        }
        }else{
        return null}
    }

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




    renderDeck() {
        const hand_layout = "spread"

      return (
          <div>


            <div id='top' style={this._getHandPositions().top}>
                    <Hand hide={true} layout={hand_layout} cards={this.state.top_hand} cardSize={1.2*this._getCardSize()}/>
             </div>


            <div id='bottom' style={this._getHandPositions().bottom}>
                     <Hand hide={false} layout={hand_layout} cards={this.state.hand} cardSize={1.5*this._getCardSize()}/>
             </div>

             <div id='left' style={this._getHandPositions().left}>
                    <Hand hide={true} layout={hand_layout} cards={this.state.left_hand} cardSize={0.8*this._getCardSize()}/>

             </div>

              <div id='right' style={this._getHandPositions().right}>
                    <Hand hide={true} layout={hand_layout} cards={this.state.right_hand} cardSize={0.8*this._getCardSize()}/>

             </div>

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
        console.log("This is the gameboard", this.props.game_id)
        return (
            <div className="row">


                   {this.renderDeck()}


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