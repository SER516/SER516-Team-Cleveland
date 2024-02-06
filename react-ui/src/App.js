import React, { useState } from 'react';
import { Button, Form } from "react-bootstrap";
import './App.css';
import ProjectSlug from './ProjectSlug';

function App() {
  const [showProjectSlug, setShowProjectSlug] = useState(false);

  return (
    <div className="d-flex align-items-center justify-content-center vh-100">
      {showProjectSlug ? (
        <ProjectSlug />
      ) : (
        <Form style={{ width: '100%' }}>
          <Form.Group className="mb-3 col-sm-8 offset-sm-2" controlId="formUsername">
            <Form.Label>Username: </Form.Label>
            <Form.Control type="text" placeholder="Enter Username" />
          </Form.Group>

          <Form.Group className="mb-3 col-sm-8 offset-sm-2" controlId="formPassword">
            <Form.Label>Password: </Form.Label>
            <Form.Control type="password" placeholder="Enter Password" />
          </Form.Group>

          <Button variant="info" className="SubmitButton" onClick={() => setShowProjectSlug(true)}>Submit</Button>
        </Form>
          )}
      </div>
  );
}

export default App;
