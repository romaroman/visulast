from visulast.core import models


def does_user_exist(username):
    return True if models.UserModel(username) else False


def does_album_exist(artist_name, title):
    return True if models.AlbumModel(artist_name, title) else False


def does_artist_exist(name):
    return True if models.ArtistModel(name) else False


def does_tag_exist(name):
    return True if models.TagModel(name) else False


def does_track_exist(artist_name, track_title):
    return True if models.TrackModel(artist_name, track_title) else False
