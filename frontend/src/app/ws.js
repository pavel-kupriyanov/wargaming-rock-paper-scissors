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
  updateMeta,
  pick,
  pickConfirm,
  pickConfirmed
} from "./actions";
import {NOTIFICATION_TYPES, WS_ACTION} from "./constants";


let ws = null;

export const receive = message => {
  const {action, payload, meta} = JSON.parse(message.data);
  console.log(action, payload, meta);
  switch (action) {
    case WS_ACTION.AUTH:
      if (payload.status) {
        dispatch(loginSuccess(meta.user));
        localStorage.setItem("nickname", meta.user.nickname);
        localStorage.setItem("token", meta.user.token);
      } else {
        dispatch(loginFailure(payload.error))
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
        dispatch(pick(payload.timeout));
      } else {
        dispatch(pickConfirmed())
      }
      break;
    case WS_ACTION.DISCONNECT:
      const message = payload.player ? `${payload.player} disconnected.` : `Session closed: ${payload.reason}`;
      displayNotification(message, NOTIFICATION_TYPES.MESSAGE);
      break;
    default:
      break
  }
  if (payload.error) {
    displayNotification(payload.error, NOTIFICATION_TYPES.ERROR)
  }
  if (meta) {
    dispatch(updateMeta(meta))
  }
};

export const getWs = async () => {
  if (ws) {
    return ws
  }
  return new Promise((resolve, reject) => {
    try {
      ws = new WebSocket(process.env.REACT_APP_SERVER_URL);
    } catch (e) {
      reject(e);
    }
    ws.onmessage = receive;
    ws.onclose = () => {
      console.log("disconnect");
      ws = null;
      dispatch(closeConnection())
    };
    ws.onerror = (err) => {
      console.log("err", err)
    };
    ws.onopen = () => {
      resolve(ws);
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
  console.log(action, payload);
  ws.send(JSON.stringify({action, payload}));
};

export const close = () => {
  ws.close();
};
