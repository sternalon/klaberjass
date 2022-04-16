import React, { Component } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery'
import Websocket from 'react-websocket'
import Trick from './Trick'





function openModal() {
    this.setState({modalIsOpen: "block"});
  }

function closeModal() {
this.setState({modalIsOpen: "none"});
}


class PreviousTrick extends Component {
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

 renderBody(){
    return(
        <div className="modal-body">
             <div id="Previous Trick" style={{"height":" 400px", "backgroundColor": "Gainsboro"}} >
                    <Trick bottom_card = {this.props.bottom_card} left_card = {this.props.left_card} top_card = {this.props.top_card} right_card = {this.props.right_card} winner = {null} previous_trick ={true} />
              </div>

        </div>
    )


 }


 renderPreviousTrick() {
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
                    <h2 className="modal-title" id="exampleModalLabel">Previous Trick</h2>

                  </div>

                  {this.renderBody()}


                 <div className="modal-footer">
                    <button type="button" className="btn btn-primary" onClick={closeModal.bind(this)}>Close</button>
                </div>
            </div>
         </div>
      </div>
    </div>


  );
}

renderButton() {
  return (
    <div id='previousTrick' style={{'bottom': '6%', 'left': '2%', 'position': 'absolute'} }    >
      <button type="button" className="btn btn-primary" onClick={openModal.bind(this)} >
         Previous Trick
      </button>
    </div>


  );
}


  render() {
    return (
         <div>

        {this.renderButton()}
        {this.renderPreviousTrick()}


       </div>
    );
  }
}

PreviousTrick.propTypes = {
    bottom_card: PropTypes.string,
    left_card: PropTypes.string,
    top_card: PropTypes.string,
    right_card: PropTypes.string,
}

export default PreviousTrick;
