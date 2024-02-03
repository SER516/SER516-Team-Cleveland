<<<<<<< HEAD
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
=======
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
>>>>>>> 4042ed0 (US12Task42 Modified HTML based code to React BootStrap based code and chaged the filename)
import logo from './logo.svg';
import './App.css';
import ProjectSlug from './ProjectSlug';
import Button from 'react-bootstrap/Button';

function App() {
  return (
    <Router>
      <div className="App">
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
          <Link to="/ProjectSlug">
            <Button variant="info">Go to Project Slug</Button>
          </Link>
        </header>
<<<<<<< HEAD
      )}
>>>>>>> 778614a (US12Task42 Initial version of ProjectSelection.js and ProjectSelection.css)
    </div>
=======
        <Routes>
          <Route path="/ProjectSlug" element={<ProjectSlug />} />
        </Routes>
      </div>
    </Router>
>>>>>>> 4042ed0 (US12Task42 Modified HTML based code to React BootStrap based code and chaged the filename)
  );
}

export default App;