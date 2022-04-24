from io import BytesIO
import requests
import json
from github import Github
from github import GitReleaseAsset
import os
from typing import Dict

# Small wrapper class around the GitHub Release API
class Upload:
	def __init__(self):
		self.github = Github(os.getenv("GITHUB_TOKEN"))
		self.repo = self.github.get_repo("konradit/gopro-firmware-archive")
	def upload(self, file: BytesIO, file_len: int, version: str, release_notes: str, model_string: str, name: str, release_date: str) -> GitReleaseAsset:
		release = self.repo.create_git_release("%s_%s" % (model_string, version), "Firmware: %s" % name, release_notes, False, False)
		return release.upload_asset_from_memory(file, file_len,
								   "%s-%s-%s-firmware.zip" % (model_string, version.replace(".", "_"), release_date), 
								   "application/zip")
	def get_public_url(self, release: GitReleaseAsset):
		return release.browser_download_url
