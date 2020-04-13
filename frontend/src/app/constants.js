export const GAME_STATE = {
  LOGIN: "LOGIN",
  WAITING: "WAITING",
  GAME_START: "GAME_START",
  READY_CHECK: "READY_CHECK",
  READY_SUCCESS: "READY_SUCCESS",
  PICK: "WAITING_PICKS",
  PICK_SUCCESS: "PICK_SUCCESS",
  RESULT: "RESULT",
};

export const WS_ACTION = {
  AUTH: "auth",
  GAME_START: "game_start",
  READY_CHECK: "ready_check",
  PICK: "pick",
  GAME_RESULT: "game_result",
  DISCONNECT: "disconnect",
};

export const RESPONSE_ERROR = {
  ALREADY_CONNECTED: "You already connected now. Close other tabs and try again.",
  NICKNAME_USED: "This nickname already used.",
};

export const ERROR_CODES = {
  401: RESPONSE_ERROR.NICKNAME_USED,
  403: RESPONSE_ERROR.ALREADY_CONNECTED
};

export const CHOICES = {
  ROCK: "Rock",
  PAPER: "Paper",
  SCISSORS: "Scissors",
};

export const NOTIFICATION_TYPES = {
  ERROR: "Error",
  MESSAGE: "Message"
};
