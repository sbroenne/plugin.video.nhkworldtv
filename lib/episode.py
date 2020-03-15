import xbmcgui

class Episode():
    """ NHK Episode that contains all the necessary informaton
    to convert it into a Kodi ListItem"""

    def __init__(self, vod_id="", title="", plot="", thumb="", fanart="", video_info=None):
        """ Creates an Episode instance. All parameters are optional """
        self.vod_id = vod_id
        self.title = title
        self.plot = plot
        self.thumb = thumb
        self.fanart= fanart
        self.video_info = video_info
        self.kodi_list_item = xbmcgui.ListItem(self.title)

    def update_kodi_list_item(self):
        """ Updates the Kodi List Item propety with the latest values"""
        self.kodi_list_item.setLabel = self.title
        self.kodi_list_item = xbmcgui.ListItem(self.title)
        self.kodi_list_item.setArt({'thumb': self.thumb, 'fanart': self.fanart})
        self.kodi_list_item.setInfo('video', {'mediatype': 'episode', 'plot': self.title})
        # Only add Stream Info if the the video_info property is not none
        if (self.video_info is not None):
             self.kodi_list_item.addStreamInfo('video', self.video_info)
        
    
