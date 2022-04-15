import React from 'react'
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import Hand from "./react-playing-cards/src/PlayingCard/Hand/Hand";
import GameBoard from './GameBoard'
import Scoreboard from './Scoreboard'


class SeriesBoard extends React.Component {
    // lifecycle methods
    constructor(props) {
        super(props)
        this.state = {
            series: null,
            position: null,
            users: null,
            current_game: null,
            current_user: props.current_user,
            hand: {
                cards: ["2d", "2c", "2s", "2h", "2d", "2c", "2s", "2h"],
                layout: "spread",
                handSize: "8",
            },
        }

        // bind button click
        this.onCreateGameClick = this.onCreateGameClick.bind(this);
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
    }


    componentDidMount() {
        this.getSeries()
    }

    onCreateGameClick(event) {
        this.sendSocketMessage({action: "create_game", series_id: this.state.series.series_id})
    }

    componentWillUnmount() {
        this.serverRequest.abort();
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
                users: result.series.players,
            })
        }.bind(this))
    }

     getPosition(users){
        for (let i = 0; i < users.length; i++) {
            if (users[i].username == this.state.current_user.username){
                return users[i].position
            }
        }
    }



    sendSocketMessage(message){
        // sends message to channels back-end
       const socket = this.refs.socket
       socket.state.ws.send(JSON.stringify(message))
    }



    getPlayerName(position){
        var position_mod_4 = position % 4
        if (this.state.users[position_mod_4]){
            return this.state.users[position_mod_4].username
           }else{
               return null
           }
    }


    renderNames() {
        var player_position = this.state.position -1
        if (this.state.users) {
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

                      <div id='right' style={this._getNamePositions().right}>
                             <h2> {this.getPlayerName(player_position+3)}</h2>
                     </div>
                  </div>
              );
            }else{
         return (<div> </div>)
         }
    }

    renderRefreshButton(){
        return (
              <div id='center' style={{'top': '50%', 'left': '35%', 'position': 'fixed'}}>
                            <a className="btn btn btn-info btn-lg" href={"."}>Refresh to see if players have joined</a>
              </div>
         )
    }


    renderDealButton(){
        return (
              <div id='center' style={{'top': '50%', 'left': '40%', 'position': 'fixed'}}>
                        <a className="btn btn btn-danger btn-lg" href="" onClick={this.onCreateGameClick} id="create_game">Click here to Deal!</a>
              </div>
         )
    }

    renderGameBoard(){
        return (
            <div >
                    <GameBoard current_user={this.props.current_user} game_id={this.state.series.current_game} socket = {this.props.socket}
                                 sendSocketMessage={this.sendSocketMessage} />
            </div>
        )
    }

    Scoreboard(){
        return (
            <div >
                    <Scoreboard score1="1" score1="2" />
            </div>
        )
    }

    renderDealOrLoading() {
        if (this.state.users){
            if (this.state.users.length<4){
                return this.renderRefreshButton()
            }else{
                if (this.state.series != null){
                    if (this.state.series.current_game == null){
                        return this.renderDealButton()
                    }
                    else{
                        return this.renderGameBoard()
                    }
                }
            }
        }
    }


    render() {
        return (
            <div className="row">

                   {this.renderNames()}
                   {this.renderDealOrLoading()}
                   {this.Scoreboard()}



            </div>
        )
    }
}

SeriesBoard.propTypes = {
    current_user: PropTypes.object,
    series_id: PropTypes.number,
    socket: PropTypes.string
}

export default SeriesBoard