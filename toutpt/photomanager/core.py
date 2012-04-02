from zope import interface

from toutpt.photomanager import interfaces
import os
import urllib
from toutpt.photomanager.logger import logger

class Photo(object):
    """Base photo object"""
    
    def __init__(self):
        self.id = None
        self.title = ""
        self.description = ""
        self.tags = []
        self.uri = None
        self.albums = []

class PhotoSet(object):
    """Base photo set"""
    
    def __init__(self):
        self._photos = []
        self._uris = {}
        self.uri = None

    def add_photos(self, photos):
        for photo in photos:
            photo.albums.append(self)
            self._photos.append(photo)
            self._uris[photo.uri] = photo

    def remove_photos(self, uris):
        for uri in uris:
            photo = self._uris.get(uri,None)
            if photo is None:
                continue
            index = self._photos.index(photo)
            del self._photos[index]
            del self._uris[uri]

    def get_photos(self):
        return self._uris.values()

    def import_photos(self):
        photos = self.get_photos()
        if not self.title:
            raise ValueError('photo set must have a title')
        os.mkdir(self.title)
        cwd = os.getcwd()
        albumpath = '%s/%s'%(cwd,self.title)
        for photo in photos:
            logger.info('start download %s'%photo.title)
            urllib.urlretrieve(photo.uri,
                               '%s/%s'%(albumpath, photo.title))
            logger.info('%s downloaded'%photo.title)
