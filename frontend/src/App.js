import React from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import {connect} from "react-redux";
import {Container, Row, Col, Navbar, Nav, Button, Alert} from "react-bootstrap";

import Game from "./components/Game";
import NicknameForm from "./components/NicknameForm";
import InfoCard from "./components/InfoCard";

import {initWs, wsLogin, close} from "./app/ws";
import {displayNotification, logout} from "./app/utils";
import {GAME_STATE, NOTIFICATION_TYPES} from "./app/constants";

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      nickname: props.nickname,
      token: props.token
    };
    this.connectToWs = this.connectToWs.bind(this);
    this.onNicknameChange = this.onNicknameChange.bind(this);
  }

  componentDidMount() {
    const nickname = localStorage.getItem("nickname");
    const token = localStorage.getItem("token");
    const update = {};
    if (nickname) {
      update.nickname = nickname
    }
    if (token) {
      update.token = token
    }
    this.setState(update)
  }

  async connectToWs() {
    initWs()
      .then(_ => {
        wsLogin(this.state.nickname, this.state.token);
      })
      .catch(err => {
        displayNotification(err, NOTIFICATION_TYPES.ERROR);
      });
  }

  onNicknameChange(nickname) {
    this.setState({nickname: nickname});
  }

  render() {
    const {gameState, userInfo, notifications} = this.props;
    let currentComponent;
    switch (gameState) {
      case GAME_STATE.LOGIN:
        currentComponent =
          <NicknameForm submit={this.connectToWs} change={this.onNicknameChange} value={this.state.nickname}/>;
        break;
      case GAME_STATE.WAITING:
        currentComponent = <InfoCard message="Finding opponents..." sm spinner/>;
        break;
      default:
        currentComponent = <Game/>
    }
    return (
      <Container fluid className="no-padding">
        <Row>
          <Col>
            <Navbar bg="primary" expand="lg" variant="dark" className="shadow p-3">
              <Navbar.Brand className="mr-auto"><h3>Rock-Paper-Scissors</h3></Navbar.Brand>
              {userInfo && <Nav>
                <Nav.Item><h3 className="white">{userInfo.nickname}</h3></Nav.Item>
                <Nav.Item><h3 className="white">Win: {userInfo.win}</h3></Nav.Item>
                <Nav.Item><h3 className="white">Games: {userInfo.games}</h3></Nav.Item>
                <Nav.Item><Button onClick={logout} variant="outline-light">Logout</Button></Nav.Item>
                <Nav.Item><Button onClick={close} variant="outline-light">Exit</Button></Nav.Item>
              </Nav>}
            </Navbar>
          </Col>
        </Row>
        {notifications.map((notification, i) => {
          return <Alert key={i} variant={notification.type === NOTIFICATION_TYPES.ERROR ? "warning" : "info"}>
            {notification.message}
          </Alert>
        })}
        {currentComponent}
      </Container>
    )
  }
}

const mapStateToProps = state => ({
  nickname: state.nickname,
  token: state.token,
  gameState: state.gameState,
  userInfo: state.userInfo,
  error: state.error,
  timeout: state.timeout,
  notifications: state.notifications
});

export default connect(mapStateToProps, null)(App);

