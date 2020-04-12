import React from "react";

export default class AreYouReady extends React.Component {

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


  onReady() {
    this.props.onReady();
    clearInterval(this.interval);
  }

  render() {
    return (
      <React.Fragment>
        <h1>Are you ready?</h1>
        <h1>{this.state.timeout}</h1>
        <button onClick={this.onReady}>Ready!</button>
      </React.Fragment>
    )
  }

}
