import React from 'react'
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import Hand from "./react-playing-cards/src/PlayingCard/Hand/Hand";
// import GameSquare from './GameSquare'


class GameBoard extends React.Component {
    // lifecycle methods
    constructor(props) {
        super(props)
        this.state = {
            series: null,
            position: null,
            current_user: props.current_user,
            hand: {
                cards: ["2d", "2c", "2s", "2h", "2d", "2c", "2s", "2h"],
                layout: "spread",
                handSize: "8",
            },
        }

        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this)
        this.isPlayerTurn = this.isPlayerTurn.bind(this)

    }


    componentDidMount() {
        this.getSeries()
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    _getCardSize() {
//         console.log("window: ", window.innerWidth);
//         console.log('handsize', this.state.hand.length)
//         console.log("size: ", window.innerWidth / this.state.hand.length)
        let cardSize = window.innerWidth / this.state.hand.cards.length;
        return this.state.hand.layout !== "spread" || cardSize > 100 ? 100 : cardSize;
    }

    _getHandPositions() {
        return {
            top:{'transform' : 'translateY(-30%) rotate(180deg)', 'right': '50%', 'top': "5%", 'position': 'absolute'},
            bottom:{'bottom': '-5%', 'right': '50%', 'position': 'absolute', 'height' : '30%'},
            left:{'bottom': '40%','right': '90%', 'position': 'absolute', 'transform': 'rotate(90deg)' },
            right:{'bottom': '40%','left': '90%', 'position': 'absolute', 'transform': 'rotate(270deg)' }
            }
           }

     _getNamePositions() {
        return {
            top:{'right': '50%', 'top': "3%", 'position': 'absolute'},
            bottom:{'bottom': '-22%', 'right': '50%', 'position': 'absolute', 'height' : '30%'},
            left: {'bottom': '40%','right': '90%', 'position': 'absolute', 'transform': 'rotate(270deg)' },
            right:{'bottom': '40%','left': '90%', 'position': 'absolute', 'transform': 'rotate(90deg)' }
            }
           }

    // custom methods
    getSeries(){
         const series_url = 'http://127.0.0.1:8000/series-from-id/' + this.props.series_id
         this.serverRequest = $.get(series_url, function (result) {
            this.setState({
                series: result.series,
                position: this.getPosition(result.series.players),
            })
        }.bind(this))
    }

     getPosition(players){
        for (let i = 0; i < players.length; i++) {
            if (players[i].username == this.state.current_user.username){
                return players[i].position
            }
        }
    }


    handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
        this.setState({series: result.series,
                       squares: result.squares
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

    getPlayerName(position){
        var position_mod_4 = position % 4
        if (this.state.series.players[position_mod_4]){
            return this.state.series.players[position_mod_4].username
           }else{
               return null
           }
    }


    renderNames() {
        var player_position = this.state.position -1
        if (this.state.series) {
              return (
                  <div>

                    <div id='bottom' style={this._getNamePositions().bottom}>
                             <h2> {this.getPlayerName(player_position)}</h2>
                    </div>
                     <div id='left' style={this._getNamePositions().left}>
                           <h2> {this.getPlayerName(player_position+1)}</h2>
                     </div>

                    <div id='top' style={this._getNamePositions().top}>
                       <h2> {this.getPlayerName(player_position+2)}</h2>
                     </div>

                      <div id='right' style={this._getHandPositions().right}>
                             <h2> {this.getPlayerName(player_position+3)}</h2>
                     </div>
                  </div>
              );
            }else{
         return (<div> </div>)
         }
    }

    renderDeck() {

      return (
          <div>


            <div id='top' style={this._getHandPositions().top}>
                    <Hand hide={true} layout={this.state.hand.layout} cards={this.state.hand.cards} cardSize={1.2*this._getCardSize()}/>
             </div>


            <div id='bottom' style={this._getHandPositions().bottom}>
                     <Hand hide={false} layout={this.state.hand.layout} cards={this.state.hand.cards} cardSize={1.5*this._getCardSize()}/>
             </div>

             <div id='left' style={this._getHandPositions().left}>
                    <Hand hide={true} layout={this.state.hand.layout} cards={this.state.hand.cards} cardSize={0.8*this._getCardSize()}/>

             </div>

              <div id='right' style={this._getHandPositions().right}>
                    <Hand hide={true} layout={this.state.hand.layout} cards={this.state.hand.cards} cardSize={0.8*this._getCardSize()}/>

             </div>

          </div>
      );
  }

    currentTurn(){
        if (this.state.game){
            if (this.state.game.completed != null){
                // game is over
                return <h3>The Winner: <span className="text-primary">{(this.state.game.current_turn.username)}</span></h3>
            }else{
                return <h3>Current Turn:
                    <span className="text-primary">{(this.state.game.current_turn.username)}</span>
                 </h3>
            }

        }
    }


    render() {
        console.log("BBBBB", this)

        return (
            <div className="row">

                   { this.renderNames() }
                   {this.renderDeck()}


                    {this.currentTurn()}



            <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>
            </div>
        )
    }
}

GameBoard.propTypes = {
    game_id: PropTypes.number,
    socket: PropTypes.string,
    current_user: PropTypes.object

}

export default GameBoard