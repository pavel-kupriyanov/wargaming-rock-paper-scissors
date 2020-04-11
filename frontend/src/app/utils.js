import {store} from './reducer';
import {CLEAR_ERROR, SHOW_ERROR} from "./actions";

export const dispatch = action => {
  store.dispatch(action);
};

export const showError = error => {
  dispatch({type: SHOW_ERROR, payload: error});
  setTimeout(() => dispatch({type: CLEAR_ERROR}), 3000);
};
