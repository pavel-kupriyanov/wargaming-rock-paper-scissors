import React from "react";

import {logout} from "../app/utils";

export default class Header extends React.PureComponent {

  render() {
    const {userInfo} = this.props;
    return (
      <React.Fragment>
        <h1>{userInfo && userInfo.nickname ? userInfo.nickname : "unknown"}</h1>
        {userInfo && <p>{userInfo.win}/{userInfo.games}</p>}
        <button onClick={logout}>Logout</button>
      </React.Fragment>

    )
  }
}
