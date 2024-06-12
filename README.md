# Smart Spreadsheet

## How to run?

Make sure that you have `poetry` installed along with Python 3.12. Then, run:

```sh
poetry install # Install dependencies
poetry shell # Instantiate the virtualenv
```

The app can, at the moment, run with two different LLMs models:

- [BambooLLM](https://pandabi.ai/)
- [OpenAI Models](https://openai.com/)

Setup the environment variables:

```sh
BAMBOO_API_KEY="$2..."
OPEN_API_TOKEN="sk..."
```

Now, you'll have two options to run the app:

### Auto Parser

In this mode, the app will try to parse the Excel file without any input. To run in this mode, type:

```sh
## Using BambooLLM
python main.py auto <FILE_PATH> bamboo

## Using OpenAI Models
python main.py auto <FILE_PATH> openai
```

### Manual Parser

In this mode, the app will need some inputs to parse the Excel file. To run in this mode, type:

```sh
## Using BambooLLM
python main.py manual <FILE_PATH> bamboo

## Using OpenAI Models
python main.py manual <FILE_PATH> openai
```