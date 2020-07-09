import React from 'react';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket'
import $ from 'jquery'
import PropTypes from 'prop-types';
import PlayerSeries from './PlayerSeries'


class LobbyBase extends React.Component {

    render() {
        return <h1>LobbyBase World!</h1>
    }

    constructor(props) {
        super(props);
        this.state = {
            player_series_list: [],
            available_series_list: []
        }

        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
    }

    getPlayerSeries(){
        this.serverRequest = $.get('http://localhost:8080/player-series/?format=json', function (result) {
           this.setState({
            player_series_list: result,
             })
        }.bind(this))
    }

    componentDidMount() {
       this.getPlayerSeries()
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
        // new series, so get an updated list of this player's series
        this.getPlayerSeries()
        // we've received an updated list of available series
        this.setState({available_series_list: result})
    }

    sendSocketMessage(message){
        // sends message to channels back-end
       const socket = this.refs.socket
       console.log("YOLOLOLOLO", JSON.stringify(message))
       socket.state.ws.send(JSON.stringify(message))
    }

    render(){
        return (
            <div className="row">
                <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>
                <div className="col-lg-4">
                    <PlayerSeries player={this.props.current_user} series_list={this.state.player_series_list}
                                 sendSocketMessage={this.sendSocketMessage} />
                </div>
            </div>

        )
    }
}
 
LobbyBase.propTypes = {
    socket: PropTypes.string
};
 
export default LobbyBase;

