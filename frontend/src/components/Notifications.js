import React from "react";
import {NOTIFICATION_TYPES} from "../app/constants";

export default class Notifications extends React.PureComponent {

  render() {
    return (
      this.props.notifications.map((notification, i) => {
        return <p key={i} style={{"color": notification.type === NOTIFICATION_TYPES.ERROR ? "red" : "orange"}}>
          {notification.message}
        </p>
      })
    )
  }
}
