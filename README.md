<img src="https://github.com/AdicOnGit/Japanese-Nepali-study/assets/137413419/987b89f2-c71b-49b5-b1c0-8d0c9c615f1c" width="500" height="500">

# Anki Deck Creator for Japanese Language Learning

This project is an automated tool for creating Anki decks to assist in learning Japanese vocabulary with translations in various languages. It processes core Japanese vocabulary, translates it, and generates Anki decks with customized card templates.

## Features

- Generates Anki decks from core Japanese vocabulary
- Supports translations to multiple languages (currently set up for Bahasa)
- Custom card templates with separate front and back designs
- CSS styling for attractive and readable cards
- Logging for easy debugging and monitoring

## Prerequisites

- Python 3.6+
- pip (Python package installer)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/anki-deck-creator.git
   cd anki-deck-creator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Project Structure

- `anki_deck_maker.py`: Main script for creating Anki decks
- `conversion.py`: Script for processing raw data and core vocabulary
- `prompt.py`: Script for generating prompts for translation
- `anki_templates/`: Directory containing HTML templates and CSS for Anki cards
  - `card_front.html`: Front template for Anki cards
  - `card_back.html`: Back template for Anki cards
  - `styles.css`: CSS styles for Anki cards
- `versions/`: Directory for storing version-specific files
- `Core_vocabularies.csv`: CSV file containing core Japanese vocabulary

## Usage

1. Prepare your core vocabulary CSV file (`Core_vocabularies.csv`).

2. Generate a translation prompt:

   ```
   python prompt.py
   ```

   This will create a `prompt.txt` file with instructions for translation.

3. Use the generated prompt to obtain translations (e.g., through a translation service or ChatGPT).

4. Save the translations as a JSON file in the `versions/{file_version}/` directory with the naming format: `Jap-{conversion_language}-{file_version}.json`.

5. Process the raw translations and core vocabulary:

   ```
   python conversion.py
   ```

   This will generate a CSV file with combined data.

6. Create the Anki deck:
   ```
   python anki_deck_maker.py
   ```
   This will generate an `.apkg` file in the `versions/{file_version}/` directory.

## Customization

- Modify the HTML templates in the `anki_templates/` directory to change the card layout.
- Adjust the CSS in `anki_templates/styles.css` to change the card appearance.
- Edit the `conversion_language` and `file_version` variables in the scripts to change the target language and version of the deck.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [genanki](https://github.com/kerrickstaley/genanki) for Anki deck generation
