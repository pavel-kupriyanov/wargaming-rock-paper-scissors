import React from "react";

import {CHOICES} from "../../app/constants";
import {Button, Modal} from "react-bootstrap";

export default class Pick extends React.Component {

  interval = null;

  constructor(props) {
    super(props);
    this.state = {
      timeout: props.timeout,
    };
    this.onPick = this.onPick.bind(this);
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
      <Modal show={true}>
        <Modal.Header>
          <Modal.Title>You pick</Modal.Title>
        </Modal.Header>
        <Modal.Body>Until the end of the wait {this.state.timeout} seconds</Modal.Body>
        <Modal.Footer>
          <Button size="lg" variant="secondary" block onClick={() => this.onPick(CHOICES.ROCK)}>Rock</Button>
          <Button size="lg" variant="light" block onClick={() => this.onPick(CHOICES.PAPER)}>Paper</Button>
          <Button size="lg" variant="info" block onClick={() => this.onPick(CHOICES.SCISSORS)}>Scissors</Button>
        </Modal.Footer>
      </Modal>
    )
  }

}
