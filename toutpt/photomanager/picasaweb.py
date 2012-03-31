from zope import component
from zope import interface
from toutpt.photomanager import interfaces
from toutpt.photomanager import core
import gdata.photos, gdata.photos.service

import logging
logger = logging.getLogger('picasaweb')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

  # Get all photos in second album
#  photos = pws.GetFeed(albums[1].GetPhotosUri()).entry
  # Get all tags for photos in second album and print them
#  tags = pws.GetFeed(albums[1].GetTagsUri()).entry
#  print [ tag.summary.text for tag in tags ]
  # Get all comments for the first photos in list and print them
#  comments = pws.GetCommentFeed(photos[0].GetCommentsUri()).entry
#  print [ c.summary.text for c in comments ]

class PicasawebPhotoSet(core.PhotoSet):
    
    def __init__(self):
        super(PicasawebPhotoSet,self).__init__()
        self.pws = None
        self.raw_album = None

    def update(self):
        self.uri = self.raw_album.GetAlternateLink().href
        raw_photos = self.pws.GetFeed(self.raw_album.GetPhotosUri()).entry
        for raw_photo in raw_photos:
            photo = core.Photo()
            photo.id = raw_photo.gphoto_id.text
            photo.uri = raw_photo.content.src
            photo.title = raw_photo.title.text
            photo.description = raw_photo.summary.text or ''
            tags = self.pws.GetFeed(raw_photo.GetTagsUri()).entry
            photo.tags = [tag.summary.text for tag in tags]

        logger.info('%s photos found in %s'%(len(raw_photos), self.uri))


class PicasawebPhotoManager(object):
    """PhotoManager implementation for picasaweb"""

    interface.implements(interfaces.IPhotoManager)

    def __init__(self):
        self._uris = {}
        self.pws = gdata.photos.service.PhotosService()

    def get_photoset(self, uri):
        """REturn a IPhotoSet"""
        return self._uris.get(uri, None)

    def new_photoset(self):
        """Create a new instance of IPhotoSet"""
        return PicasawebPhotoSet()

    def all_photosets(self):
        """Return a set of all registred albums"""
        return self._uris.values()

    def add_photoset(self, photoset):
        """register an album"""
        self._uris[photoset.uri] = photoset

    def del_photoset(self, uri):
        """unregister photoset"""
        del self._uris[uri]

    def login(self, username, password):
        logger.info('login')
        self.pws.ClientLogin(username, password)
        logger.info('logged in')

    def update(self):
        logger.info('get all albums')
        #load albums
        raw_albums = self.pws.GetUserFeed().entry
        for raw_album in raw_albums:
            logger.info('load album %s'%raw_album.GetAlternateLink().href)
            album = self.new_photoset()
            album.raw_album = raw_album
            album.pws = self.pws
            album.update()

        logger.info('%s albums found'%len(raw_albums))


