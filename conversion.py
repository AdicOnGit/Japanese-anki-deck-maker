import csv
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

"""
This script requires two inputs:
1. A JSON file with raw data obtained from chatGPT, named according to the pattern: "versions/{file_version}/Jap-{conversion_language}-{file_version}.json".
2. A CSV file containing core vocabulary named "Core_vocabularies.csv" with approximately 6,000 entries.

The JSON file should be structured with keys for word, sentence, word-{conversion_language}, and sentence-{conversion_language}. The CSV file must have columns where the third column contains the word to be matched against the JSON data.

Ensure that both files are present in the correct directory before running the script.
"""


def process_raw_text(filename):
    """Load JSON data from the specified file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        logging.info(f"Successfully loaded JSON data from {filename}.")
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the file: {filename}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise


def main(start_row, end_row, main_core_file, raw_json_file, new_file):
    """Process core vocabulary and JSON data, then write the results to a new CSV file."""
    try:
        conversion_language_list = process_raw_text(raw_json_file)
    except Exception as e:
        logging.error(f"Failed to process raw JSON file: {str(e)}")
        return

    new_list = []

    try:
        with open(main_core_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            header = next(csv_reader)  # Skip the header row

            # Create a dictionary from the JSON list for faster lookup
            conversion_language_dict = {item["word"]: {
                f"{conversion_language}-meaning": item[f"word-{conversion_language}"],
                f"sent-{conversion_language}": item[f"sentence-{conversion_language}"]
            } for item in conversion_language_list}

            # Process each row within the specified range and check for matches
            row_count = 0
            for row in csv_reader:
                row_count += 1
                if start_row <= row_count < end_row:
                    # Assuming the word to match is in the third column (index 2)
                    word = row[2]
                    if word in conversion_language_dict:
                        # Insert the meaning and sentence before the 5th and 10th columns respectively
                        row.insert(4, conversion_language_dict[word][f"{
                                   conversion_language}-meaning"])
                        row.insert(
                            9, conversion_language_dict[word][f"sent-{conversion_language}"])
                        new_list.append(row)
        logging.info(f"Successfully processed core vocabulary file: {
                     main_core_file}.")
    except FileNotFoundError:
        logging.error(f"File not found: {main_core_file}")
        return
    except Exception as e:
        logging.error(
            f"Unexpected error occurred while processing core vocabulary: {str(e)}")
        return

    headers = ["Core-index", "jlpt", "Vocab-expression", "Vocab-kana", f"{conversion_language}-meaning", "Vocab-meaning-eng",
               "Vocab-pos", "Sentence-expression", "Sentence-kana", f"Sentence-meaning-{conversion_language}", "Sentence-meaning-eng"]

    try:
        with open(new_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(headers)
            for line in new_list:
                csv_writer.writerow(line)
        logging.info(f"Successfully wrote results to {new_file}.")
    except Exception as e:
        logging.error(
            f"Unexpected error occurred while writing to file: {str(e)}")
        raise


if __name__ == "__main__":
    start_row = 1
    end_row = 501
    file_version = "first500"
    conversion_language = "Bahasa"
    main_core_file = "Core_vocabularies.csv"
    new_file = f"versions/{file_version}/Jap-{
        conversion_language}-{file_version}.csv"
    raw_json_file = f"versions/{file_version}/Jap-{
        conversion_language}-{file_version}.json"
    main(start_row, end_row, main_core_file, raw_json_file, new_file)
