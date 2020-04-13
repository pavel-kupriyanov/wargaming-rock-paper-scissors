import {dispatch, displayNotification} from "./utils";
import {
  loginFailure,
  loginSuccess,
  readyCheck,
  closeConnection,
  gameStart,
  readyConfirmed,
  login,
  readyConfirm,
  pick,
  pickConfirm,
  pickConfirmed,
  gameResult,
  gameWinner
} from "./actions";
import {ERROR_CODES, NOTIFICATION_TYPES, WS_ACTION} from "./constants";


let ws = null;

export const receive = message => {
  const {action, payload, meta} = JSON.parse(message.data);
  switch (action) {
    case WS_ACTION.AUTH:
      if (payload.status) {
        dispatch(loginSuccess(meta.user));
        localStorage.setItem("nickname", meta.user.nickname);
        localStorage.setItem("token", meta.user.token);
      } else {
        dispatch(loginFailure(ERROR_CODES[payload.error.code]))
      }
      break;
    case WS_ACTION.GAME_START:
      dispatch(gameStart(payload.players));
      break;
    case WS_ACTION.READY_CHECK:
      if (payload.timeout) {
        dispatch(readyCheck(payload.timeout));
      } else {
        dispatch(readyConfirmed())
      }
      break;
    case WS_ACTION.PICK:
      if (payload.timeout) {
        dispatch(pick(payload.timeout, payload.current_round));
      } else {
        dispatch(pickConfirmed())
      }
      break;
    case WS_ACTION.GAME_RESULT:
      dispatch(gameResult(payload.choices));
      if (payload.winner) {
        dispatch(gameWinner(payload.winner));
      }
      break;
    case WS_ACTION.DISCONNECT:
      const message = payload.player ? `${payload.player} disconnected.` : `Session closed: ${payload.reason.message}`;
      displayNotification(message, NOTIFICATION_TYPES.MESSAGE);
      break;
    default:
      break
  }
  if (payload.error) {
    displayNotification(ERROR_CODES[payload.error.code], NOTIFICATION_TYPES.ERROR)
  }
};

export const initWs = async () => {
  if (ws) {
    return;
  }
  return new Promise((resolve, reject) => {
    try {
      ws = new WebSocket(process.env.REACT_APP_SERVER_URL);
    } catch (e) {
      reject(e);
    }
    ws.onmessage = receive;
    ws.onclose = () => {
      ws = null;
      dispatch(closeConnection())
    };
    ws.onerror = () => {
      displayNotification("Server connection error", NOTIFICATION_TYPES.ERROR);
    };
    ws.onopen = () => {
      resolve();
    };
  })
};

export const wsLogin = (nickname, token) => {
  send(WS_ACTION.AUTH, {nickname, token});
  dispatch(login(nickname, token))
};

export const wsReadyConfirm = () => {
  send(WS_ACTION.READY_CHECK, {});
  dispatch(readyConfirm());
};

export const wsPick = (pick) => {
  send(WS_ACTION.PICK, {pick});
  dispatch(pickConfirm(pick));
};


export const send = (action, payload) => {
  ws.send(JSON.stringify({action, payload}));
};

export const close = () => {
  ws.close();
};
