import React, { Component } from "react";
import { render } from "react-dom";

class Lobby extends Component {
  render() {
        return <h1>Lobby World!</h1>
    }
}

export default Lobby;

const container = document.getElementById("lobby_component");
render(<Lobby />, container);