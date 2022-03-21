import React from 'react';
import ReactDOM from 'react-dom';
import Dropdown from 'react-dropdown'
import PlayingCardsList from "./react-playing-cards/src/PlayingCard/Hand/PlayingCard/PlayingCardsList";
import Hand from "./react-playing-cards/src/PlayingCard/Hand/Hand";

class Jass extends React.Component {
    constructor(){
    super();
this.state = {hand: ["1d", "1c", "1s", "1h", "1d", "1c", "1s", "1h"],
layout: "spread",
handSize: "8" }

  }


    _getCardSize() {
//         console.log("window: ", window.innerWidth);
//         console.log('handsize', this.state.hand.length)
//         console.log("size: ", window.innerWidth / this.state.hand.length)
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


//             handS: {'bottom': '0', 'right': '50%', 'position': 'absolute', 'height' : '30%'},
//             handNE : {'bottom': '0', 'right': '50%', 'position': 'absolute', 'transform': 'rotate(45deg) translate(' + props.cardSize +'px -' + window.innerHeight() + ')', 'transform-origin' : ' 0px -' + window.innerWidth / 2 + 'px'},
//             board: {'left': 'calc(50% - ' + props.cardSize * 1.4 + 'px)', 'top': '35%', 'position': 'absolute', 'width': props.cardSize * 4 + 'px'}


  render() {

      return (
          <div>


            <div id='top' style={this._getHandPositions().top}>
                    <Hand hide={true} layout={this.state.layout} cards={this.state.hand} cardSize={1.2*this._getCardSize()}/>
             </div>


            <div id='bottom' style={this._getHandPositions().bottom}>
                     <Hand hide={false} layout={this.state.layout} cards={this.state.hand} cardSize={1.5*this._getCardSize()}/>
             </div>

             <div id='left' style={this._getHandPositions().left}>
                    <Hand hide={true} layout={this.state.layout} cards={this.state.hand} cardSize={0.8*this._getCardSize()}/>

             </div>

              <div id='right' style={this._getHandPositions().right}>
                    <Hand hide={true} layout={this.state.layout} cards={this.state.hand} cardSize={0.8*this._getCardSize()}/>

             </div>

{/*               <div style={handStyle}> */}
{/*                   <Hand hide={false} layout={this.state.layout} cards={this.state.hand} cardSize={this._getCardSize()}/> */}
{/*               </div> */}
          </div>
      );
  }
}


export default Jass;

