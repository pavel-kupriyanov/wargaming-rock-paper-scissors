import React from "react";

import {Card, Col, Row, Spinner} from "react-bootstrap";

export default class Waiting extends React.PureComponent {

  render() {
    return (
      <Row>
        <Col>
          <Card className="mx-auto app-card shadow p-3 d-flex flex-column justify-content-center">
            <h1 className="text-center">Finding opponents...</h1>
            <div className="d-flex justify-content-center w-100">
              <Spinner animation="border" />
            </div>
          </Card>
        </Col>
      </Row>
    )
  }
}
