# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "openai",
#     "tenacity",
# ]
# ///

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tenacity import retry, stop_after_attempt, wait_fixed
import openai
import sys

# Set OpenAI API key
openai.api_key = os.environ.get("AI_PROXY")
if not openai.api_key:
    raise EnvironmentError("AI_PROXY environment variable is not set.")

# Retry logic for API calls
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def call_openai(prompt):
    """Make a robust call to OpenAI."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"]

def load_and_summarize(file_path):
    """Load and summarize the dataset."""
    df = pd.read_csv(file_path, encoding="latin1")
    summary = {
        "shape": df.shape,
        "columns": df.dtypes.to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "sample": df.head(5).to_dict(orient="records")
    }
    return df, summary

def create_visualizations(df, output_dir):
    """Generate and save visualizations."""
    visualizations = []
    # Correlation heatmap
    if not df.corr(numeric_only=True).isnull().all().all():
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
        heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
        plt.savefig(heatmap_path)
        plt.close()
        visualizations.append(heatmap_path)

    # Missing values bar plot
    missing = df.isnull().sum()
    if missing.any():
        plt.figure(figsize=(8, 6))
        sns.barplot(x=missing.index, y=missing.values)
        plt.title("Missing Values")
        plt.xticks(rotation=45)
        missing_path = os.path.join(output_dir, "missing_values.png")
        plt.savefig(missing_path)
        plt.close()
        visualizations.append(missing_path)
    
    return visualizations

def generate_story(summary, visualizations):
    """Generate a story using OpenAI."""
    prompt = f"""
    I analyzed a dataset with the following summary:
    - Shape: {summary['shape']}
    - Columns and Data Types: {summary['columns']}
    - Missing Values: {summary['missing']}
    - Sample Data: {summary['sample']}

    Visualizations:
    - Correlation Heatmap: {os.path.basename(visualizations[0])}
    - Missing Values: {os.path.basename(visualizations[1]) if len(visualizations) > 1 else 'N/A'}

    Write a detailed narrative about the dataset insights.
    """
    return call_openai(prompt)

def save_results(output_dir, story, visualizations):
    """Save the story and visualizations to the output directory."""
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(story)

def main():
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py ")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = os.path.splitext(input_file)[0]
    os.makedirs(output_dir, exist_ok=True)

    # Load and analyze data
    df, summary = load_and_summarize(input_file)

    # Generate visualizations
    visualizations = create_visualizations(df, output_dir)

    # Create a narrative story
    story = generate_story(summary, visualizations)

    # Save results
    save_results(output_dir, story, visualizations)
    print(f"Analysis completed! Results saved in {output_dir}")

if __name__ == "__main__":
    main()
