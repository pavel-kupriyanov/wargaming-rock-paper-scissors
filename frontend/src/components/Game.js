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

    const {gameState, players, timeout, round, winner} = this.props;

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
        <h1>Round: {round}</h1>
        <h3>Players:</h3>
        {players.map(player =>
          <p key={player.nickname} style={{color: winner === player.nickname ? "green" : ""}}>
            {player.nickname} {player.choice}
          </p>)}
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
  round: state.current_round,
  winner: state.winner
});

export default connect(mapStateToProps, null)(Game);
