import {send} from "./ws";

export const LOGIN_REQUEST = "LOGIN@REQUEST";
export const LOGIN_SUCCESS = "LOGIN@SUCCESS";
export const LOGIN_FAILURE = "LOGIN@FAILURE";

export const SHOW_ERROR = "SHOW_ERROR";
export const CLEAR_ERROR = "CLEAR_ERROR";


export const clearError = () => {
  return {type: CLEAR_ERROR};
};

export const showError = (error) => {
  return {type: SHOW_ERROR, payload: error}
};

export const login = (nickname, token) => {
  send("auth", {"nickname": nickname, "token": token});
  return {type: LOGIN_REQUEST}
};

export const loginSuccess = () => {
  return {type: LOGIN_SUCCESS}
};

export const loginFailure = (error) => {
  return {type: LOGIN_FAILURE, payload: error}
};

