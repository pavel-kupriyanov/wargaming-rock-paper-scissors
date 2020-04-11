import React from "react";

export default class NicknameForm extends React.PureComponent {

  constructor(props) {
    super(props);
    this.state = {
      nickname: props.nickname || ""
    };
    this.onNicknameChange = this.onNicknameChange.bind(this);
    this.submitNickname = this.submitNickname.bind(this);
  }

  onNicknameChange(e) {
    this.setState({nickname: e.target.value})
  }

  submitNickname(e) {
    e.preventDefault();
    this.props.submit(this.state.nickname);
  }

  render() {
    return (
      <form onSubmit={this.submitNickname}>
        <input name="nickname" onChange={this.onNicknameChange}/>
        <button type="submit">Submit</button>
      </form>
    )
  }
}
