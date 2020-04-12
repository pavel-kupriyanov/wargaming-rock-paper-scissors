import React from "react";
import {NOTIFICATION_TYPES} from "../app/constants";
import {Alert} from "react-bootstrap";

export default class Notifications extends React.PureComponent {

  render() {
    return (
      this.props.notifications.map((notification, i) => {
        return <Alert key={i} variant={notification.type === NOTIFICATION_TYPES.ERROR ? "warning" : "info"}>
          {notification.message}
        </Alert>
      })
    )
  }
}
