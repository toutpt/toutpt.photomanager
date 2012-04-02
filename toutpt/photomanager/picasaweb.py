from zope import component
from zope import interface
from toutpt.photomanager import interfaces
from toutpt.photomanager import core
from toutpt.photomanager.logger import logger
import gdata.photos, gdata.photos.service


class PicasawebPhotoSet(core.PhotoSet):
    
    def __init__(self):
        super(PicasawebPhotoSet,self).__init__()
        self.pws = None
        self.raw_album = None
        self._photos = []


    def get_photos(self):
        if self._photos:
            return self._photos

        photos = []
        raw_photos = self.pws.GetFeed(self.raw_album.GetPhotosUri()).entry
        for raw_photo in raw_photos:
            photo = core.Photo()
            photo.id = raw_photo.gphoto_id.text
            photo.uri = raw_photo.content.src
            photo.title = raw_photo.title.text
            photo.description = raw_photo.summary.text or ''
#            tags = self.pws.GetFeed(raw_photo.GetTagsUri()).entry
#            photo.tags = [tag.summary.text for tag in tags]
            photos.append(photo)

        self.add_photos(photos)

        logger.info('%s photos found in %s'%(len(raw_photos), self.uri))

        return self._photos
    
    def update(self):
        self.uri = self.raw_album.GetAlternateLink().href
        self.title = self.raw_album.title.text


class PicasawebPhotoManager(object):
    """PhotoManager implementation for picasaweb"""

    interface.implements(interfaces.IPhotoManager)

    def __init__(self):
        self._uris = {}
        self.pws = gdata.photos.service.PhotosService()

    def get_photoset(self, uri):
        """REturn a IPhotoSet"""
        self.update()
        return self._uris.get(uri, None)

    def new_photoset(self):
        """Create a new instance of IPhotoSet"""
        return PicasawebPhotoSet()

    def all_photosets(self):
        """Return a set of all registred albums"""
        self.update()
        return self._uris.values()

    def update(self):
        if self._uris:
            return self._uris

        logger.info('load albums')
        raw_albums = self.pws.GetUserFeed().entry
        for raw_album in raw_albums:
            album = self.new_photoset()
            album.raw_album = raw_album
            album.pws = self.pws
            album.update()
            self.add_photoset(album)
        
        logger.info('%s albums loaded'%len(self._uris))

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
