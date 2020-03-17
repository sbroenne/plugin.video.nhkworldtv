import xbmcgui
import utils
from datetime import datetime, timedelta


class Episode(object):
    """ NHK Episode that contains all the necessary informaton
    to convert itself into a Kodi ListItem"""
    def __init__(self):
        """ Creates an Episode instance """
        self.vod_id = None
        self.pgm_no = None
        self.title = None
        self.plot = None
        self.duration = None
        self.video_info = None
        self.url = None
        self.IsPlayable = False
        self._broadcast_start_date = None
        self._broadcast_end_date = None
        self._thumb = None
        self._fanart = None
        self._kodi_list_item = None
  

    #
    # Properties
    #

    @property
    def broadcast_start_date(self):
        """ Gets the current broadcast start date in local timezone """
        return self._broadcast_start_date

    @broadcast_start_date.setter
    def broadcast_start_date(self, value):
        """ Sets the current broadcast start date from the timestamp value """
        timestamp = int(value) // 1000
        local_date = utils.to_local_time(timestamp)
        self._broadcast_start_date = local_date

    @property
    def broadcast_end_date(self):
        """ Gets the current broadcast end date in local timezone """
        return self._broadcast_end_date

    @broadcast_end_date.setter
    def broadcast_end_date(self, value):
        """ Sets the current broadcast end date from the timestamp value """
        timestamp = int(value) // 1000
        local_date = utils.to_local_time(timestamp)
        self._broadcast_end_date = local_date

    @property
    def thumb(self):
        """ Gets the thumbnail URL """
        return self._thumb

    @thumb.setter
    def thumb(self, value):
        """ Sets thumbnail URL """
        if 'https://' in value:
            self._thumb = value
        else:
            self._thumb = utils.get_NHK_website_url(value)

    @property
    def fanart(self):
        """ Gets the fanart URL """
        return self._fanart

    @fanart.setter
    def fanart(self, value):
        """ Sets thumbnail URL """
        if 'https://' in value:
            self._fanart = value
        else:
            self._fanart = utils.get_NHK_website_url(value)

    @property
    def kodi_list_item(self):
        """ Gets the current Kodi List Item """

        info_labels = {}
        if (self.url is not None):
            # Path was provided - created the ListItem with path
            self._kodi_list_item = xbmcgui.ListItem(path=self.url)
        else:
            # Create ListItem with title
            self._kodi_list_item = xbmcgui.ListItem(self.title)

        if (self.IsPlayable):
            # Playable episode
            self._kodi_list_item.setProperty('IsPlayable', 'true')

        self._kodi_list_item.setArt({
            'thumb': self.thumb,
            'fanart': self.fanart
        })
        
        # Add Kodi InfoLabels
        info_labels = {}
        info_labels['mediatype'] = 'episode'
        info_labels['plot'] = self.plot
        info_labels['title'] = self.title
        self._kodi_list_item.setInfo('video',info_labels)
       
        # Only add Stream Info if the the video_info property is not none
        if (self.video_info is not None):
            self._kodi_list_item.addStreamInfo('video', self.video_info)

        return self._kodi_list_item
