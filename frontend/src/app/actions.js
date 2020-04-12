export const LOGIN_REQUEST = "LOGIN@REQUEST";
export const LOGIN_SUCCESS = "LOGIN@SUCCESS";
export const LOGIN_FAILURE = "LOGIN@FAILURE";

export const GAME_START = "GAME@START";

export const READY_CHECK = "READY@CHECK";
export const READY_CONFIRM = "READY@CONFIRM";
export const READY_SUCCESS = "READY@SUCCESS";

export const SHOW_ERROR = "ERROR@SHOW";
export const CLEAR_ERROR = "ERROR@CLEAR";

export const CLOSE = "CLOSE";
export const UPDATE_META = "META";


export const clearError = () => {
  return {type: CLEAR_ERROR};
};

export const showError = (error) => {
  return {type: SHOW_ERROR, payload: error}
};

export const updateMeta = (meta) => {
  return {UPDATE_META, meta}
};

export const login = (nickname, token) => {
  return {type: LOGIN_REQUEST, payload: {nickname, token}}
};

export const loginSuccess = (userInfo) => {
  return {type: LOGIN_SUCCESS, payload: userInfo}
};

export const loginFailure = (error) => {
  return {type: LOGIN_FAILURE, payload: error}
};

export const gameStart = (players) => {
  console.log("game start action", players);
  return {type: GAME_START, payload: players}
};

export const readyCheck = (timeout) => {
  return {type: READY_CHECK, payload: timeout}
};

export const readyConfirm = () => {
  return {type: READY_CONFIRM, payload: {}}
};

export const readyConfirmed = () => {
  return {type: READY_SUCCESS, payload: {}}
};

export const closeConnection = () => {
  return {type: CLOSE}
};

