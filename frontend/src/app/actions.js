import {send} from "./ws";
import {WS_ACTION} from "./constants";

export const LOGIN_REQUEST = "LOGIN@REQUEST";
export const LOGIN_SUCCESS = "LOGIN@SUCCESS";
export const LOGIN_FAILURE = "LOGIN@FAILURE";

export const SHOW_ERROR = "SHOW_ERROR";
export const CLEAR_ERROR = "CLEAR_ERROR";

export const CLOSE = "CLOSE";


export const clearError = () => {
  return {type: CLEAR_ERROR};
};

export const showError = (error) => {
  return {type: SHOW_ERROR, payload: error}
};

export const login = (nickname, token) => {
  const payload = {nickname, token};
  send(WS_ACTION.AUTH, payload);
  return {type: LOGIN_REQUEST, payload: payload}
};

export const loginSuccess = (userInfo) => {
  console.log(userInfo);
  return {type: LOGIN_SUCCESS, payload: userInfo}
};

export const loginFailure = (error) => {
  return {type: LOGIN_FAILURE, payload: error}
};

export const closeConnection = () => {
  return {type: CLOSE}
};

