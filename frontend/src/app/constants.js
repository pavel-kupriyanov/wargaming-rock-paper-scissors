export const GAME_STATE = {
  LOGIN: "LOGIN",
  WAITING: "WAITING",
  READY_CHECK: "READY_CHECK",
  WAITING_PICKS: "WAITING_PICKS",
  RESULT: "RESULT",
  GAME_END: "GAME_END",
};


export const WS_ACTION = {
  AUTH: "auth",
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
