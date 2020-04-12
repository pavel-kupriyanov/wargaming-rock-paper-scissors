import React from "react";
import {connect} from "react-redux";
import {GAME_STATE} from "../app/constants";
import AreYouReady from "./game/AreYouReady";
import {wsReadyConfirm, close, wsPick} from "../app/ws";
import Pick from "./game/Pick";
import Waiting from "./game/Waiting";
import {Card, Table} from "react-bootstrap";
import Info from "./game/Info";

class Game extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {

    const {gameState, players, timeout, current_round, winner} = this.props;

    let currentComponent;
    switch (gameState) {
      case GAME_STATE.READY_CHECK:
        currentComponent = <AreYouReady timeout={timeout} onReady={wsReadyConfirm} onTimeout={close}/>;
        break;
      case GAME_STATE.READY_SUCCESS:
        currentComponent = <Waiting/>;
        break;
      case GAME_STATE.PICK:
        currentComponent = <Pick timeout={timeout} onPick={wsPick} onTimeout={close}/>;
        break;
      case GAME_STATE.PICK_SUCCESS:
        currentComponent = <Waiting/>;
        break;
      case GAME_STATE.RESULT:
        const message = winner ? `Player ${winner} win the game!` : `Draw. The next round is about to begin!`;
        currentComponent = <Info message={message}/>;
        break;
    }

    return (
      <React.Fragment>
        <Card className="game-card shadow p-3">
          <Card.Title>Round: {current_round}</Card.Title>
          <hr/>
          <Card.Body>
            <Table striped bordered hover>
              <thead>
              <tr>
                <th>Nickname</th>
                <th>Pick</th>
              </tr>
              </thead>
              <tbody>
              {players.map((player) =>
                <tr key={player.nickname} style={{color: winner === player.nickname ? "green" : ""}}>
                  <td>{player.nickname}</td>
                  <td>{player.choice}</td>
                </tr>)}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
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
  current_round: state.current_round,
  winner: state.winner
});

export default connect(mapStateToProps, null)(Game);
