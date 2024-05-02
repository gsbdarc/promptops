from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
from sklearn.metrics import cohen_kappa_score
import os

app = Flask(__name__)

# Define results globally
results = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        df = pd.read_csv(file)
        # Example column names, replace with actual column names from your form
        ground_truth_column = request.form['ground_truth_column']
        inference_column = request.form['inference_column']

        ground_truth = df[ground_truth_column]
        inference = df[inference_column].astype('str')

        # Calculate metrics
        percent_matched = (ground_truth == inference).mean() * 100
        percent_matched_rounded = round(percent_matched, 1)
        kappa_score = cohen_kappa_score(ground_truth, inference)
        kappa_score_rounded = round(kappa_score, 1)

        # Capture additional form data
        original_prompt = request.form.get('original_prompt', 'Not provided')
        revised_prompt = request.form.get('revised_prompt', 'Not provided')
        changes_made = request.form.get('changes_made', 'Not provided')

        experiment_result = {
            "original_prompt": original_prompt,
            "revised_prompt": revised_prompt,
            "changes_made": changes_made,
            "percent_matched": percent_matched_rounded,
            "kappa_score": kappa_score_rounded,
            "experiment_id": len(results) + 1  # Simple way to generate a unique ID for each experiment
        }
        results.append(experiment_result)

        # Pass all data to the template
        return render_template('results.html',
                               matches=percent_matched_rounded , kappa_score=kappa_score_rounded,
                               original_prompt=original_prompt, revised_prompt=revised_prompt,
                               changes_made=changes_made)

    return 'No file uploaded', 400


# @app.route('/download', methods=['POST'])
# def download_file():
#     # Default filename if none is specified
#     default_name = "default_filename.csv"
#
#     # Get the custom filename from the form data
#     custom_filename = request.form.get('custom_filename', default_name) + '.csv'
#
#     # Specify the path to the file you want to download
#     # This could be a static path or dynamically generated based on other logic
#     file_path = "path/to/your/generated_file.csv"
#
#     # Serve the file for download with the custom or default filename
#     return send_file(file_path, as_attachment=True, download_name=custom_filename)

@app.route('/download-results', methods=['GET'])
def download_results():
    # Convert the results list to a DataFrame for easy CSV conversion
    df_results = pd.DataFrame(results)

    # Define the CSV file name
    csv_file = "experiment_results.csv"

    # Save the DataFrame to a CSV file
    df_results.to_csv(csv_file, index=False)

    # Flask logic to send the CSV file to the user
    return send_file(csv_file, as_attachment=True, download_name=csv_file)


if __name__ == '__main__':
    app.run(debug=True)
