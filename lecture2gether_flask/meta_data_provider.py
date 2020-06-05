import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class VideoNotFoundException(Exception):
    pass


class VideoUnauthorizedException(Exception):
    pass


class MetaDataProvider():
    def __init__(self, video_url):
        self.video_meta_data = {
            "Url": video_url,
            "StreamUrl": None,
            "Title": None,
            "Creator": None,
            "CreatorLink": None,
            "Date": None,
            "License": None,
            "LicenseLink": None,
        }

        self.get_meta_data()

    def get_meta_data(self):
        return self.video_meta_data

class L2GoMetaDataProvider(MetaDataProvider):
    def __init__(self, video_url, password=''):
        self._password = password

        try:  # Get video
            r = requests.post(self.video_meta_data["Url"], data={'_lgopenaccessvideos_WAR_lecture2goportlet_password': self._password}, headers={'User-Agent': 'Lecture2Gether'})
        except requests.exceptions.RequestException as e:
            raise VideoNotFoundException()

        self.parsed_url = urlparse(video_url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

        # Redirected to catalog means video does not exist
        _page_title = self.soup.find("title").text
        if "Catalog - Lecture2Go" in _page_title or "Videokatalog - Lecture2Go" in _page_title:
            raise VideoNotFoundException()

        # Check for password required or wrong
        if self.soup.find("input", {"id": "_lgopenaccessvideos_WAR_lecture2goportlet_password"}):
            raise VideoUnauthorizedException()

        super().__init__(video_url)

    def get_meta_data(self):
        self.video_meta_data["StreamUrl"] = self._parse_stream_url()
        self.video_meta_data["Title"] = self._parse_title()
        self.video_meta_data["Creator"] = self._parse_creator()
        self.video_meta_data["CreatorLink"] = self._parse_creator_link()
        self.video_meta_data["Date"] = self._parser_date()
        self.video_meta_data["License"] = self._parse_license()
        self.video_meta_data["LicenseLink"] = self._parse_creator_link()
        return super().get_meta_data()

    def _parse_stream_url(self):
        return re.search('https://[^"]*m3u8', self.soup.text).group()

    def _parse_title(self):
        return self.soup.find("div", {"class": "meta-title"}).text.strip()

    def _parse_creator(self):
        return self.soup.find("div", {"class": "meta-creators"}).find("a").text.strip()

    def _parse_creator_link(self):
        _creator_link = self.soup.find("div", {"class": "meta-creators"}).find('a')['href']
        if _creator_link is None:
            return None
        return f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/{_creator_link}"

    def _parser_date(self):
        _date_string = self.soup.find("div", {"class": "meta-creators"}).find("div", "date").text.strip()
        if _date_string is None:
            return None
        return datetime.strptime(_date_string, "%d.%m.%Y")

    def _parse_license(self):
        _license_string = self.soup.find("div", {"class": "license"}).find("a").text
        if _license_string is None:
            return None
        return re.split(r":\s", _license_string)[1].strip()

    def _parser_license_link(self):
        return self.soup.find("div", {"class": "license"}).find("a")['href'].strip()


class YouTubeMetaDataProvider(MetaDataProvider):
    def __init__(self, video_url):
        super().__init__(video_url)

    def main():
        scopes = []
        # TODO Read API-Key from environment var
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.videos().list(
            part="status",
            id="VIDEO-ID"  # TODO
        )
        response = request.execute()

        print(response)
