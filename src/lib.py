from io import BytesIO
import requests
from dataclasses import dataclass
import html2text
from typing import Dict, Tuple


@dataclass
class Firmware:
    Model: int
    ModelString: str
    Name: str
    Version: str
    ReleaseDate: str
    ReleaseNotes: str
    DownloadURL: str

    def get_safe_name(self):
        return self.Name.replace(" ", "_").replace("(", "").replace(")","")

    def get_as_upload_payload(self) -> BytesIO:
        response = requests.get(self.DownloadURL)
        files = BytesIO(response.content)
        return files

    def get_firmware_size(self) -> int:
        response = requests.head(self.DownloadURL)
        return int(response.headers.get("Content-Length"))

class FirmwareCatalog:
    def __init__(
        self,
        endpoint: str = "https://firmware-api.gopro.com/v2/firmware/catalog",
        timeout: int = 1,
    ):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.timeout = timeout
        self.__payload: dict

    def get_catalog(self) -> None:
        self.__payload = self.session.get(self.endpoint, timeout=self.timeout).json()
        self.__prune()

    def __prune(self):
        self.__payload = self.__payload.get("cameras")

    def get_all_cameras(self):
        for cam in self.__payload:
            yield Firmware(
                Version=cam["version"],
                ReleaseDate=cam["release_date"],
                ReleaseNotes=html2text.html2text(cam["release_html"]),
                DownloadURL=cam["url"],
                Model=cam["model"],
                ModelString=cam["model_string"],
                Name=cam["name"],
            )
