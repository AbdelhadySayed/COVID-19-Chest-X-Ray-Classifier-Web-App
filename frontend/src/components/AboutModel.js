import React from "react";
import evaluationChart from "./assets/evaluation-chart.png"; // Assuming the image is stored in a folder named 'assets'

const AboutModel = () => {
  return (
    <div className="about-page">
      <h2>About the Model</h2>
      <p>
        The model is based on a fine-tuned ResNet-50 architecture pretrained model on imageNet data. we finetuned the model on a dataset of chest X-ray images 
        10,000 images to detect COVID-19 cases with the training and validation accuracy on 500 x-ray images.
        Below is the evaluation chart showcasing the model's performance on the validation dataset on 10 epochs till now. 
        We will train the model on more epochs after that to ensure high accuracy:
      </p>
      <div className="text-center mt-4">
        <img
          src={evaluationChart}
          alt="Evaluation Chart"
          className="img-fluid"
          style={{
            maxWidth: "80%",
            height: "auto",
            border: "2px solid #000",
            borderRadius: "8px",
          }}
        />
      </div>
    </div>
  );
};

export default AboutModel;



