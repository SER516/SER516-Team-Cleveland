import React from 'react';
import axios from "axios";
import { Button, FloatingLabel, Form } from "react-bootstrap";
import { Navigate } from "react-router-dom";

export default class Login extends React.Component {
    state = {
        username: "",
        password: "",
        token: "",
        validUser: false
    }

    handleUsernameInput = (event) => {
        this.setState({ username: event.target.value });
    }

    handlePasswordChange = (event) => {
        this.setState({ password: event.target.value });
    }

    handleSubmit = (event) => {
        event.preventDefault();
        
        axios({
            method: "post",
            url: "http://localhost:8000/auth",
            data: {
                username: this.state.username,
                password: this.state.password
            },
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http:/localhost:3000"
            }
        })
        .then(res => {
            console.log(res.data);
            this.setState({ token: res.data.auth_token })
            this.setState({ validUser: true });
        })
        .catch(ex => {
            this.setState({ validUser: false });
        });
    }

    render() {
        return(
            <Form onSubmit={this.handleSubmit}>
                <FloatingLabel
                    controlId="floatingUsername"
                    label="Enter Username"
                    className="mb-3"
                >
                    <Form.Control type="text" placeholder="Enter Username" onChange={this.handleUsernameInput} />
                </FloatingLabel>

                <FloatingLabel
                    controlId="floatingPassword"
                    label="Enter Password"
                    className="mb-3"
                >
                    <Form.Control type="password" placeholder="Enter Password" onChange={this.handlePasswordChange} />
                </FloatingLabel>

                <Button variant="primary" type="submit">
                    Submit
                </Button>
                
                {this.state.validUser ? (
                    <Navigate replace to="/project" state={{ token: this.state.token }} />
                ) : null}
            </Form>
        );
    }
}