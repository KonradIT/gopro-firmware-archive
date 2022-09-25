import requests
from bs4 import BeautifulSoup
from utils import get_day, replace_line

class LabsFirmwareDownloader:
	def __init__(self, url="https://community.gopro.com/s/article/GoPro-Labs?language=en_US"):
		self.url = url
		
  
	def __get_html_text(self, payload: dict) -> dict:
		key = "Message__c"
		for k, v in payload.items():
				if k == key:
					return v
				elif isinstance(v, dict):
					p = self.__get_html_text(v)
					if p is not None:
						return p
			
	def get(self) -> None:
		
		cookies = {
			'renderCtx': '%7B%22pageId%22%3A%22ab75e21f-79df-418f-a9c2-3d28838b77c1%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%22463973ed-2501-4c3c-9ebd-469ee1ae8d9b%22%2C%22audienceIds%22%3A%226Au3b000000Kz8V%22%7D',
			'CookieConsentPolicy': '0:1',
			'LSKey-c$CookieConsentPolicy': '0:1',
			'force-proxy-stream': '!k/0NvsdtEDOfR50rtG3tgA5N95FzTu0sPoChtUQf3htL0/eo1mkBxJrmWJx6Xy/oDcTieUPI3GMzyMw=',
			'sfdc-stream': '!y9drwQD+Tpo2lz8sLfvCYtUI8W0gYkGGZrWfdc+nlsauz6j3o6ijyJ99PBXEjLD8KSSPzraBzaQT0Q==',
			'force-stream': '!y9drwQD+Tpo2lz8sLfvCYtUI8W0gYkGGZrWfdc+nlsauz6j3o6ijyJ99PBXEjLD8KSSPzraBzaQT0Q==',
			'_gcl_au': '1.1.588552888.1664134092',
			'_uetsid': '32bd2de03d0811ed9d39890c210b8225',
			'_uetvid': '32bd1d203d0811ed93de151a3c3e9020',
			'_tt_enable_cookie': '1',
			'_ttp': '463e1432-c99a-4868-b153-c39e45b97525',
			'_ga_NX92TBC2KF': 'GS1.1.1664134095.1.0.1664134095.60.0.0',
			'_ga': 'GA1.1.1987406895.1664134095',
		}

		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			# 'Accept-Encoding': 'gzip, deflate, br',
			'Referer': 'https://community.gopro.com/s/article/GoPro-Labs?language=en_US',
			'X-SFDC-Page-Scope-Id': '0d304635-dfbe-4071-9f1d-e1d8c4c3251f',
			'X-SFDC-Request-Id': '4778000000de860de6',
			'X-SFDC-Page-Cache': 'ffa61ea01fcebb15',
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
			'Origin': 'https://community.gopro.com',
			'DNT': '1',
			'Connection': 'keep-alive',
			# Requests sorts cookies= alphabetically
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			# Requests doesn't support trailers
			# 'TE': 'trailers',
		}
		params = {
			'r': '3',
			'ui-force-components-controllers-recordGlobalValueProvider.RecordGvp.getRecord': '1',
		}

		data = {
			'message': '{"actions":[{"id":"282;a","descriptor":"serviceComponent://ui.force.components.controllers.recordGlobalValueProvider.RecordGvpController/ACTION$getRecord","callingDescriptor":"UNKNOWN","params":{"recordDescriptor":"ka13b000000QSAwAAO.undefined.FULL.null.null.Summary.VIEW.true.null.Summary,LastModifiedDate,Message__c,CreatedDate,Title,Id,LastModifiedById,SystemModstamp.null"}}]}',
			'aura.context': '{"mode":"PROD","fwuid":"QPQi8lbYE8YujG6og6Dqgw","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"Zj1VcUXqZfCDWZ-Q5LxXcA","COMPONENT@markup://force:outputField":"yClNNqFExn4evLotb5Pplg","COMPONENT@markup://forceChatter:feedQbProxy":"fr0uC15O20eYx6JC5zAaiQ","COMPONENT@markup://forceCommunity:forceCommunityFeed":"vhVEZIiBt64So-_HjsnASw","COMPONENT@markup://instrumentation:o11yCoreCollector":"8089lZkrpgraL8-V8KZXNw"},"dn":[],"globals":{},"uad":false}',
			'aura.pageURI': '/s/article/GoPro-Labs?language=en_US',
			'aura.token': 'null',
		}

		r = requests.post("https://community.gopro.com/s/sfsites/aura", params=params, cookies=cookies, headers=headers, data=data)
  
		loaded = r.json()
		dictionary = self.__get_html_text(loaded.get("context").get("globalValueProviders")[1].get("values").get("records"))
		#print(dictionary.get("value"))
		soup = BeautifulSoup(dictionary.get("value"), "lxml")
		for lists in soup:
			ulList = lists.find_all("li")
			for li in ulList:
				if li.find("a"):
					if "https://gopro.my.salesforce.com" in li.a.get('href'):
						# is a camera
						# v1.10.70 | Sept 2022
						download_url = li.a.get('href')
						print(li.text.strip())
						camera_name = li.text.strip().split(" v")[0]
						version = li.text.strip().split(" | ")[0].split("v")[1]
						date = li.text.strip().split(" | ")[1]
						try:
							f = open("./data/Labs/%s.md" % camera_name.replace(" ", "_"), "r")
							if version in f.read():
								continue
						except:
							f = open("./data/Labs/%s.md" % camera_name.replace(" ", "_"), "w")
							f.write("%s Labs Firmwares:\n\n\n\n" % camera_name)
							f.close()
						replace_line("./data/Labs/%s.md" % camera_name.replace(" ", "_"), 1, """
- **v%s** - Date: *%s*:
	- **Original Firmware URL**: %s
 """ % (version, date, download_url))
