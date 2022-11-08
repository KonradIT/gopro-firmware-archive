import requests
from bs4 import BeautifulSoup
from utils import get_day, replace_line
import json
import traceback

class LabsFirmwareDownloader:
	def __init__(self, url="https://community.gopro.com/s/article/GoPro-Labs?language=en_US"):
		self.url = url
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			# 'Accept-Encoding': 'gzip, deflate, br',
			'Referer': 'https://community.gopro.com/s/article/GoPro-Labs?language=en_US',
			'X-SFDC-Page-Scope-Id': '0d304635-dfbe-4071-9f1d-e1d8c4c3251f',
			'X-SFDC-Request-Id': '6885000000756bb6a0',
			'X-SFDC-Page-Cache': 'ae613cdab6e23c17',		
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
		self.fwuid = "5FtqNRNwJDpZNZFKfXyAmg"
		self.session = requests.Session()
		self.session.get(self.url, headers=self.headers)
		
  
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
			'gp_geoip_location': 'ES',
			'_ga': 'GA1.2.1164871419.1606895388',
			'lastRskxRun': '1606895389742',
			'rskxRunCookie': '0',
			'rCookie': 'mie6ustse8pgwre7v8knatki740y0h',
			'gp_features_id': '395bbdbf-e957-4c48-9b6a-08958cf714d8',
			'gp_locale_override': 'true',
			'pp_data': 'N4IgxgNglgpgdgFwPoHMCuUAmIBcJMBMALAMwwDsRARgLQCGRAjHTdSQAz0l0AcNBAVh4FMA9gDZuATnE1Gkno2HsC4ompABfIA_',
			'amplitude_idgopro.com': 'eyJkZXZpY2VJZCI6ImM3NzE4Yzg2LTk5MmYtNDYxYi05Njg5LTQwNjA2OTJjNDc5NSIsInVzZXJJZCI6Im1haWxAY2hlcm5vd2lpLmNvbSIsIm9wdE91dCI6ZmFsc2V9',
			'gp_language': 'es',
			'gp_location': 'ES',
			'community_user_id': '395bbdbf-e957-4c48-9b6a-08958cf714d8',
			'_urlg_app_session': 'WXhBdk5rMnVjMXQxT2s4d2NzOHVyZ09zMENHS2tSOHJpdlNYRzgrZloxMnRXTVc3Y1did3FqcVBzbzhqYlZNZnpiQlVUbU9CcWZXRkdtYktSaHQ1V3FiazRlYjdhVGh3L1hRckdYUVBJMFhUTGZTd2YrQnN4Y2V2VjdOWkNucHhoRVNTQThnUUdhdXQzNDY2Q1BvQzFBPT0tLUtVbDljbTd3cVRFdFRnQ3ZjSThtS0E9PQ%3D%3D--22b48e7f5ed51658ef899b6d649de232b0b90dff',
			'LiSESSIONID': '8DAE991F2DDC3DC0BFC5A1E6BD0B449F',
			'gp_user_id': '395bbdbf-e957-4c48-9b6a-08958cf714d8',
			'gp_access_token': 'eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkExMjhHQ00ifQ.x8nkhebCq7WEkXqsBsGRffTx-BPLhObGhtZSNHT2sNyt6SSTigJBP6-Q1RNqTlGzQofF4QYst1YyUYX7FJ_GqRGezbXwAC46TaCsbIvyO_URkJoR6yg2Xd6MHu1M2OI1_mdVRGE6rfIlntZGexdg7Or1RYre5wJCZ3vNUKI0YRvHo5R2ZwtC-H8KUBXNTvLZYpdHDhVthqu_WSIEDEwehOuVDLnqM6jqtsjlZjTVMus6GE615tucF2kgn5xsTv3EMH9Ch9sgi9Kf-AWrrqMAJ-OMiBn6AQTTGIEekdFvrncwYU1wzQD8xTN6H0ytmKLxj06IQfVgWj-hOPCG6mMtdA.Q98xjIPXq0GfzSd5.LmFm5goqMAI3TygdbPFj-nsXxF3kFA3AToI2pY2vC400OHVw3Q2-s6KAsBixeULDhn8_yVU8jO0kbaLW6rIFGSAZ-QjYmgZ8U-E5ux5J7bejaDAjbt8hHGzxzjSnRYT-wdDztUmPRs29DlaWJw7P5ol5IGYpsWCNId7321eYJVDFC3rUFpD4EYuWNnuHQLtZhoG3KD1yJ8bjJSvq3goXyBCv9ktK9pPt8nhy2HLlRl8B6xQmhoIe64dWCr5eAPajCOAzDxhIzSJnNzAQzLVRpVDGlJyJdialADhjuWoYdbqljmxMkAtj5AWuGWXMZTOWgmEjusX5OTle7uf2AV6LvPC-SoI55n8Cb_-qiIZsohQqnmsTj6hUn8uL76o-1F-oyRDjNVcdQ-k_LsH5jfWuN0dutExUX9-xUXsBc0T8PAoJ8PDCZUGK4NLiHjFXnUO578RGS4NAnNne9XZs1dOo1F1O3fBU-fDQnMxjlk6CFUp_ka70WXUIH7wD0AlNqZ_xMdz3Oy0qWsQO5dBlu2RUOFyi_FYn_1oDTzwA06qt6GRUb5oEqMD_ZE9ANeeRTZ5kjTtPQ1xXVkryl7HKgAOn_qNR47MG7YeTQe861xv51LQT3YqxWgDC7d8fL1Y-WaWTGv6zgfFRSjkvlRHwNU71OHtKGSaCI4hHhW9KUfQ2-KINbZSDyRnFc04Ts8Cwayp3vk_Pkm7ODDxOUjk8yRI5LjwWfzdp58-8hnCnNvWPaV9rn6c5XOvPAWsVlBFAsXEyimIdRnQvTeRTMyZltp2MWQ8NKHRMTZb7odwEgZImLcwms-kjd3qr9Q.VxeRWygXWxwL5J0qnnM4gQ',
			'CookieConsentPolicy': '0:1',
			'LSKey-c$CookieConsentPolicy': '0:1',
			'force-proxy-stream': '!HACg3oe3jwPwwnD65C+XCSbdMcPRW0fuzRSFiZpDKwFhavxeZHsBUvtJIfZp32wVreHftdC0LqWKG/0=',
			'sfdc-stream': '!azxoCkKjtNR/NMM2tgpxx7QiiB0rhbt0a91D0Dx414BLQpPOZbvDvgDDedGNv54rUSWwtJ/4X2vUwA==',
			'force-stream': '!azxoCkKjtNR/NMM2tgpxx7QiiB0rhbt0a91D0Dx414BLQpPOZbvDvgDDedGNv54rUSWwtJ/4X2vUwA==',
		}

		
		params = {
			'r': '5',
			'ui-force-components-controllers-recordGlobalValueProvider.RecordGvp.getRecord': '1',
		}

		data = {
			'message': '{"actions":[{"id":"270;a","descriptor":"serviceComponent://ui.force.components.controllers.recordGlobalValueProvider.RecordGvpController/ACTION$getRecord","callingDescriptor":"UNKNOWN","params":{"recordDescriptor":"ka13b0000000Se5AAE.undefined.FULL.null.null.Summary.VIEW.true.null.null.null"}}]}',
			'aura.context': '{"mode":"PROD","fwuid":"%s","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"s_4leunyp4tEvUlLxDl4iw","COMPONENT@markup://instrumentation:o11yCoreCollector":"93Js8cqwotuQqZe93Cxffg"},"dn":[],"globals":{},"uad":false}' % self.fwuid,
			'aura.pageURI': '/s/article/GoPro-Labs?language=en_US',
			'aura.token': 'null',
		}

		r = self.session.post("https://community.gopro.com/s/sfsites/aura", params=params, cookies=cookies, headers=self.headers, data=data)
  
		# Expect some errors...
		try:
			loaded = r.json()
		except:
			print(traceback.format_exc())
			print(r.text)
			assert "Framework has been updated. Expected:" in r.text
			# New fwuid...
			error_message = json.loads(r.text.replace("*/", "").replace("/*ERROR", ""))
			self.fwuid = error_message.get("exceptionMessage").split("Expected: ")[1].split(" Actual:")[0]
			print("Caught new FWUID (%s), continuing\n" % self.fwuid )
			return self.get()
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
