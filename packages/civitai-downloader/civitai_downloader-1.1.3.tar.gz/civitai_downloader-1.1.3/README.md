# CivitAI Downloader

A Python package for downloading models from CivitAI via a command-line tool or programmatically. This package supports token-based authentication and allows users to save downloaded models to a specified directory.



[![Open In Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/Ryouko65777/civitai-downloader)



## Installation

Install the package via pip:

```bash
pip install civitai-downloader
```

## Usage

### Command-Line Usage

To download a model from CivitAI, use the `civitai-downloader` command with the following arguments:

```bash
civitai-downloader <url> <output_path> <token>
```



### Programmatic Usage

You can also use the downloader in your own Python scripts.

```python
from civitai_downloader import download_file, get_token, store_token

url = 'https://civitai.com/api/download/models/46846'
output_path = '/path/to/save'
token = 'your_api_token_here'

download_file(url, output_path, token)
```

## Features

- **Token-based authentication:** Automatically stores your CivitAI API token for future use.
- **Progress tracking:** Shows download progress with speed in MB/s.
- **Error handling:** Includes handling for common download errors like redirects and missing files.

## API Token

The first time you use `civitai_downloader`, you'll be prompted to enter your CivitAI API token. This token will be stored in `~/.civitai/config`. You can generate your API token from your [CivitAI account settings](https://civitai.com/settings).

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Credits

gradio demo by - [Eddycrack864](https://github.com/Eddycrack864)


