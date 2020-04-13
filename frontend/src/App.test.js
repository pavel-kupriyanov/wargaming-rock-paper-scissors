import React from 'react';
import {Provider} from "react-redux";
import {unmountComponentAtNode, render} from "react-dom";
import configureStore from 'redux-mock-store'
import {act} from "react-dom/test-utils";

import App from './App';
import {GAME_STATE} from "./app/constants";

let container, store, initialState;
const mockStore = configureStore();

beforeEach(() => {
  initialState = {gameState: GAME_STATE.LOGIN, players: [], notifications: []};
  store = mockStore(() => initialState);
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});


it("renders with game state LOGIN", () => {
  act(() => {
    render(<Provider store={store}><App/></Provider>, container);
  });
  expect(container.textContent).toEqual(expect.stringContaining("Rock-Paper-Scissors"));
  expect(container.textContent).toEqual(expect.stringContaining("Nickname"));
  expect(container.textContent).toEqual(expect.not.stringContaining("Player"));
});

it("renders with game state WAITING", () => {
  initialState = {...initialState, gameState: GAME_STATE.WAITING};
  store.dispatch({type: "TYPE"});
  act(() => {
    render(<Provider store={store}><App/></Provider>, container);
  });
  expect(container.textContent).toEqual(expect.stringContaining("Finding"));
  expect(container.textContent).toEqual(expect.not.stringContaining("Nickname"));
});


it("renders with game state READY_CHECK", () => {
  initialState = {...initialState, gameState: GAME_STATE.READY_CHECK, timeout: 10};
  store.dispatch({type: "TYPE"});
  act(() => {
    render(<Provider store={store}><App/></Provider>, container);
  });
  expect(document.body.textContent).toEqual(expect.stringContaining("Are you ready?"));
  expect(document.body.textContent).toEqual(expect.stringContaining("Ready!"));
});

it("renders with game state PICK", () => {
  initialState = {...initialState, gameState: GAME_STATE.PICK, timeout: 10};
  store.dispatch({type: "TYPE"});
  act(() => {
    render(<Provider store={store}><App/></Provider>, container);
  });
  expect(document.body.textContent).toEqual(expect.stringContaining("You pick"));
});

it("renders with game state RESULT", () => {
  initialState = {...initialState, gameState: GAME_STATE.RESULT, winner: "Jonny"};
  store.dispatch({type: "TYPE"});
  act(() => {
    render(<Provider store={store}><App/></Provider>, container);
  });
  expect(document.body.textContent).toEqual(expect.stringContaining("Jonny"));
  expect(document.body.textContent).toEqual(expect.stringContaining("game!"));
});

it("renders with game state READY_SUCCESS", () => {
  initialState = {...initialState, gameState: GAME_STATE.READY_SUCCESS};
  store.dispatch({type: "TYPE"});
  act(() => {
    render(<Provider store={store}><App/></Provider>, container);
  });
  expect(document.body.textContent).toEqual(expect.stringContaining("Waiting"));
});

it("renders with game state PICK_SUCCESS", () => {
  initialState = {...initialState, gameState: GAME_STATE.READY_SUCCESS};
  store.dispatch({type: "TYPE"});
  act(() => {
    render(<Provider store={store}><App/></Provider>, container);
  });
  expect(document.body.textContent).toEqual(expect.stringContaining("Waiting"));
});
