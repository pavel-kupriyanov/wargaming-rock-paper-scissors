import React from "react";
import {connect} from "react-redux";
import {GAME_STATE} from "../app/constants";
import AreYouReady from "./game/AreYouReady";
import {wsReadyConfirm, close} from "../app/ws";

class Game extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {

    const {gameState, players, timeout} = this.props;

    return (
      <React.Fragment>
        <h1>Game</h1>
        <h3>Players:</h3>
        {players.map(player => <p key={player}>{player}</p>)}
        {gameState === GAME_STATE.READY_CHECK &&
        <AreYouReady timeot={timeout} onReady={wsReadyConfirm} onTimeout={close}/>}
        {gameState === GAME_STATE.READY_SUCCESS && <p>Waiting another players...</p>}
      </React.Fragment>
    )
  }

}

const mapStateToProps = state => ({
  gameState: state.gameState,
  players: state.players,
  timeout: state.timeout,
  userInfo: state.userInfo,
});

export default connect(mapStateToProps, null)(Game);
