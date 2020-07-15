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
    randomHand = (size) => {
        console.log('size: ', size)
        var cardList = Object.keys(PlayingCardsList);
        var hand = [];
        var used = {};
        for(var i = 0; i < size; i++) {
            var card = Math.floor(Math.random()*Object.keys(PlayingCardsList).length);
            console.log("card: ", card);
            while(used[card]) {
                card = Math.floor(Math.random()*Object.keys(PlayingCardsList).length);
            }
            used[card] =  true;
            hand.push(cardList[card]);
        }
        console.log("hand: ", hand)
        return hand;
    };
    _onSelectLayout = (option) => {
        console.log('You selected ', option);
        this.setState({layout: option.value}, function(){

        });
    };
    _onSelectHandSize = (option) => {
        console.log('You selected ', option);
        var hand = this.randomHand(option.value);

        this.setState({hand : hand, handSize : option}, function(){

        });
    };
    _getCardSize() {
        console.log("window: ", window.innerWidth);
        console.log('handsize', this.state.hand.length)
        console.log("size: ", window.innerWidth / this.state.hand.length)
        let cardSize = window.innerWidth / this.state.hand.length;
        return this.state.layout !== "spread" || cardSize > 100 ? 100 : cardSize;
    }


  render() {
    const handStyle = {
        margin: "auto",
        width: "10%",
        paddingBottom: "5%",
        paddingTop: "5%",
        left: "45%",
        top: "50%"
    };
      return (
          <div>
{/*                <div style={{"width": "30%", "paddingLeft":"32%"}}> */}
{/*                   Select a Layout: */}
{/*                   <Dropdown */}
{/*                       options={["fan", "spread"]} */}
{/*                       onChange={this._onSelectLayout} */}
{/*                       value={this.state.layout} */}
{/*                       placeholder="Select an option" */}
{/*                   /> */}
{/*               </div> */}


            <div id='top' style={{'transform' : 'translateY(-30%) rotate(180deg)', 'right': '50%', 'top': "5%", 'position': 'absolute'}}>
                    <Hand hide={true} layout={this.state.layout} cards={this.state.hand} cardSize={1.2*this._getCardSize()}/>
             </div>


            <div id='bottom' style={{'bottom': '-5%', 'right': '50%', 'position': 'absolute', 'height' : '30%'}}>
                     <Hand hide={false} layout={this.state.layout} cards={this.state.hand} cardSize={1.5*this._getCardSize()}/>
             </div>

             <div id='left' style={{'bottom': '40%','right': '90%', 'position': 'absolute', 'transform': 'rotate(90deg)' }}>
                    <Hand hide={true} layout={this.state.layout} cards={this.state.hand} cardSize={0.8*this._getCardSize()}/>

             </div>

              <div id='right' style={{'bottom': '40%','left': '90%', 'position': 'absolute', 'transform': 'rotate(270deg)' }}>
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

