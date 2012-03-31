from zope import interface
from zope import schema

class IPhoto(interface.Interface):
    """A photo is a file like object that can be on the current computer
    or on a distant photo service (like flickr).
    """

    uri = schema.URI(title=u"URI")

    sets = schema.List(title=u"Albums")

class IPhotosSet(interface.Interface):
    """A set of photos (album)"""

    uri = schema.URI(title=u"URI")

    photos = schema.List(title=u"Photos")

    def add_photos(photos):
        """Add a list of photo to the photoset"""
    
    def remove_photos(uris):
        """Remove photos"""

class IPhotoManager(interface.Interface):
    """Photo manager is able to search photo, add photo"""

    def get_photoset(uri):
        """REturn a IPhotoSet"""

    def new_photoset():
        """Create a new instance of IPhotoSet"""

    def all_photosets():
        """Return a set of all registred albums"""

    def add_photoset(photoset):
        """register an album"""

    def del_photoset(uri):
        """unregister photoset"""
