export const LOGIN_REQUEST = "LOGIN@REQUEST";
export const LOGIN_SUCCESS = "LOGIN@SUCCESS";
export const LOGIN_FAILURE = "LOGIN@FAILURE";

export const GAME_START = "GAME@START";

export const READY_CHECK = "READY@CHECK";
export const READY_CONFIRM = "READY@CONFIRM";
export const READY_SUCCESS = "READY@SUCCESS";

export const PICK = "PICK@CHECK";
export const PICK_CONFIRM = "PICK@CONFIRM";
export const PICK_SUCCESS = "PICK@SUCCESS";

export const ADD_NOTIFICATION = "NOTIFICATION@ADD";
export const REMOVE_NOTIFICATION = "NOTIFICATION@REMOVE";

export const CLOSE = "CLOSE";
export const UPDATE_META = "META";

export const addNotification = (message, type) => {
  return {type: ADD_NOTIFICATION, payload: {message, type}}
};

export const removeNotification = (message, type) => {
  return {type: REMOVE_NOTIFICATION, payload: {message, type}}
};

export const updateMeta = (meta) => {
  return {type: UPDATE_META, payload: meta}
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

export const pick = (timeout) => {
  return {type: PICK, payload: timeout}
};

export const pickConfirm = (pick) => {
  return {type: PICK_CONFIRM, payload: pick}
};

export const pickConfirmed = () => {
  return {type: PICK_SUCCESS, payload: {}}
};


export const closeConnection = () => {
  return {type: CLOSE}
};

