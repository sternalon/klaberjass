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


class Scoreboard extends Component {
    constructor(props){
    super(props);
    this.state = {
        modalIsOpen: "none",

      }
    // This binding is necessary to make `this` work in the callback
    // this.handleClick = this.handleClick.bind(this);

  }

    //   componentWillMount() {
    //     Modal.setAppElement('body');
    // }

     componentWillUnmount() {
        this.serverRequest.abort();
    }


 renderScoreboard() {
  var modalIsOpen = this.state.modalIsOpen

  return (
    <div>
      <div style={{"display":this.state.modalIsOpen, }}  >
        <div className="modal-dialog" role="document">
            <div className="modal-content">
                 <div className="modal-header">
                    <button type="button" className="close" onClick={closeModal.bind(this)} aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                    <h2 className="modal-title" id="exampleModalLabel">Scoreboard</h2>
                  </div>

                   <div className="modal-body">
                    Scoreboard Goes Here
                  </div>

                 <div className="modal-footer">
                    <button type="button" className="btn btn-secondary" onClick={closeModal.bind(this)}>Close</button>
                    <button type="button" className="btn btn-primary">Save changes</button>
                </div>
            </div>
         </div>
      </div>
    </div>


  );
}

renderButton() {
  return (
    <div id='scoreboardButton' style={{'bottom': '2%', 'left': '2%', 'position': 'absolute'} }    >
      <button type="button" className="btn btn-secondary" onClick={openModal.bind(this)}  >
        . Scoreboard .
      </button>
    </div>


  );
}


  render() {
    return (
         <div>

        {this.renderButton()}
        {this.renderScoreboard()}


       </div>
    );
  }
}

Scoreboard.propTypes = {
    score1: PropTypes.string,
    score2: PropTypes.string,
}

export default Scoreboard;
