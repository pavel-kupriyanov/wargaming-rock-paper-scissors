import React from "react";

export default class NicknameForm extends React.PureComponent {

  constructor(props) {
    super(props);
    this.onNicknameChange = this.onNicknameChange.bind(this);
    this.submitNickname = this.submitNickname.bind(this);
  }

  onNicknameChange(e) {
    this.props.change(e.target.value)
  }

  submitNickname(e) {
    e.preventDefault();
    this.props.submit();
  }

  render() {
    return (
      <form onSubmit={this.submitNickname}>
        <input name="nickname" onChange={this.onNicknameChange} value={this.props.value || ""}/>
        <button type="submit">Submit</button>
      </form>
    )
  }
}
