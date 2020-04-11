import {store} from './reducer';
import {showError, clearError} from "./actions";
import {close} from "./ws";

export const dispatch = action => {
  store.dispatch(action);
};

export const displayError = error => {
  console.log(error);
  dispatch(showError(error));
  setTimeout(() => dispatch(clearError()), 3000);
};

export const logout = () => {
  localStorage.clear();
  close();
};
