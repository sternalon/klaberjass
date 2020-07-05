import React, { Component } from "react";
import { render } from "react-dom";

class Hello extends Component {
  render() {
        return <h1>Hello World!</h1>
    }
}

export default Hello;

const container = document.getElementById("app");
render(<Hello />, container);