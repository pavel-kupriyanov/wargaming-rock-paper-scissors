import React from "react";

import {Card, Spinner} from "react-bootstrap";

export default class Waiting extends React.PureComponent {

  render() {
    return (
      <Card className="mx-auto game-card shadow p-3 d-flex flex-column justify-content-center">
        <h1 className="text-center">Waiting another players...</h1>
        <div className="d-flex justify-content-center w-100">
          <Spinner animation="border"/>
        </div>
      </Card>
    )
  }
}
