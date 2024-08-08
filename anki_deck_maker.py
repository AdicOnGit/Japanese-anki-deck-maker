import genanki
import csv
import random
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def read_file(file_path):
    """Reads a file and returns its content."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logging.info(f"Successfully read file: {file_path}")
            return content
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        raise


def read_csv_file(file_path):
    """Reads a CSV file and returns its content."""
    if not os.path.exists(file_path):
        logging.error(f"CSV file not found: {file_path}")
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            logging.info(f"Successfully read CSV file: {file_path}")
            return list(reader)
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
        raise


def main(conversion_language, file_version, csv_file):
    # Read HTML and CSS files
    try:
        card_front_html = read_file('anki_templates/card_front.html')
        card_back_html = read_file('anki_templates/card_back.html')
        css_content = read_file('anki_templates/styles.css')
    except Exception as e:
        logging.error(f"Failed to read template files: {e}")
        return

    # Define the model
    try:
        model = genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            f'Japanese {conversion_language} Vocabulary Model',
            fields=[
                {'name': 'Core-index'},
                {'name': 'JLPT'},
                {'name': 'Vocab-expression'},
                {'name': 'Vocab-kana'},
                {'name': 'conversion_language-meaning'},
                {'name': 'Vocab-meaning-eng'},
                {'name': 'Vocab-pos'},
                {'name': 'Sentence-expression'},
                {'name': 'Sentence-kana'},
                {'name': 'Sentence-meaning-conversion_language'},
                {'name': 'Sentence-meaning-eng'},
                {'name': 'conversion_language'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': card_front_html,
                    'afmt': card_back_html,
                },
            ],
            css=css_content
        )
        logging.info("Model created successfully.")
    except Exception as e:
        logging.error(f"Error creating model: {e}")
        return

    # Create a new deck
    try:
        deck = genanki.Deck(
            random.randrange(1 << 30, 1 << 31),
            f'Japanese {conversion_language} Vocabulary Deck'
        )
        logging.info("Deck created successfully.")
    except Exception as e:
        logging.error(f"Error creating deck: {e}")
        return

    # Read the CSV file and add notes to the deck
    try:
        csv_data = read_csv_file(csv_file)
        for row in csv_data:
            note = genanki.Note(
                model=model,
                fields=[
                    row.get('Core-index', ''),
                    row.get('jlpt', ''),
                    row.get('Vocab-expression', ''),
                    row.get('Vocab-kana', ''),
                    row.get(f'{conversion_language}-meaning', ''),
                    row.get('Vocab-meaning-eng', ''),
                    row.get('Vocab-pos', ''),
                    row.get('Sentence-expression', ''),
                    row.get('Sentence-kana', ''),
                    row.get(f'Sentence-meaning-{conversion_language}', ''),
                    row.get('Sentence-meaning-eng', ''),
                    conversion_language
                ]
            )
            deck.add_note(note)
        logging.info("Notes added to deck successfully.")
    except Exception as e:
        logging.error(f"Error processing CSV data: {e}")
        return

    # Create and save the Anki package
    try:
        genanki.Package(deck).write_to_file(
            f'versions/{file_version}/Jap-{conversion_language}-{file_version}.apkg')
        logging.info("Anki package created and saved successfully.")
    except Exception as e:
        logging.error(f"Error creating Anki package: {e}")


if __name__ == "__main__":
    conversion_language = "Bahasa"
    file_version = "first500"
    csv_file = f"versions/{file_version}/Jap-{
        conversion_language}-{file_version}.csv"
    main(conversion_language, file_version, csv_file)
