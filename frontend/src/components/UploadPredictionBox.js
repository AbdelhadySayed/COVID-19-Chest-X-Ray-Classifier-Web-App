import React, { useState, useRef } from "react";

const UploadPredictionBox = ({ onPredict }) => {
  const [image, setImage] = useState(null); // Stores the uploaded/captured image
  const [prediction, setPrediction] = useState(null); // Stores the prediction result
  const [cameraMode, setCameraMode] = useState(false); // Tracks if the camera is active
  const [isPredictionEnabled, setIsPredictionEnabled] = useState(false); // Controls prediction button state
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null); // Stores the camera stream for stopping it

  // Handle file upload
  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file)); // Display the uploaded image
      setIsPredictionEnabled(true); // Enable prediction button
      setPrediction(null); // Reset previous prediction
    }
  };

  // Start camera
  const startCamera = async () => {
    setCameraMode(true);
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    videoRef.current.play();
    streamRef.current = stream; // Save the stream to stop it later
  };

  // Capture image from camera
  const captureImage = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL("image/png"); // Get image as base64
    setImage(dataUrl);
    setIsPredictionEnabled(true); // Enable prediction button
    setPrediction(null); // Reset previous prediction

    // Stop the camera after capturing the image
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }
    setCameraMode(false); // Exit camera mode
  };

  // Simulate prediction process (replace this with actual API call)
  const handlePredict = () => {
    setPrediction({
      message: "COVID-19 Detected",
    });
  };

  return (
    <div className="upload-prediction-box page-container">
      <h3>Upload or Capture an Image</h3>
      <div className="upload-buttons" style={{ display: "flex", gap: "10px" }}>
        {/* Upload Input */}
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          className="btn btn-secondary"
        />

        {/* Camera Capture Button */}
        {!cameraMode && (
          <button className="btn btn-primary" onClick={startCamera}>
            Capture Using Camera
          </button>
        )}
      </div>

      {/* Camera View */}
      {cameraMode && (
        <div style={{ marginTop: "10px" }}>
          <video ref={videoRef} style={{ width: "100%", border: "1px solid #ddd" }} />
          <button
            className="btn btn-success mt-3"
            onClick={captureImage}
            style={{ display: "block", margin: "10px auto" }}
          >
            Capture Image
          </button>
          <canvas ref={canvasRef} style={{ display: "none" }} width={640} height={480}></canvas>
        </div>
      )}

      {/* Display the selected or captured image */}
      {image && (
        <div style={{ marginTop: "20px", textAlign: "center" }}>
          <h4>Selected Image</h4>
          <img
            src={image}
            alt="Uploaded or Captured"
            style={{ maxWidth: "100%", borderRadius: "8px", border: "1px solid #ddd" }}
          />
        </div>
      )}

      {/* Prediction Section */}
      <div style={{ marginTop: "20px", textAlign: "center" }}>
        <button
          className="btn btn-primary"
          onClick={handlePredict}
          disabled={!isPredictionEnabled} // Disable until image is uploaded or captured
        >
          Get Prediction
        </button>

        {/* Show Prediction Result */}
        {prediction && (
          <div style={{ marginTop: "15px" }}>
            <h4>Prediction Result</h4>
            <p className="text-danger">{prediction.message}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPredictionBox;
