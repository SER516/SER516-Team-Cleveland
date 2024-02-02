<<<<<<< HEAD
import { Button, Form, Row, Col } from "react-bootstrap";
import './App.css';

function App() {
  return (
    <div className="d-flex align-items-center justify-content-center vh-100">
      <Form style={{ width: '100%' }}>
        <Form.Group className="mb-3 col-sm-8 offset-sm-2" controlId="formUsername">
          <Form.Label>Username: </Form.Label>
          <Form.Control type="text" placeholder="Enter Username" />
        </Form.Group>

        <Form.Group className="mb-3 col-sm-8 offset-sm-2" controlId="formPassword">
          <Form.Label>Password: </Form.Label>
          <Form.Control type="password" placeholder="Enter Password" />
        </Form.Group>

        <Button variant="primary" type="submit" className="col-sm-1 offset-sm-6">
          Submit
        </Button>
      </Form>
=======
import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import ProjectSelection from './ProjectSelection';

function App() {
  const [showProjectSelection, setShowProjectSelection] = useState(false);

  return (
    <div className="App">
      {showProjectSelection ? (
        <ProjectSelection />
      ) : (
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          <button
            onClick={() => setShowProjectSelection(true)}
          >
            Go to Project Selection
          </button>
        </header>
      )}
>>>>>>> 778614a (US12Task42 Initial version of ProjectSelection.js and ProjectSelection.css)
    </div>
  );
}

export default App;
