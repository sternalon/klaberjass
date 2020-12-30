import React, { Component } from 'react';
//import {createStore } from 'redux';
import Dropdown from 'react-dropdown'
import PlayingCard from './react-playing-cards/src/PlayingCard/Hand/PlayingCard/PlayingCard';



class Trick extends Component {
    constructor(props){
    super(props);
this.state = {
        card: "1h",
        cards: props.cards,
      }

  }

    _getCardSize() {
        let cardSize = window.innerWidth / this.state.hand.length;
        return this.state.layout !== "spread" || cardSize > 100 ? 100 : cardSize;
    }

    _getCardPositions() {
        return {
            top:{'transform' : 'translateY(-30%) rotate(180deg)', 'top': "-30%", 'position': 'absolute'},
            bottom:{'bottom': '50%', 'position': 'absolute', 'height' : '30%'},
            left:{'bottom': '60%', 'left': '10%', 'position': 'absolute', 'transform': 'translateX(90%) rotate(90deg)' },
            right:{'bottom': '60%','right': '10%', 'position': 'absolute', 'transform': 'rotate(270deg)' },
            }
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

export default Trick;
