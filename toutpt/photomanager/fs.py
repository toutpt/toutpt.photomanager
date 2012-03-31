from zope import component
from zope import interface
from toutpt.photomanager import interfaces
from toutpt.photomanager import core

class FSPhotoManager(object):
    """PhotoManager implementation for filesystem"""
    
    interface.implements(interfaces.IPhotoManager)
    
    def __init__(self):
        self._uris = {}

    def get_photoset(self, uri):
        """REturn a IPhotoSet"""
        return self._uris.get(uri, None)

    def new_photoset():
        """Create a new instance of IPhotoSet"""
        return core.PhotoSet()

    def all_photosets():
        """Return a set of all registred albums"""
        return self._uris.values()

    def add_photoset(photoset):
        """register an album"""
        self._uris[photoset.uri] = photoset

    def del_photoset(uri):
        """unregister photoset"""
        del self._uris[uri]
