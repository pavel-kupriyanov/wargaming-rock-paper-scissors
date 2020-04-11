import React from 'react';
import './App.css';
import {Provider, connect} from "react-redux";
import {createStore, bindActionCreators} from "redux";

import reducer from "./app/reducer";
import {LOGIN, WAITING, GAME, GAME_STATE} from "./app/constants";
import Game from "./components/Game";
import NicknameForm from "./components/NicknameForm";
import {getWs} from "./app/ws";
import {login} from "./app/actions";
import Waiting from "./components/Waiting";


class App extends React.Component {

  constructor() {
    super();
    this.connectToWs = this.connectToWs.bind(this);
  }

  async connectToWs(nickname, token = null) {
    getWs().then(_ => {
      console.log("inited", nickname, token);
      this.props.login(nickname, token);
    }).catch(err => {
      console.log(err);
    });
  }

  render() {
    const {gameState, nickname} = this.props;
    let currentComponent;
    console.log(gameState);
    switch (gameState) {
      case GAME_STATE.LOGIN:
        currentComponent = <NicknameForm submit={this.connectToWs} nickname={nickname}/>;
        break;
      case GAME_STATE.WAITING:
        currentComponent = <Waiting/>;
        break;
      default:
        currentComponent = <h1>Unknown</h1>
    }
    return (
      <React.Fragment>
        {currentComponent}
      </React.Fragment>
    )
  }
}

const mapStateToProps = state => ({nickname: state.nickname, token: state.token, gameState: state.gameState});
const mapDispatchToProps = dispatch => {
  return bindActionCreators({login}, dispatch);
};

export default connect(mapStateToProps, mapDispatchToProps)(App);

