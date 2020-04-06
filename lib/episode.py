from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import object
from kodi_six import xbmcgui
from . import utils


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
        self.aspect = None
        self.width = None
        self.height = None
        self.url = None
        self.IsPlayable = False
        self.playcount = None
        self._date = None
        self._year = None
        self._broadcast_start_date = None
        self._broadcast_end_date = None
        self._thumb = None
        self._fanart = None
        self._video_info = None
        self._kodi_list_item = xbmcgui.ListItem
        self.absolute_image_url = False

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
        if ('/nhkworld/' in value and not self.absolute_image_url):
            self._thumb = utils.get_NHK_website_url(value)
        else:
            self._thumb = value

    @property
    def fanart(self):
        """ Gets the fanart URL """
        return self._fanart

    @fanart.setter
    def fanart(self, value):
        """ Sets thumbnail URL """
        if ('/nhkworld/' in value and not self.absolute_image_url):
            self._fanart = utils.get_NHK_website_url(value)
        else:
            self._fanart = value

    @property
    def date(self):
        """ Get the sort date in Kodi date format """
        if (self._date is not None):
            return self._date.strftime('%d/%m/%Y')
        else:
            return None

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def year(self):
        if (self._date is not None):
            self._year = self._date.strftime('%Y')
            return self._year
        else:
            return None

    @property
    def video_info(self):
        if (self._video_info is not None):
            return self._video_info
        elif (self.aspect is not None):
            vi = {
                'aspect': self.aspect,
                'width': self.width,
                'height': self.height
            }
            self._video_info = vi
            return vi

        else:
            return None

    @video_info.setter
    def video_info(self, value):
        self._video_info = value

    @property
    def kodi_list_item(self):
        """ Gets the current Kodi List Item """

        if (self.url is not None):
            # Path was provided - created the ListItem with path
            li = xbmcgui.ListItem(path=self.url)
            li.setLabel(self.title)
        else:
            # Create ListItem with title
            li = xbmcgui.ListItem(self.title)

        if (self.IsPlayable):
            # Playable episode
            li.setProperty('IsPlayable', 'true')

        li.setArt({'thumb': self.thumb, 'fanart': self.fanart})

        # Add Kodi InfoLabels
        info_labels = {}
        info_labels['mediatype'] = 'episode'
        info_labels['Plot'] = self.plot
        info_labels['Title'] = self.title

        if (self.duration is not None):
            info_labels['Duration'] = self.duration

        if (self.pgm_no is not None):
            info_labels['Episode'] = self.pgm_no

        if (self.year is not None):
            info_labels['Year'] = self.year

        if (self._date is not None):
            info_labels['Date'] = self.date

        if (self.playcount is not None):
            info_labels['playcount'] = self.playcount

        li.setInfo('video', info_labels)

        # Only add Stream Info if the the video_info property is not none
        if (self.video_info is not None):
            li.addStreamInfo('video', self.video_info)

        self._kodi_list_item = li

        return self._kodi_list_item
