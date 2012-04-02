from getpass import getpass
from toutpt.photomanager import picasaweb

def main():
    pm = picasaweb.PicasawebPhotoManager() #getUtility

    username=raw_input('User name: ')
    password = getpass('Password : ')
    
    pm.login(username, password)
    albums = pm.all_photosets()
    for album in albums:
        photos = album.import_photos()
