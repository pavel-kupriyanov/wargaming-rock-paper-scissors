import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {connect} from "react-redux";
import {Container, Row, Col} from "react-bootstrap";

import {GAME_STATE, NOTIFICATION_TYPES} from "./app/constants";
import Game from "./components/Game";
import NicknameForm from "./components/NicknameForm";
import {getWs, wsLogin, close} from "./app/ws";
import {displayNotification, logout} from "./app/utils";
import Waiting from "./components/Waiting";
import Header from "./components/Header";
import Notifications from "./components/Notifications";

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
    getWs()
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
        currentComponent = <Waiting/>;
        break;
      default:
        currentComponent = <Game/>
    }
    return (
      <Container fluid className="no-padding">
        <Header userInfo={userInfo} onExit={close} onLogout={logout}/>
        {notifications && <Notifications notifications={notifications}/>}
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

