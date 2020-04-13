import React from "react";

import {connect} from "react-redux";
import {Card, Table} from "react-bootstrap";

import InfoCard from "./InfoCard";
import TimeoutModal from "./TimeoutModal";

import {CHOICES, GAME_STATE} from "../app/constants";
import {wsReadyConfirm, close, wsPick} from "../app/ws";


class Game extends React.Component {

  render() {

    const {gameState, players, timeout, current_round, winner} = this.props;

    let currentComponent, buttonsConfig;
    switch (gameState) {
      case GAME_STATE.READY_CHECK:
        buttonsConfig = [{variant: "primary", callback: wsReadyConfirm, text: "Ready!"}];
        currentComponent =
          <TimeoutModal header="Are you ready?" messageTemplate="You will be disconnected after {timeout} seconds."
                        buttonsConfig={buttonsConfig} timeout={timeout} onTimeout={close}/>;
        break;
      case GAME_STATE.PICK:
        buttonsConfig = [
          {variant: "secondary", callback: () => wsPick(CHOICES.ROCK), text: "Rock"},
          {variant: "light", callback: () => wsPick(CHOICES.PAPER), text: "Paper"},
          {variant: "info", callback: () => wsPick(CHOICES.SCISSORS), text: "Scissors"}
        ];
        currentComponent =
          <TimeoutModal header="You pick" messageTemplate="Until the end of the wait {timeout} seconds."
                        buttonsConfig={buttonsConfig} timeout={timeout} onTimeout={close}/>;
        break;
      case GAME_STATE.RESULT:
        const message = winner ? `Player ${winner} win the game!` : `Draw. The next round is about to begin!`;
        currentComponent = <InfoCard message={message}/>;
        break;
      default:
        currentComponent = <InfoCard message="Waiting another players..." spinner/>;
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
  current_round: state.current_round,
  winner: state.winner
});

export default connect(mapStateToProps, null)(Game);
