import {createStore} from "redux";

import {GAME_STATE, RESPONSE_ERROR} from "./constants";
import {
  LOGIN_REQUEST,
  LOGIN_SUCCESS,
  LOGIN_FAILURE,
  SHOW_ERROR,
  CLEAR_ERROR,
  CLOSE,
  READY_CHECK,
  GAME_START,
  READY_SUCCESS,
  READY_CONFIRM, UPDATE_META, PICK, PICK_CONFIRM, PICK_SUCCESS
} from "./actions";

const initialState = {
  gameState: GAME_STATE.LOGIN,
  nickname: null,
  token: null,
  timeout: null,
  loading: false,
  error: null,
  userInfo: null,
  players: [],
  meta: {}
};

export const store = createStore(reducer, initialState);

export default function reducer(state = initialState, action) {
  console.log("reducer", state, action);
  const payload = action.payload;
  switch (action.type) {
    case LOGIN_REQUEST:
      return {...state, loading: true, nickname: payload.nickname, token: payload.token};
    case LOGIN_SUCCESS:
      return {...state, loading: false, gameState: GAME_STATE.WAITING, userInfo: payload};
    case LOGIN_FAILURE:
      if (action.payload === RESPONSE_ERROR.NICKNAME_USED) state.nickname = null;
      return {...state, loading: false};
    case GAME_START:
      return {...state, gameState: GAME_STATE.GAME_START, players: payload};
    case READY_CHECK:
      return {...state, gameState: GAME_STATE.READY_CHECK, timeout: payload};
    case READY_CONFIRM:
      return state;
    case READY_SUCCESS:
      return {...state, gameState: GAME_STATE.READY_SUCCESS};
    case PICK:
      return {...state, gameState: GAME_STATE.PICK, timeout: payload};
    case PICK_CONFIRM:
      return state;
    case PICK_SUCCESS:
      return {...state, gameState: GAME_STATE.PICK_SUCCESS};
    case SHOW_ERROR:
      return {...state, error: action.payload};
    case CLEAR_ERROR:
      return {...state, error: null};
    case CLOSE:
      return initialState;
    case UPDATE_META:
      return {...state, meta: payload};
    default:
      return state;
  }
}

