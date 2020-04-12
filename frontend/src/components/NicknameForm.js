import React from "react";
import {Card, Col, Row, Button, Form, InputGroup, FormGroup} from "react-bootstrap";

export default class NicknameForm extends React.PureComponent {

  constructor(props) {
    super(props);
    this.onNicknameChange = this.onNicknameChange.bind(this);
    this.submitNickname = this.submitNickname.bind(this);
  }

  onNicknameChange(e) {
    this.props.change(e.target.value)
  }

  submitNickname(e) {
    e.preventDefault();
    this.props.submit();
  }

  render() {
    return (
      <Row>
        <Col>
          <Card className="mx-auto nickname-card shadow p-3">
            <Form onSubmit={this.submitNickname}>
              <Form.Group>
                <Form.Label>Nickname</Form.Label>
                <Form.Control type="text" placeholder="Nickname" onChange={this.onNicknameChange}
                              value={this.props.value || ""}/>
              </Form.Group>
              <Button size="lg" type="submit" block>Connect to server</Button>
            </Form>
          </Card>
        </Col>
      </Row>
    )
  }
}
