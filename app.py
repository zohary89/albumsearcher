from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
     return render_template('index.html')


@app.route('/albums', methods =['GET'])
def albums():
    artist_name = request.args.get('artist').title()
    albums_resp = requests.get(f'http://theaudiodb.com/api/v1/json/1/searchalbum.php?s={artist_name}')
    albums_resp_json = albums_resp.json()
    artist_resp = requests.get(f'http://theaudiodb.com/api/v1/json/1/search.php?s={artist_name}')
    artist_resp_json = artist_resp.json()
    if albums_resp_json['album'] is None:
      return redirect(url_for('index'))
    albums = albums_resp_json['album']
    artist = artist_resp_json['artists']
    sorted_albums = sorted(albums, key=lambda k: k["intYearReleased"], reverse=True) 
    return render_template(
      'results.html',
      ARTIST_NAME=artist_name,
      all_albums=sorted_albums,
      artist_info=artist,
    )


@app.route('/albums/<album_id>')
def album(album_id):
  album_resp = requests.get(f'https://theaudiodb.com/api/v1/json/1/album.php?m={album_id}')
  tracks_resp = requests.get(f'https://theaudiodb.com/api/v1/json/1/track.php?m={album_id}')
  album_resp_json = album_resp.json()
  tracks_resp_json = tracks_resp.json()
  if album_resp_json['album'] is None:
     return redirect(url_for('index'))
  album_info = album_resp_json['album'][0]
  tracks_info = tracks_resp_json['track']
  return render_template(
      'album.html',
      album_info=album_info,
      tracks_info=tracks_info
    )


if __name__ == '__main__':
    app.run(debug=True)

