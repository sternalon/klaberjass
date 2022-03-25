import React, { Component } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import PlayingCard from './react-playing-cards/src/PlayingCard/Hand/PlayingCard/PlayingCard';



class Trick extends Component {
    constructor(props){
    super(props);
this.state = {
        card: "1h",
        cards: ["1h", "1h", "1h", "1h"],
      }


  }


  componentDidMount() {
        this.getTrick()
    }

     componentWillUnmount() {
        this.serverRequest.abort();
    }


    _getCardPositions() {
        return {
            top:{'bottom': '56%', 'left': '45%', 'position': 'absolute', 'height' : '30%', 'transform' : 'rotate(180deg)' },
            bottom:{'bottom': '18%', 'left': '45%', 'position': 'absolute', 'height' : '30%'},
            left:{'bottom': '45%', 'left': '30%', 'position': 'absolute', 'transform': 'translateX(90%) rotate(90deg)' },
            right:{'bottom': '45%','right': '39%', 'position': 'absolute', 'transform': 'rotate(270deg)' },
            }
           }

   // custom methods
    getTrick(){
    console.log("HHHHHHHH", this.props.trick_id)
         const trick_url = 'http://127.0.0.1:8000/trick-from-id/' + this.props.trick_id
         this.serverRequest = $.get(trick_url, function (result) {
            console.log("Trick Result", result)
            this.setState({
                trick: result.trick,
            })
        }.bind(this))
    }




  render() {
    return (
         <div>
            <div id='left_card' style={this._getCardPositions().left}>
               <PlayingCard height={ 150 } card={ this.state.cards[0] } flipped={ false } elevateOnClick={true} />
            </div>
            <div id='top_card' style={this._getCardPositions().top}>
               <PlayingCard height={ 150 } card={ this.state.cards[1] } flipped={ false } elevateOnClick={true} />
            </div>
            <div id='right_card' style={this._getCardPositions().right}>
               <PlayingCard height={ 150 } card={ this.state.cards[2] } flipped={ false } elevateOnClick={true} />
            </div>
           <div id='bottom_card' style={this._getCardPositions().bottom}>
              <PlayingCard height={ 150 } card={ this.state.cards[3] } flipped={ false } elevateOnClick={true} />
           </div>
       </div>
    );
  }
}

Trick.propTypes = {
    current_user: PropTypes.object,
    trick_id: PropTypes.number,
    socket: PropTypes.string
}

export default Trick;
