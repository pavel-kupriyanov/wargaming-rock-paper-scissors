import React from "react";


export default class Header extends React.PureComponent {

  render() {
    const {userInfo, onLogout, onExit} = this.props;
    return (
      <React.Fragment>
        <h1>{userInfo && userInfo.nickname ? userInfo.nickname : "unknown"}</h1>
        {userInfo && <p>{userInfo.win}/{userInfo.games}</p>}
        <button onClick={onLogout}>Logout</button>
        <button onClick={onExit}>Exit</button>
      </React.Fragment>
    )
  }
}
