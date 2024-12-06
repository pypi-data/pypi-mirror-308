# UrlInfoTessMack

A simple python package to get informations about a url

## Installation

```bash
pip install UrlInfoTessMack
```

## Usage

```python
from urlinfotessmack import UrlInfo
url = "https://www.google.com/search?q=test"
url_info = UrlInfo(url)
print(url_info.get_protocol())
print(url_info.get_domain())
print(url_info.get_path())
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
