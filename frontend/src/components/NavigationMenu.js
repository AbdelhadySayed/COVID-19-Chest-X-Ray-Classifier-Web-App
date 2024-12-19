import React from 'react';
import { Link } from 'react-router-dom';

const NavigationMenu = () => {
  return (
    <nav className="navbar navbar-expand-lg  custom-nav">
      <div className="container">
        {/* Add logo or title if needed */}
        <Link className="navbar-brand" to="/">COVID-19 X-ray Classifier</Link>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">Prediction</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/about">About the Model</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/future">Future Improvements</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/contact">Contact Us</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default NavigationMenu;
