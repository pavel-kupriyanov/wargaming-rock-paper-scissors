import {createStore} from "redux";

import {GAME_STATE, RESPONSE_ERROR} from "./constants";
import {
  LOGIN,
  LOGIN_SUCCESS,
  LOGIN_FAILURE,
  CLOSE,
  READY_CHECK,
  GAME_START,
  READY_SUCCESS,
  PICK,
  PICK_CONFIRM,
  PICK_SUCCESS,
  GAME_RESULT,
  GAME_WINNER,
  ADD_NOTIFICATION,
  REMOVE_NOTIFICATION,
} from "./actions";

const initialState = {
  gameState: GAME_STATE.LOGIN,
  current_round: 1,
  nickname: null,
  token: null,
  timeout: null,
  userInfo: null,
  winner: null,
  players: [],
  notifications: [],
};

export const store = createStore(reducer, initialState);

export default function reducer(state = initialState, action) {
  console.log("reducer", state, action);
  const payload = action.payload;
  switch (action.type) {
    case LOGIN:
      return {...state, nickname: payload.nickname, token: payload.token};
    case LOGIN_SUCCESS:
      return {...state, gameState: GAME_STATE.WAITING, userInfo: payload};
    case LOGIN_FAILURE:
      const nickname = action.payload === RESPONSE_ERROR.NICKNAME_USED ? null : state.nickname;
      return {...state, nickname: nickname};
    case GAME_START:
      return {...state, gameState: GAME_STATE.GAME_START, players: payload};
    case READY_CHECK:
      return {...state, gameState: GAME_STATE.READY_CHECK, timeout: payload};
    case READY_SUCCESS:
      return {...state, gameState: GAME_STATE.READY_SUCCESS};
    case PICK:
      return {...state, gameState: GAME_STATE.PICK, timeout: payload.timeout, round: payload.current_round};
    case PICK_CONFIRM:
      return {...state, players: state.players.map(x => x.nickname === state.nickname ? {...x, choice: payload} : x)};
    case PICK_SUCCESS:
      return {...state, gameState: GAME_STATE.PICK_SUCCESS};
    case GAME_RESULT:
      return {...state, gameState: GAME_STATE.RESULT, players: payload};
    case GAME_WINNER:
      return {...state, winner: payload};
    case ADD_NOTIFICATION:
      return {...state, notifications: state.notifications.concat(payload)};
    case REMOVE_NOTIFICATION:
      return {...state, notifications: state.notifications.filter(x => x.message !== payload.message)};
    case CLOSE:
      return {...initialState, notifications: state.notifications};
    default:
      return state;
  }
}

