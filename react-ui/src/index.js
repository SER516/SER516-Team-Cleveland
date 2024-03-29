import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Project from './project';
import MetricWiki from './metricwiki/metricwiki';
import AboutUs from './aboutus/aboutus'

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />
  },
  {
    path: "/project",
    element: <Project auth="" />
  },
  {
    path: "/metricwiki",
    element: <MetricWiki auth=""/>
  },
  {
    path: "/aboutus", 
    element: <AboutUs auth=""/>
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
