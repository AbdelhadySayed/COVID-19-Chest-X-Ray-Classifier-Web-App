import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import NavigationMenu from "./components/NavigationMenu";
import UploadPredictionBox from "./components/UploadPredictionBox";
import AboutModel from "./components/AboutModel";
import ContactUs from "./components/ContactUs";
import FutureImprovements from "./components/FutureImprovements";
import Footer from "./components/Footer";
import "./styles.css";

const App = () => {
  return (
    <Router>
      <div id="app-container">
        <NavigationMenu />
        <div id="main-content">
          <Routes>
            <Route path="/" element={<UploadPredictionBox/>} />
            <Route path="/about" element={<AboutModel />} />
            <Route path="/contact" element={<ContactUs />} />
            <Route path="/future" element={<FutureImprovements />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
};

export default App;

