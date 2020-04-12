import React from "react";
import {connect} from "react-redux";
import {GAME_STATE} from "../app/constants";
import AreYouReady from "./game/AreYouReady";
import {wsReadyConfirm, close, wsPick} from "../app/ws";
import Pick from "./game/Pick";

class Game extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {

    const {gameState, players, timeout} = this.props;

    let currentComponent;
    switch (gameState) {
      case GAME_STATE.READY_CHECK:
        currentComponent = <AreYouReady timeout={timeout} onReady={wsReadyConfirm} onTimeout={close}/>;
        break;
      case GAME_STATE.READY_SUCCESS:
        currentComponent = <p>Waiting another players...</p>;
        break;
      case GAME_STATE.PICK:
        currentComponent = <Pick timeout={timeout} onPick={wsPick} onTimeout={close}/>;
        break;
      case GAME_STATE.PICK_SUCCESS:
        currentComponent = <p>Waiting another players...</p>;
        break;
      default:
        currentComponent = <h1>Unknown</h1>
    }

    return (
      <React.Fragment>
        <h1>Game</h1>
        <h3>Players:</h3>
        {players.map(player => <p key={player}>{player}</p>)}
        {currentComponent}
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
