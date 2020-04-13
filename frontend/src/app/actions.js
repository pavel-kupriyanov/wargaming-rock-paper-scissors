export const LOGIN = "LOGIN";
export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_FAILURE = "LOGIN_FAILURE";

export const GAME_START = "GAME_START";

export const READY_CHECK = "READY_CHECK";
export const READY_CONFIRM = "READY_CONFIRM";
export const READY_SUCCESS = "READY@SUCCESS";

export const PICK = "PICK_CHECK";
export const PICK_CONFIRM = "PICK_CONFIRM";
export const PICK_SUCCESS = "PICK_SUCCESS";

export const GAME_RESULT = "GAME_RESULT";
export const GAME_WINNER = "GAME_WINNER";

export const ADD_NOTIFICATION = "NOTIFICATION_ADD";
export const REMOVE_NOTIFICATION = "NOTIFICATION_REMOVE";

export const CLOSE = "CLOSE";

export const addNotification = (message, type) => {
  return {type: ADD_NOTIFICATION, payload: {message, type}}
};

export const removeNotification = (message, type) => {
  return {type: REMOVE_NOTIFICATION, payload: {message, type}}
};

export const login = (nickname, token) => {
  return {type: LOGIN, payload: {nickname, token}}
};

export const loginSuccess = (userInfo) => {
  return {type: LOGIN_SUCCESS, payload: userInfo}
};

export const loginFailure = (error) => {
  return {type: LOGIN_FAILURE, payload: error}
};

export const gameStart = (players) => {
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

export const pick = (timeout, current_round) => {
  return {type: PICK, payload: {timeout, current_round}}
};

export const pickConfirm = (pick) => {
  return {type: PICK_CONFIRM, payload: pick}
};

export const pickConfirmed = () => {
  return {type: PICK_SUCCESS, payload: {}}
};

export const gameResult = (players) => {
  return {type: GAME_RESULT, payload: players}
};

export const gameWinner = (winner) => {
  return {type: GAME_WINNER, payload: winner}
};

export const closeConnection = () => {
  return {type: CLOSE}
};

