import React, { Component } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import PlayingCard from './react-playing-cards/src/PlayingCard/Hand/PlayingCard/PlayingCard';



class Trick extends Component {
    constructor(props){
    super(props);
    this.wrapperRef =  React.createRef();
    this.state = {
        current_player: null,
        bottom_card: null,
        left_card: null,
        top_card: null,
        right_card: null,
        winner : null
      }
    // This binding is necessary to make `this` work in the callback
//     this.handleClick = this.handleClick.bind(this);

  }


//   componentDidMount() {
//         this.getTrick()
//     }

     componentWillUnmount() {
        this.serverRequest.abort();
    }

    _getOpenTrickPosition(){
        return {
                top:{'bottom': '56%', 'left': '45%', 'position': 'absolute', 'height' : '30%', 'transform' : 'rotate(180deg)'},
                bottom:{'bottom': '18%', 'left': '45%', 'position': 'absolute', 'height' : '30%'},
                left:{'bottom': '45%', 'left': '30%', 'position': 'absolute', 'transform': 'translateX(90%) rotate(90deg)' },
                right:{'bottom': '45%','left': '54%', 'position': 'absolute', 'transform': 'rotate(270deg)' },
            }
    }

    _getLeftWinningPosition(){
        return {
                top:{'bottom': '56%', 'left': '-20%', 'position': 'absolute', 'height' : '30%', 'transform' : 'rotate(180deg)', 'transition': 'left .5s' },
                bottom:{'bottom': '18%', 'left': '-20%', 'position': 'absolute', 'height' : '30%', 'transition': 'left .5s' },
                left:{'bottom': '45%', 'left': '-20%', 'position': 'absolute', 'transform': 'translateX(90%) rotate(90deg)', 'transition': 'left .5s'  },
                right:{'bottom': '45%','left': '-20%', 'position': 'absolute', 'transform': 'rotate(270deg)', 'transition': 'left .5s'  },
            }
    }

    _getRightWinningPosition(){
        return {
                top:{'bottom': '56%', 'left': '110%', 'position': 'absolute', 'height' : '30%', 'transform' : 'rotate(180deg)', 'transition': 'left .5s' },
                bottom:{'bottom': '18%', 'left': '110%', 'position': 'absolute', 'height' : '30%', 'transition': 'left .5s' },
                left:{'bottom': '45%', 'left': '110%', 'position': 'absolute', 'transform': 'translateX(90%) rotate(90deg)', 'transition': 'left .5s'  },
                right:{'bottom': '45%','left': '110%', 'position': 'absolute', 'transform': 'rotate(270deg)', 'transition': 'left .5s'  },
            }
    }

    _getTopWinningPosition(){
        return {
                top:{'bottom': '110%', 'left': '45%', 'position': 'absolute', 'height' : '30%', 'transform' : 'rotate(180deg)', 'transition': 'bottom .5s'},
                bottom:{'bottom': '110%', 'left': '45%', 'position': 'absolute', 'height' : '30%', 'transition': 'bottom .5s'},
                left:{'bottom': '110%', 'left': '30%', 'position': 'absolute', 'transform': 'translateX(90%) rotate(90deg)', 'transition': 'bottom .5s' },
                right:{'bottom': '110%','left': '54%', 'position': 'absolute', 'transform': 'rotate(270deg)', 'transition': 'bottom .5s' },
            }
    }

    _getBottomWinningPosition(){
        return {
                top:{'bottom': '-40%', 'left': '45%', 'position': 'absolute', 'height' : '30%', 'transform' : 'rotate(180deg)', 'transition': 'bottom .5s'},
                bottom:{'bottom': '-40%', 'left': '45%', 'position': 'absolute', 'height' : '30%', 'transition': 'bottom .5s'},
                left:{'bottom': '-40%', 'left': '30%', 'position': 'absolute', 'transform': 'translateX(90%) rotate(90deg)', 'transition': 'bottom .5s' },
                right:{'bottom': '-40%','left': '54%', 'position': 'absolute', 'transform': 'rotate(270deg)', 'transition': 'bottom .5s' },
            }
    }


    _getCardPositions() {
        if (this.state.winner == null){
            return this._getOpenTrickPosition()
         }else if (this.state.winner == "left"){
            return this._getLeftWinningPosition()
         }else if (this.state.winner == "bottom") {
            return this._getBottomWinningPosition()
         }else if (this.state.winner == "right") {
            return this._getRightWinningPosition()
         }else if (this.state.winner == "top") {
            return this._getTopWinningPosition()
         }
       }


   renderLeftCard(){
       if (this.props.left_card){
           return (
                <div id='left_card' style={this._getCardPositions().left}>
                           <PlayingCard height={ 150 } card={this.props.left_card} flipped={this.state.winner!=null} elevateOnClick={true} />
                </div>
          )
       }
   }

   renderRightCard(){
       if (this.props.right_card){
           return (
                <div id='right_card' style={this._getCardPositions().right}>
                   <PlayingCard height={ 150 } card={this.props.right_card} flipped={this.state.winner!=null} elevateOnClick={true} />
                </div>
          )
       }
   }

   renderBottomCard(){
       if (this.props.bottom_card){
           return (
                <div id='bottom_card' style={this._getCardPositions().bottom}>
                  <PlayingCard height={ 150 } card={this.props.bottom_card} flipped={this.state.winner!=null} elevateOnClick={true} />
               </div>
          )
       }
   }

   renderTopCard(){
       if (this.props.top_card){
           return (
                <div id='top_card' style={this._getCardPositions().top}>
                   <PlayingCard height={ 150 } card={this.props.top_card} flipped={(this.state.winner!=null)} elevateOnClick={true} />
                </div>
          )
      }
   }




   updateWinner(){

        setTimeout(() => {
          this.setState({winner: this.props.winner});
        }, 2500)
    }



  render() {
    this.updateWinner()
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
    winner: PropTypes.string,
}

export default Trick;
