import React, { Component } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import PlayingCard from './react-playing-cards/src/PlayingCard/Hand/PlayingCard/PlayingCard';



class Trick extends Component {
    constructor(props){
    super(props);
this.state = {
        current_player: null,
        bottom_card: null,
        left_card: null,
        top_card: null,
        right_card: null,
        card: "1h",
        cards: ["1h", "1h", "1h"],
      }


  }


//   componentDidMount() {
//         this.getTrick()
//     }

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

//    // custom methods
//     getTrick(){
//     console.log("HHHHHHHH", this.props.trick_id)
//          const trick_url = 'http://127.0.0.1:8000/trick-from-id/' + this.props.trick_id
//          this.serverRequest = $.get(trick_url, function (result) {
//             console.log("Trick Result", result)
//             this.setState({
//                 trick: result.trick,
// //                 bottom:
// //                 left:
// //                 top:
// //                 right:
//             })
//         }.bind(this))
//     }

   renderLeftCard(){
       if (this.props.left_card){
           return (
                <div id='left_card' style={this._getCardPositions().left}>
                           <PlayingCard height={ 150 } card={this.props.left_card} flipped={ false } elevateOnClick={true} />
                </div>
          )
       }
   }

   renderRightCard(){
       if (this.props.right_card){
           return (
                <div id='right_card' style={this._getCardPositions().right}>
                   <PlayingCard height={ 150 } card={this.props.right_card} flipped={ false } elevateOnClick={true} />
                </div>
          )
       }
   }

   renderBottomCard(){
       if (this.props.bottom_card){
           return (
                <div id='bottom_card' style={this._getCardPositions().bottom}>
                  <PlayingCard height={ 150 } card={this.props.bottom_card} flipped={ false } elevateOnClick={true} />
               </div>
          )
       }
   }

   renderTopCard(){
       if (this.props.top_card){
           return (
                <div id='top_card' style={this._getCardPositions().top}>
                   <PlayingCard height={ 150 } card={this.props.top_card} flipped={ false } elevateOnClick={true} />
                </div>
          )
      }
   }




  render() {
    console.log("Trick Bottom: ", this.props.bottom_card)
    console.log("Trick Left: ", this.props.left_card)
    console.log("Trick Top: ", this.props.top_card)
    console.log("Trick Right: ", this.props.right_card)
    return (
         <div>
            {this.renderBottomCard()}
            {this.renderLeftCard()}
            {this.renderTopCard()}
            {this.renderRightCard()}

       </div>
    );
  }
}

Trick.propTypes = {
//     current_player: PropTypes.object,
//     trick_id: PropTypes.number,
    bottom_card: PropTypes.string,
    left_card: PropTypes.string,
    top_card: PropTypes.string,
    right_card: PropTypes.string,
}

export default Trick;
