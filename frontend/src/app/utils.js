import {store} from './reducer';
import {addNotification, removeNotification} from "./actions";
import {close} from "./ws";

export const dispatch = action => {
  store.dispatch(action);
};

export const displayNotification = (message, type) => {
  console.log(`${type}: ${message}`);
  dispatch(addNotification(message, type));
  setTimeout(() => dispatch(removeNotification(message, type)), 5000);
};

export const logout = () => {
  localStorage.setItem("nickname", "");
  localStorage.setItem("token", "");
  close();
};
