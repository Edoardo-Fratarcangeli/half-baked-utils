# GitHub Profile Analyzer

A Python desktop application to analyze GitHub profiles, visualize language usage, and export reports to PDF.

## Features

- **Profile Analysis**: Fetches repository data using GitHub GraphQL API.
- **Visualizations**: Displays language usage statistics in a table and pie chart.
- **PDF Export**: Generates a professional PDF report of the analysis.
- **GUI**: User-friendly interface built with PyQt5.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your GitHub Token:
   - Create a Personal Access Token on GitHub (with `read:user` and `repo` scopes).
   - Set the environment variable `GITHUB_TOKEN`.

## Usage

Run the application:

```bash
python main.py
```

1. Enter your Name, Website, GitHub Username, and Target Role.
2. Click **Analizza profilo**.
3. View the results and click **Export PDF** to save the report.

## Project Structure

- `src/`: Source code modules.
- `main.py`: Application entry point.
- `.vscode/`: VS Code debug configuration.

## Requirements

- Python 3.8+
- See `requirements.txt` for libraries.
