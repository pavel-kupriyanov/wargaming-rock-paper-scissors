import React from "react";
import PropTypes from 'prop-types';

import {Card, Spinner} from "react-bootstrap";
import PropTypes from "prop-types";

export default class InfoCard extends React.PureComponent {

  render() {
    const {message, spinner} = this.props;

    return (
      <Card className={"mx-auto shadow p-3 d-flex flex-column justify-content-center game-card"}>
        <h1 className="text-center">{message}</h1>
        {spinner && <div className="d-flex justify-content-center w-100">
          <Spinner animation="border"/>
        </div>}
      </Card>
    )
  }
}

InfoCard.propTypes = {
  message: PropTypes.string,
  spinner: PropTypes.bool,
};
