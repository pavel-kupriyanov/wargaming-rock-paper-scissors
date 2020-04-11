import {dispatch, showError} from "./utils";
import {loginFailure, loginSuccess} from "./actions";
import {RESPONSE_ACTION} from "./constants";


let ws = null;

export const disconnect = () => {
  console.log("disconnect")
};

export const error = () => {
  console.log("err")
};

export const processMessage = message => {
  const {action, payload} = JSON.parse(message.data);
  switch (action) {
    case RESPONSE_ACTION.AUTH:
      if (payload.status) {
        dispatch(loginSuccess())
      } else {
        dispatch(loginFailure(payload.error))
      }
      break;
    default:
      break
  }
  if (payload.error) {
    showError(payload.error)
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
    ws.onclose = disconnect;
    ws.onerror = error;
    ws.onmessage = processMessage;
    ws.onopen = () => {
      resolve(ws);
    };
  })
};

export const send = (action, payload) => {
  console.log(ws);
  ws.send(JSON.stringify({action, payload}));
};
