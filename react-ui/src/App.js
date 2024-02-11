import React from 'react';
import { Stack } from "react-bootstrap";
import './App.css';
import Login from './login/Login';

function App() {
  return (
    <div className='background' style={{ height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ height: '80%', width: '30%', maxHeight: '80vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Stack gap={4} style={{ borderRadius: '30px', overflow: 'hidden' }}>
          <Login />
        </Stack>
      </div>
    </div>
  );
}

export default App;
