# Prompts and Experiment Results Analysis App

This Flask application provides a web interface for entering prompts, uploading coded datasets, calculating metrics such as percentage of matches and Cohen's Kappa score, and downloading results as a CSV file. It's designed to facilitate the analysis of experimental data comparing ground truth with inference data by tracking metadata for prompt engineering, including different versions of prompts, changes, and evaluation metrics. This will be used for the DEI summer undergraduate internship.

## Features

- **Interactive Web Interface:** Two main web pages for user interaction:
  - **Home Page:** Allows users to upload data and add original and revised prompts, as well as column names for ground truth and GPT-coded values for evaluation metrics (percent matched and IRR) calculation.
  - **Results Page:** Displays calculated metrics and provides options to download the data or go back to make changes.
- **Upload CSV Files:** Users can upload CSV files to analyze experimental data.
- **Calculate Metrics:** The app calculates the percentage of matches and Cohen's Kappa score for uploaded data.
- **Download Results:** Users can download a summary of their results in CSV format.

## Prerequisites

Before you can run this application, you need to have Python installed on your machine along with Flask and its dependencies. You will also need `pandas` and `sklearn` for data manipulation and metrics calculation.

## Installation

1. Clone the repository or download the source code.
2. Install required Python libraries:
   ```bash
   pip install Flask pandas scikit-learn
   ```
3. Navigate to the application directory.

## Usage

To start the application:

```bash
python3 promptApp.py
```

Once the application is running, navigate to `http://127.0.0.1:5000/` in your web browser to access the app.

### Uploading Data

- Go to the home page and use the upload form to submit a CSV file.
- Fill out the required fields including original and revised prompts, and the reasons for changes.
- Specify the column names for ground truth and inference data in your CSV file.

### Viewing and Downloading Results

- After uploading the data, the application will display the calculated metrics on the results page.
- You can view details about the prompts used and any changes made.
- Use the provided link to download a CSV file of your results.
- You can return to the home page to try another file by clicking the "Go Back" button.

## Configuration

You can modify the column names used in the calculations by editing the `ground_truth_column` and `inference_column` variables within the `upload_file` function to match the column names in your CSV files.

## Development

The application is set up with Flask's debug mode enabled to assist with development. Remember to disable debug mode in a production environment.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit pull requests with any enhancements or bug fixes.
This is a testing ground for custom prompt ops
