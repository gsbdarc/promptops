from flask import Flask, request, render_template, send_file, redirect, url_for, session
import os
import html
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from difflib import ndiff
from dotenv import load_dotenv
load_dotenv()

# Create a Flask instance
app = Flask(__name__)

# Set the secret key from an environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_fallback_secret_key')

# Define results globally
results = []

@app.route('/', methods=['GET'])
def home():

    """
    Serves the homepage template.

    This function handles the route for the root URL ('/'). It is responsible for rendering
    and returning the 'index.html' template, which serves as the homepage of the application.
    The template can be customized by enabling the 'project_name' variable if needed.

    Returns:
        A rendered template ('index.html') that serves as the homepage of the application.
    """

    return render_template('index.html')


def highlight_character_differences(prompt1, prompt2):

    """
    Highlights character differences between two prompts with HTML and aggregates added and deleted characters.

    Args:
    - prompt1 (str): The original string.
    - prompt2 (str): The modified string.

    Returns:
    - str: An HTML string with differences highlighted.
    - dict: A dictionary with 'added' and 'deleted' keys and the corresponding aggregated values.
    """

    result = []
    added = []
    deleted = []
    diff = ndiff(prompt1, prompt2)

    for char in diff:
        if char.startswith('+ '):
            result.append(f'<span style="background-color: #ccffcc">{html.escape(char[-1])}</span>')
            added.append(char[-1])
        elif char.startswith('- '):
            result.append(f'<span style="background-color: #ffcccc">{html.escape(char[-1])}</span>')
            deleted.append(char[-1])
        elif char.startswith('  '):
            result.append(html.escape(char[-1]))

    aggregated_changes = {
        'added': ', '.join(added),
        'deleted': ', '.join(deleted)
    }

    return ''.join(result), aggregated_changes


@app.route('/upload', methods=['POST'])
def upload_file():

    """
    Handles the file upload and process the CSV data to calculate metrics and record experiment results.
    This endpoint accepts a POST request with a file and form data. This function calculates the match percentage and kappa score
    between ground truth and inference columns specified in the form and processes other form data such as prompts and reasons for changes.

    Returns:
        A rendered HTML template displaying the calculated results and other experiment data.
    """

    if 'file' in request.files:
        file = request.files['file']

        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            file.seek(0)  # Reset file pointer to the beginning
            df = pd.read_csv(file, encoding='ISO-8859-1')  # Try a different encoding

        # Ground truth and inference column names
        ground_truth_column = request.form['ground_truth_column']
        inference_column = request.form['inference_column']

        ground_truth = df[ground_truth_column]
        inference = df[inference_column].astype('str')

        # Ensure both ground_truth and inference are of the same type (convert to strings)
        ground_truth_str = [str(item) for item in ground_truth]
        inference_str = [str(item) for item in inference]
        
        # Calculate metrics
        percent_matched = (pd.Series(ground_truth_str) == pd.Series(inference_str)).mean() * 100
        percent_matched_rounded = round(percent_matched, 1)
        kappa_score = cohen_kappa_score(ground_truth, inference)
        kappa_score_rounded = round(kappa_score, 1)

        # Capture additional form data
        original_prompt = request.form.get('original_prompt', 'Not provided')
        revised_prompt = request.form.get('revised_prompt', 'Not provided')
        changes_reason = request.form.get('changes_reason', 'Not provided')
        changes_display = highlight_character_differences(original_prompt, revised_prompt)[0]
        changes = highlight_character_differences(original_prompt, revised_prompt)[1]

        experiment_result = {
            "original_prompt": original_prompt,
            "revised_prompt": revised_prompt,
            "changes_display": changes_display,
            "changes": changes,
            "changes_reason": changes_reason,
            "percent_matched": percent_matched_rounded,
            "kappa_score": kappa_score_rounded,
            "experiment_id": len(results) + 1  # Simple way to generate a unique ID for each experiment
        }
        results.append(experiment_result)

        # Store and retrieve experiment results
        session['experiment_result'] = experiment_result  # Store the result in the session
        experiment_result = session.get('experiment_result', {})  # Retrieve the result from the session

        # Pass all data to the template
        return render_template('results.html',
                               matches=percent_matched_rounded , kappa_score=kappa_score_rounded,
                               original_prompt=original_prompt, revised_prompt=revised_prompt,
                               changes_display=changes_display, changes_reason=changes_reason)

@app.route('/download-results', methods=['GET'])
def download_results():

    """
    Provides a downloadable Excel file containing the results of all experiments.
    This endpoint handles a GET request and creates an Excel file from a DataFrame
    that accumulates the results of experiments, then sends this file as a downloadable
    attachment to the user.

    Returns:
        A Flask response object that triggers the download of the results Excel file.
    """

    # Convert the results list to a DataFrame for easy CSV conversion
    df_results = pd.DataFrame(results)

    # Define the CSV file name
    excel_file = "experiment_results.xlsx"

    # Save the DataFrame to a CSV file
    df_results.to_excel(excel_file, index=False)

    # Flask logic to send the results file to the user
    return send_file(excel_file, as_attachment=True, download_name=excel_file)


# Main
if __name__ == '__main__':
    # Run the Flask application with debug enabled; useful for development purposes.
    app.run(debug=True)
