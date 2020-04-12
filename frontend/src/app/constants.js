export const GAME_STATE = {
  LOGIN: "LOGIN",
  WAITING: "WAITING",
  GAME_START: "GAME_START",
  READY_CHECK: "READY_CHECK",
  READY_SUCCESS: "READY_SUCCESS",
  PICK: "WAITING_PICKS",
  PICK_SUCCESS: "PICK_SUCCESS",
  RESULT: "RESULT",
  GAME_END: "GAME_END",
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
  INVALID_FORMAT: "Invalid format",
  ALREADY_CONNECTED: "User already connected now",
  NICKNAME_USED: "Nickname already used",
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
