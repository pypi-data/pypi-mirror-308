from urllib.parse import urlparse


class UrlInfo:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)

    def get_protocol(self):
        return self.parsed_url.scheme
    
    def get_domain(self):
        return self.parsed_url.netloc
    
    def get_path(self):
        return self.parsed_url.path
    
    def get_query(self):
        return self.parsed_url.query
    
    def get_fragment(self):
        return self.parsed_url.fragment


if __name__ == "__main__":
    url = "https://www.google.com/search?q=test"
    url_info = UrlInfo(url)
    print(url_info.get_protocol())
    print(url_info.get_domain())
    print(url_info.get_path())
