import React from "react";
import PropTypes from 'prop-types';
import {Button, Modal} from "react-bootstrap";

export default class TimeoutModal extends React.PureComponent {

  interval = null;

  constructor(props) {
    super(props);
    this.state = {
      timeout: props.timeout,
    };
    this.onClick = this.onClick.bind(this);
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


  onClick(callback) {
    callback();
    clearInterval(this.interval);
  }

  render() {

    const {header, messageTemplate, buttonsConfig} = this.props;

    return (
      <Modal show={true}>
        <Modal.Header>
          <Modal.Title>{header}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{messageTemplate.replace("{timeout}", this.state.timeout.toString())}</Modal.Body>
        <Modal.Footer>
          {buttonsConfig.map((conf, i) =>
            <Button size="lg" variant={conf.variant} block onClick={() => this.onClick(conf.callback)}
                    key={`button-${i}`}>
              {conf.text}
            </Button>)
          }
        </Modal.Footer>
      </Modal>
    )
  }
}

TimeoutModal.propTypes = {
  header: PropTypes.string,
  messageTemplate: PropTypes.string,
  buttonsConfig: PropTypes.array,
  timeout: PropTypes.number
};

