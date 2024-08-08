import csv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def prompt_text_maker(language="Bahasa", starting_row=1, ending_row=10):
    csv_file_name = "Core_vocabularies.csv"
    list_ = []

    try:
        with open(csv_file_name, mode='r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = 0

            # Skip the header
            next(csv_reader)
            for row in csv_reader:
                row_count += 1

                if starting_row <= row_count < ending_row:
                    try:
                        dic = {
                            "Japanese-word": row[2],
                            "Japanese-sentence": row[6]
                        }
                        list_.append(dic)
                    except IndexError as e:
                        logging.warning(
                            f"Row {row_count} skipped due to missing data: {e}")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return []
    except IOError as e:
        logging.error(f"IO error occurred: {e}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return []

    prompt_text = f'''I will provide you with a list containing Japanese words along with their corresponding Japanese sentences. You need to translate each one and return the information in the following JSON format:

    {{
      "word": "Japanese word",
      "sentence": "Japanese sentence",
      "word-{language}": "Translation of the Japanese word in {language}",
      "sentence-{language}": "Translation of the Japanese sentence in {language}"
    }}

    This is the list:

    {list_}

    Notes:
    1. Please ensure the translations are simple and meaningful.
    2. The translations should be casual and not too formal.
    '''

    # Log the created prompt text
    logging.info(f'Generated prompt text: {prompt_text}')

    # save the prompt text into a file
    logging.info(f'Saving prompt text to prompt.txt')
    with open('prompt.txt', 'w', encoding='utf-8') as f:
        f.write(prompt_text)

    only_words = []
    for dic in list_:
        only_words.append(dic["Japanese-word"])

    # Log the extracted words
    logging.info(f'Extracted words: {only_words}')

    return prompt_text, only_words


# Example usage
if __name__ == "__main__":
    starting_row = 1
    ending_row = 501
    prompt_text, only_words = prompt_text_maker(
        starting_row=starting_row, ending_row=ending_row)
    print(prompt_text)
