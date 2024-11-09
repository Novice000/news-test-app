# News Generator

**News Generator** is a Python-based CLI tool that fetches news articles and generates a PDF with headlines and links to top news stories or articles based on user-specified search terms. Users can retrieve either trending headlines or search through a vast archive of articles from multiple sources. 

## Features

- **Top Headlines**: Fetch the latest top and breaking news headlines by country, category, or specific sources.
- **Everything Search**: Search across millions of articles from a variety of sources, including both large and niche news outlets.
- **PDF Export**: Export the retrieved headlines and article links to a PDF document.

## Usage

Run the `project.py` file with command-line options to specify your query type and output file. 

```bash
usage: project.py [-h] (-t | -e) -f FILE

options:
  -h, --help            show this help message and exit
  -t, --headlines       Fetch live top and breaking headlines by country, category, or specific sources.
  -e, --everything      Search through millions of articles from numerous news sources and blogs.
  -f FILE, --file FILE  Specify the output PDF filename for saving the news results.
```

### Example Commands

- Fetch top headlines:
  ```bash
  python project.py -t -f headlines.pdf
  ```
- Search through all news articles with specific keywords:
  ```bash
  python project.py -e -f search_results.pdf
  ```

## Project Structure

### Main Files

- **`project.py`**: Contains the main program, responsible for managing CLI options, requesting news data, validating inputs, and generating the PDF.
- **`requirements.txt`**: Lists dependencies for the project, installable via:
  ```bash
  pip install -r requirements.txt
  ```

### Functions Overview

#### Core Functions

- **`main`**: Entry point that combines all functions to achieve the overall program functionality.
- **`cli`**: Manages command-line arguments, validates input, and returns the news type and output file path.
- **`pdfify`**: Converts retrieved headlines and URLs into a formatted PDF document.

#### Input & Validation Helpers

- **`get_source_table`**: Provides a dictionary of sources by country and category for user selection.
- **`inp_params`**: Checks the news type (headlines or everything) and prompts users for relevant parameters. Returns a dictionary of parameters with user inputs.
- **`check_q`**: Validates if a string is a single letter (exiting if so), or returns `None` if empty.
- **`check_date`**: Validates if a string matches ISO 8601 date or datetime format, returning the date or exiting on invalid input.
- **`check_page`**: Verifies if a string can convert to an integer (for pagination), returning it or exiting on invalid input.
- **`check_country`** and **`check_category`**: Validate against lists of allowed countries and categories, respectively.
- **`check_source`**: Ensures the source input matches valid sources.
- **`check_path`**: Validates the provided file path.

#### API Request Functions

- **`headlines`**: Makes an HTTP request to retrieve top headlines based on user parameters.
- **`everything`**: Retrieves articles from the "everything" endpoint with a wide array of filters and returns JSON-formatted data.

### Tests

**`test_project.py`**: Contains unit tests for key functions in `project.py`, ensuring proper validation and handling.

- **`test_check_q`**: Tests the `check_q` function.
- **`test_check_date`**: Tests the `check_date` function.
- **`test_check_num`**: Tests `check_page`.
- **`test_check_country`** and **`test_check_category`**: Test country and category validation functions.

## Example Workflow

1. **Specify Query Type**: Use `-t` for top headlines or `-e` to search all articles.
2. **Define Output**: Specify `-f` followed by the filename (e.g., `output.pdf`) to save the PDF.
3. **Enter Parameters**: Follow prompts to specify parameters like `country`, `category`, and date range.
4. **View Output**: Check the generated PDF file for compiled headlines and article links.

## Conclusion

This project showcases the use of APIs, PDF generation, and robust user input validation to create a practical CLI tool. While the core functionality is implemented, additional features could include:
- Improved error handling and logging.
- Enhanced PDF formatting with summaries or article snippets.
- Scheduled, automated PDF generation based on saved queries.
