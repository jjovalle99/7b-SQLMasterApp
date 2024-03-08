# [7BSQL Master - Mistral](http://ec2-3-91-221-46.compute-1.amazonaws.com:7860/) 🚀 

Welcome to the 7BSQL Master, your intelligent assistant for transforming natural language questions into precise SQL queries. This application is powered by the Mistral7B version, fine-tuned for NL2SQL.

## Features

- Converts natural language questions into SQL queries
- Powered by the Mistral7B model, fine-tuned for NL2SQL

## Technical Details

- **Model**: Mistral7B version, fine-tuned for NL2SQL. Check out the repo -> https://github.com/jjovalle99/7b-SQLMaster-FineTune
- **Model Deployment**: The model is hosted on an AWS SageMaker endpoint powered by an `ml.g5.2xlarge` instance (NVIDIA A10G).
- **App Deployment**: The app is hosted on a `t3.xlarge` EC2 instance.
- **App Construction**: The app was built using **Streamlit** and **LlamaIndex**.

## Code Walkthrough

| Component         | Link                                                                                                                       |
|-------------------|---------------------------------------------------------------------------------------------------------------------------- |
| Application       | [app.py](https://github.com/jjovalle99/7b-SQLMasterApp/blob/1fc7bc62bff8ce550eed8d7542fc694a9da585ed/app.py)               |
| Model Deployment  | [deploy.py](https://github.com/jjovalle99/7b-SQLMasterApp/blob/1fc7bc62bff8ce550eed8d7542fc694a9da585ed/deploy.py)          |

## Getting Started

To get started with 7BSQL Master, simply visit the application URL: [http://ec2-3-91-221-46.compute-1.amazonaws.com:7860/](http://ec2-3-91-221-46.compute-1.amazonaws.com:7860/). Enter your natural language question, and the application will generate the corresponding SQL query for you.
