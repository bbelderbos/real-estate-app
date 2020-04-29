""" Proxy Handling """
from dataclasses import dataclass, field
from pathlib import Path
from random import choice
from typing import List


@dataclass
class ProxyHandler:
    """ Proxy handling class, initiate it with a path to txt file
    with proxies in following format:
    <user>:<password>@<ip>:<port>pyte
    <user>:<password>@<ip>:<port>
    """

    path: Path
    proxies: List[str] = field(init=False)

    def __post_init__(self):
        """ Validates if path exists, and reads
        the proxies to a list of strings.
        """
        path = Path(self.path)
        if not path.exists():
            raise FileNotFoundError("File does not exist.")
        with path.open(mode="r", encoding="utf-8") as fid:
            self.proxies = list({x.strip() for x in fid if x.strip()})
        if not self.proxies:
            raise ValueError("File is Empty.")

    @property
    def random_proxy(self) -> dict:
        """ Return random proxy formatted as dict.
        """
        proxy = choice(self.proxies)
        return self.create_proxy_dict(proxy)

    @staticmethod
    def create_proxy_dict(proxy):
        """ create proxy dict.
        """
        proxy_str = f"http://{proxy}"
        return {"http": proxy_str, "https": proxy_str}
