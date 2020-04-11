import {createStore} from "redux";

import {GAME_STATE, RESPONSE_ERROR} from "./constants";
import {LOGIN_REQUEST, LOGIN_SUCCESS, LOGIN_FAILURE, SHOW_ERROR, CLEAR_ERROR} from "./actions";

const initialState = {
  nickname: null,
  token: null,
  gameState: GAME_STATE.LOGIN,
  loading: false,
  error: null
};

export const store = createStore(reducer, initialState);

export default function reducer(state = initialState, action) {
  console.log("reducer", state, action);
  switch (action.type) {
    case LOGIN_REQUEST:
      return {...state, loading: true};
    case LOGIN_SUCCESS:
      return {...state, loading: false, gameState: GAME_STATE.WAITING};
    case LOGIN_FAILURE:
      if (action.payload === RESPONSE_ERROR.NICKNAME_USED) state.nickname = null;
      return {...state, loading: false};
    case SHOW_ERROR:
      return {...state, error: action.payload};
    case CLEAR_ERROR:
      return {...state, error: null};
    default:
      return state;
  }
}
