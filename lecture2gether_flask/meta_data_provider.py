import os
import re
import json
import requests
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class VideoNotFoundException(Exception):
    pass


class VideoUnauthorizedException(Exception):
    pass


class APIUnauthorizedException(Exception):
    pass


class MetaDataProvider():
    def __init__(self, video_url):
        self.video_meta_data = {
            "url": video_url,
            "streamUrl": video_url,
            "title": None,
            "creator": None,
            "creatorLink": None,
            "date": None,
            "license": None,
            "licenseLink": None,
            "mimeType": None
        }

    def get_meta_data(self):
        return self.video_meta_data


class DefaultMetaDataProvider(MetaDataProvider):
    pass


class L2GoMetaDataProvider(MetaDataProvider):
    def __init__(self, video_url, password=''):
        super().__init__(video_url)

        self._password = password

        try:  # Get video
            r = requests.post(self.video_meta_data["url"], data={'_lgopenaccessvideos_WAR_lecture2goportlet_password': self._password}, headers={'User-Agent': 'Lecture2Gether'})
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

    def get_meta_data(self):
        self.video_meta_data["streamUrl"] = self._parse_stream_url()
        self.video_meta_data["title"] = self._parse_title()
        self.video_meta_data["creator"] = self._parse_creator()
        self.video_meta_data["creatorLink"] = self._parse_creator_link()
        self.video_meta_data["date"] = self._parse_date()
        self.video_meta_data["license"] = self._parse_license()
        self.video_meta_data["licenseLink"] = self._parse_license_link()
        return super().get_meta_data()

    def _parse_stream_url(self):
        return re.search('https://[^"]*m3u8', str(self.soup)).group()

    def _parse_title(self):
        return self.soup.find("div", {"class": "meta-title"}).text.strip()

    def _parse_creator(self):
        return self.soup.find("div", {"class": "meta-creators"}).find("a").text.strip()

    def _parse_creator_link(self):
        _creator_link = self.soup.find("div", {"class": "meta-creators"}).find('a')['href']
        if _creator_link is None:
            return None
        return f"{self.parsed_url.scheme}://{self.parsed_url.netloc}{_creator_link}"

    def _parse_date(self):
        _date_string = self.soup.find("div", {"class": "meta-creators"}).find("div", "date").text.strip()
        if _date_string is None:
            return None
        return datetime.strptime(_date_string, "%d.%m.%Y")

    def _parse_license(self):
        _license_string = self.soup.find("div", {"class": "license"}).find("a").text
        if _license_string is None:
            return None
        return re.split(r":\s", _license_string)[1].strip()

    def _parse_license_link(self):
        return self.soup.find("div", {"class": "license"}).find("a")['href'].strip()


class YouTubeMetaDataProvider(MetaDataProvider):
    def __init__(self, video_url):
        super().__init__(video_url)
        self._video_id = YouTubeMetaDataProvider.youtube_video_id_from_url(video_url)
        if not self._video_id:
            raise VideoNotFoundException

    def get_meta_data(self):
        if 'GOOGLE_API_KEY' not in os.environ:
            self.video_meta_data["url"] = f'https://www.youtube.com/watch?v={self._video_id}'
            self.video_meta_data["streamUrl"] = f'https://www.youtube.com/watch?v={self._video_id}'
            return super().get_meta_data()

        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=os.environ['GOOGLE_API_KEY'], cache_discovery=False)

        request = youtube.videos().list(
            part="snippet,status",
            id=self._video_id,
        )
        response = request.execute()['items'][0]
        self.video_meta_data = {
            "url": f'https://www.youtube.com/watch?v={self._video_id}',
            "streamUrl": f'https://www.youtube.com/watch?v={self._video_id}',
            "title": response['snippet']['title'],
            "creator": response['snippet']['channelTitle'],
            "creatorLink": f'https://www.youtube.com/channel/{response["snippet"]["channelId"]}',
            "date": datetime.strptime(response['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
            "license": response['status']['license'],
            "licenseLink": None,
        }

        return super().get_meta_data()

    @staticmethod
    def youtube_video_id_from_url(video_url):
        url = urlparse(video_url)
        if url.hostname == 'youtu.be':
            # Return path without '/'
            return url.path[1:]
        if url.hostname in ['youtube.com', 'www.youtube.com']:
            if url.path in ['/watch', '/watch/']:
                query = parse_qs(url.query)
                if 'v' in query:
                    return query['v'][0]
            elif re.fullmatch(r'/watch/[a-zA-Z0-9]+', url.path):
                return url.path[len('/watch/'):]
        return None


class GoogleDriveMetaDataProvider(MetaDataProvider):
    def __init__(self, share_link):
        super().__init__(share_link)
        self._file_id = GoogleDriveMetaDataProvider.drive_file_id_from_share_url(share_link)

        if not self._file_id:
            raise VideoNotFoundException

        # Check API Key
        if 'GOOGLE_API_KEY' not in os.environ:
            raise APIUnauthorizedException

        # Init Google API
        try:
            self._drive = googleapiclient.discovery.build(
                'drive', 'v3', developerKey=os.environ['GOOGLE_API_KEY'], cache_discovery=False)
        except HttpError as e:
            if e.resp.status in [400, 401, 403]:
                raise APIUnauthorizedException
            else:
                raise e

    def get_meta_data(self):
        # Get meta data for file
        try:
            file_meta = self._drive.files().get(fileId=self._file_id).execute()
        except HttpError as e:
            if e.resp.status in [400, 401, 403]:
                raise VideoUnauthorizedException
            elif e.resp.status in [404,]:
                raise VideoNotFoundException
            else:
                raise e

        # Set the metadata
        self.video_meta_data["title"] = file_meta["name"]
        self.video_meta_data["mimeType"] = file_meta["mimeType"]

        # This is inv of the table in the frontend
        mime2ext = {
            "application/x-mpegURL": 'm3u8',
            'video/mp4': 'mp4',
            'video/ogg': 'ogg',
            'video/webm': 'webm',
        }

        # Get stream url from API
        file_download_url = json.loads(self._drive.files().get_media(fileId=self._file_id).to_json())['uri']
        self.video_meta_data["streamUrl"] = f"{file_download_url}&l2g_media_type={mime2ext[file_meta['mimeType']]}"

        return super().get_meta_data()

    @staticmethod
    def drive_file_id_from_share_url(share_url):
        """
        Converts a google drive share link into a google drive file id
        """
        url = urlparse(share_url)
        if url.hostname in ['drive.google.com',]:
            if re.fullmatch(r'/file/d/[a-zA-Z0-9-_]+/view', url.path):
                return url.path[len('/file/d/'):-len("/view")]
        return None
