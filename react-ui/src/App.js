import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="mainbody">
        <h1 align="left">Login Page: </h1><br/>
        <h5 align="left">Email address: </h5>
        <input type="email" class="form-control" id="Input1" aria-describedby="emailHelp" placeholder="Enter email"></input><br/>
        <h5 align="left">Password: </h5>
        <input type="password" class="form-control" id="Input2" placeholder="Password"></input><br/>
        <button type="button" className="btn btn-primary" id="Submit1">Submit</button>
      </div>
    </div>
  );
}

export default App;
