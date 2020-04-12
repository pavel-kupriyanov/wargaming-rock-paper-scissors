import React from "react";
import {Button, Modal} from "react-bootstrap";

export default class AreYouReady extends React.Component {

  interval = null;

  constructor(props) {
    super(props);
    this.state = {
      timeout: props.timeout,
    };
    console.log(this.state);
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


  onReady() {
    this.props.onReady();
    clearInterval(this.interval);
  }

  render() {
    return (
      <Modal show={true}>
        <Modal.Header>
          <Modal.Title>Are you ready?</Modal.Title>
        </Modal.Header>
        <Modal.Body>You will be disconnected after {this.state.timeout} seconds</Modal.Body>
        <Modal.Footer><Button size="lg" block onClick={this.onReady}>Ready!</Button></Modal.Footer>
      </Modal>
    )
  }
}
