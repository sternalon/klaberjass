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
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                 <div class="modal-header">
                    <h2 class="modal-title" id="exampleModalLabel">Modal title</h2>
                    <button type="button" class="close" onClick={closeModal.bind(this)} aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>

                   <div class="modal-body">
                    I am a modal
                  </div>

                 <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onClick={closeModal.bind(this)}>Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
         </div>
      </div>
    </div>


  );
}

renderButton() {
  return (
    <div id='previousTrick' style={{'bottom': '2%', 'left': '2%', 'position': 'absolute'} }    >
      <button type="button" class="btn btn-primary" onClick={openModal.bind(this)} >
        Previous Trick
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
