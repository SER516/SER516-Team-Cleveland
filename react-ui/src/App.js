import React from 'react';
import { Stack } from "react-bootstrap";
import './App.css';
import Login from './login/Login';

function App() {
  return (
    <Stack gap={4} className="col-md-5 mx-auto">
      <Login />
    </Stack>
  );
}

export default App;
