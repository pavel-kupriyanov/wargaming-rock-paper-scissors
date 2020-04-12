import React from "react";

import {Card} from "react-bootstrap";

export default class Info extends React.PureComponent {

  render() {
    return (
      <Card className="mx-auto game-card shadow p-3 d-flex flex-column justify-content-center">
        <h1 className="text-center">{this.props.message}</h1>
      </Card>
    )
  }
}
