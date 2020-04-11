import React from 'react';
import './App.css';
import {connect} from "react-redux";
import {bindActionCreators} from "redux";

import {GAME_STATE} from "./app/constants";
import Game from "./components/Game";
import Error from "./components/Error";
import NicknameForm from "./components/NicknameForm";
import {getWs} from "./app/ws";
import {displayError} from "./app/utils";
import {login} from "./app/actions";
import Waiting from "./components/Waiting";
import Header from "./components/Header";


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
        this.props.login(this.state.nickname, this.state.token);
      })
      .catch(err => {
        displayError(err);
      });
  }

  onNicknameChange(nickname) {
    this.setState({nickname: nickname});
  }

  render() {
    const {gameState, error, userInfo} = this.props;
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
        currentComponent = <h1>Unknown</h1>
    }
    return (
      <React.Fragment>
        <Header userInfo={userInfo}/>
        {currentComponent}
        {error && <Error error={error}/>}
      </React.Fragment>
    )
  }
}

const mapStateToProps = state => ({
  nickname: state.nickname,
  token: state.token,
  gameState: state.gameState,
  userInfo: state.userInfo,
  error: state.error
});
const mapDispatchToProps = dispatch => {
  return bindActionCreators({login}, dispatch);
};

export default connect(mapStateToProps, mapDispatchToProps)(App);

