import React from "react";
import {Navbar, Nav, Button, Row, Col} from "react-bootstrap";


export default class Header extends React.PureComponent {

  render() {
    const {userInfo, onLogout, onExit} = this.props;
    return (
      <Row>
        <Col>
          <Navbar bg="primary" expand="lg" variant="dark" className="shadow p-3">
            <Navbar.Brand className="mr-auto"><h3>Rock-Paper-Scissors</h3></Navbar.Brand>
            {userInfo && <Nav>
              <Nav.Item><h3 className="white">{userInfo.nickname}</h3></Nav.Item>
              <Nav.Item><h3 className="white">Win: {userInfo.win}</h3></Nav.Item>
              <Nav.Item><h3 className="white">Games: {userInfo.games}</h3></Nav.Item>
              <Nav.Item><Button onClick={onLogout} variant="outline-light">Logout</Button></Nav.Item>
              <Nav.Item><Button onClick={onExit} variant="outline-light">Exit</Button></Nav.Item>
            </Nav>}
          </Navbar>
        </Col>
      </Row>
    )
  }
}
