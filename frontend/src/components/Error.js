import React from "react";

export default class Error extends React.PureComponent {

  render() {
    return (
      <h1 style={{color: "red"}}>{this.props.error}</h1>
    )
  }

}
