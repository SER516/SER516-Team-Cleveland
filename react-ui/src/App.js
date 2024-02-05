import { Button, Form, Row, Col } from "react-bootstrap";
import './App.css';

function App() {
  return (
    <div className="d-flex align-items-center justify-content-center vh-100">
      <Form style={{ width: '100%' }}>
        <Form.Group className="mb-3 col-sm-8 offset-sm-2" controlId="formUsername">
          <Form.Label>Username: </Form.Label>
          <Form.Control type="text" placeholder="Enter Username: " />
        </Form.Group>

        <Form.Group className="mb-3 col-sm-8 offset-sm-2" controlId="formPassword">
          <Form.Label>Password: </Form.Label>
          <Form.Control type="password" placeholder="Enter Password: " />
        </Form.Group>

        <Button variant="primary" type="submit" className="col-sm-1 offset-sm-6">
          Submit
        </Button>
      </Form>
    </div>
  );
}

export default App;
