from zope import interface

from toutpt.photomanager import interfaces

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
            photo.sets.append(self)
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
