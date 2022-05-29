import React, { Component } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'




function openModal() {
    this.setState({modalIsOpen: "block"});
  }

function closeModal() {
this.setState({modalIsOpen: "none"});
}


class GameScore extends Component {
    constructor(props){
    super(props);
    this.state = {
        modalIsOpen: true,

      }
    // This binding is necessary to make `this` work in the callback
    // this.handleClick = this.handleClick.bind(this);

  }

    //   componentWillMount() {
    //     Modal.setAppElement('body');
    // }




 onClick(){
    this.setState({modalIsOpen: "none"})
    this.props.onClick()
  }


  calculateResult(score1, score2){

    console.log("Score", score1, score2)
    if ((score1) > 1000 || score2 > 1000){
        const margin = Math.abs(score1-score2)
        if (score1 > score2){
            return (this.props.team1 + " won by " + margin + " points")
        } else if (score1 < score2){
            return (this.props.team2 + " won by " + margin + " points")
        } else {
            return ("Game Tied")
        }
    }


  }

  renderResult(score1, score2){

    const result = this.calculateResult(score1, score2)
    if (result){
        return(
            <div>
                <h1 style={{"color":"blue", "textAlign": "center"}}>Game Over!</h1>
                <p style={{"color":"black", "textAlign": "center"}}> {result} </p>
            </div>
        )
       }
  }

 renderBody(){
    return(
        <div className="modal-body" style={{"height":" 350px", "backgroundColor": "White", "marginTop": "2cm"}}>

           <table width="550" >

    <tbody>
        <tr>
            <td style={{"height":" 50px", "width":" 160px", "textAlign": "center", "fontSize": "20px"}}>{""}</td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px", "backgroundColor":"#33A5FF"}}><b>{this.props.team1}</b></td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px", "backgroundColor":"#33A5FF"}}><b>{this.props.team2}</b></td>
        </tr>
        <tr>
            <td style={{"height":" 50px", "width":" 160px", "textAlign": "center", "fontSize": "20px"}}>{"Points Won"}</td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px"}}>{this.props.points1}</td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px"}}>{this.props.points2}</td>
        </tr>
        <tr>
            <td style={{"height":" 50px", "width":" 160px", "textAlign": "center", "fontSize": "20px"}}>{"Game Result"}</td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px"}}>{this.props.score1}</td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px"}}>{this.props.score2}</td>
        </tr>
        <tr>
            <td style={{"height":" 50px", "width":" 160px", "textAlign": "center", "fontSize": "20px"}}>{"Series Score"}</td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px"}}>{this.props.series_score1}</td>
            <td style={{"height":" 50px", "textAlign": "center", "fontSize": "20px"}}>{this.props.series_score2}</td>
        </tr>

    </tbody>
</table>

            {this.renderResult(this.props.series_score1, this.props.series_score2)}

        </div>

    )

 }


 renderGameScore() {
  var modalIsOpen = this.state.modalIsOpen

  return (
    <div>
      <div style={{"display":this.state.modalIsOpen, }}  >
        <div className="modal-dialog" role="document">
            <div className="modal-content">
                 <div className="modal-header">
                    <h2 className="modal-title" id="exampleModalLabel">Game Result</h2>
                  </div>

                  {this.renderBody()}



                 <div className="modal-footer">
                    <button type="button" className="btn btn-primary" onClick={this.onClick.bind(this)}>Close</button>
{/*                     <button type="button" className="btn btn-primary">Save changes</button> */}
                </div>
            </div>
         </div>
      </div>
    </div>


  );
}





  render() {
    return (
         <div>

        {this.renderGameScore()}


       </div>
    );
  }
}

GameScore.propTypes = {
    score1: PropTypes.number,
    score2: PropTypes.number,
    points1: PropTypes.number,
    points2: PropTypes.number,
    series_score1: PropTypes.number,
    series_score2: PropTypes.number,
    team1: PropTypes.string,
    team2: PropTypes.string,
    onClick: PropTypes.func,
}

export default GameScore;
