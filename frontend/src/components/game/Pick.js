import React from "react";

import {CHOICES} from "../../app/constants";

export default class Pick extends React.Component {

  interval = null;

  constructor(props) {
    super(props);
    this.state = {
      timeout: this.props.timeout,
    };
    this.onReady = this.onReady.bind(this);
  }

  componentDidMount() {
    this.interval = setInterval(() => {
      let timeout = this.state.timeout;
      if (timeout === 0) {
        clearInterval(this.interval);
        this.props.onTimeout();
      }
      this.setState({timeout: timeout - 1})
    }, 1000)
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }


  onPick(value) {
    this.props.onPick(value);
    clearInterval(this.interval);
  }

  render() {
    return (
      <React.Fragment>
        <h1>You pick</h1>
        <h1>{this.state.timeout}</h1>
        <button onClick={() => this.onPick(CHOICES.ROCK)}>Rock</button>
        <button onClick={() => this.onPick(CHOICES.PAPER)}>Paper</button>
        <button onClick={() => this.onPick(CHOICES.SCISSORS)}>Scissors</button>
      </React.Fragment>
    )
  }

}
