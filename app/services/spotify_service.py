"""
Spotify metadata service using official Spotify Web API.
"""
import os
from typing import Dict, List
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables
load_dotenv()


class SpotifyService:
    """Service for fetching Spotify metadata using official API."""
    
    def __init__(self):
        """Initialize Spotify API client."""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            raise ValueError(
                "Spotify credentials not found. "
                "Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env file"
            )
        
        # Authenticate with Spotify
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
    
    def get_track_metadata(self, spotify_url: str) -> Dict[str, str]:
        """
        Get track metadata from Spotify URL using API.
        
        Args:
            spotify_url: Spotify track URL
            
        Returns:
            Dictionary with track metadata
        """
        try:
            # Extract track ID from URL
            track_id = self._extract_id_from_url(spotify_url, 'track')
            
            # Fetch track data from API
            track = self.sp.track(track_id)
            
            # Extract metadata
            artists = ', '.join([artist['name'] for artist in track['artists']])
            album = track['album']['name']
            year = track['album']['release_date'][:4] if track['album'].get('release_date') else ''
            cover_url = track['album']['images'][0]['url'] if track['album']['images'] else ''
            
            return {
                "name": track['name'],
                "artist": artists,
                "album": album,
                "year": year,
                "duration": track['duration_ms'],
                "track_id": track['id'],
                "cover_url": cover_url
            }
            
        except Exception as e:
            raise Exception(f"Failed to fetch Spotify track metadata: {str(e)}")
    
    def get_playlist_tracks(self, playlist_url: str) -> List[Dict[str, str]]:
        """
        Get all tracks from a Spotify playlist using API.
        
        Args:
            playlist_url: Spotify playlist URL
            
        Returns:
            List of track metadata dictionaries
        """
        try:
            # Extract playlist ID from URL
            playlist_id = self._extract_id_from_url(playlist_url, 'playlist')
            
            tracks = []
            offset = 0
            limit = 100  # Max allowed by Spotify API
            
            while True:
                # Fetch playlist tracks (paginated)
                results = self.sp.playlist_tracks(
                    playlist_id,
                    offset=offset,
                    limit=limit,
                    fields='items(track(name,artists,album,duration_ms,id)),next'
                )
                
                # Extract track metadata
                for item in results['items']:
                    if item['track'] is None:
                        continue  # Skip deleted/unavailable tracks
                    
                    track = item['track']
                    artists = ', '.join([artist['name'] for artist in track['artists']])
                    album = track['album']['name']
                    year = track['album']['release_date'][:4] if track['album'].get('release_date') else ''
                    cover_url = track['album']['images'][0]['url'] if track['album']['images'] else ''
                    
                    tracks.append({
                        "name": track['name'],
                        "artist": artists,
                        "album": album,
                        "year": year,
                        "duration": track['duration_ms'],
                        "track_id": track['id'],
                        "cover_url": cover_url
                    })
                
                # Check if there are more tracks
                if results['next'] is None:
                    break
                
                offset += limit
            
            if not tracks:
                raise ValueError("No tracks found in playlist")
            
            return tracks
            
        except Exception as e:
            raise Exception(f"Failed to fetch playlist: {str(e)}")
    
    def get_album_tracks(self, album_url: str) -> List[Dict[str, str]]:
        """
        Get all tracks from a Spotify album using API.
        
        Args:
            album_url: Spotify album URL
            
        Returns:
            List of track metadata dictionaries
        """
        try:
            # Extract album ID from URL
            album_id = self._extract_id_from_url(album_url, 'album')
            
            # Fetch album data
            album = self.sp.album(album_id)
            
            tracks = []
            for track in album['tracks']['items']:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                year = album['release_date'][:4] if album.get('release_date') else ''
                cover_url = album['images'][0]['url'] if album['images'] else ''
                
                tracks.append({
                    "name": track['name'],
                    "artist": artists,
                    "album": album['name'],
                    "year": year,
                    "duration": track['duration_ms'],
                    "track_id": track['id'],
                    "cover_url": cover_url
                })
            
            return tracks
            
        except Exception as e:
            raise Exception(f"Failed to fetch album: {str(e)}")
    
    @staticmethod
    def _extract_id_from_url(url: str, resource_type: str) -> str:
        """
        Extract Spotify ID from URL.
        
        Args:
            url: Spotify URL
            resource_type: Type of resource (track, playlist, album)
            
        Returns:
            Spotify ID
        """
        # Remove query parameters
        url = url.split('?')[0]
        
        # Extract ID from URL
        # Format: https://open.spotify.com/{type}/{id}
        parts = url.rstrip('/').split('/')
        
        if len(parts) >= 2 and parts[-2] == resource_type:
            return parts[-1]
        
        raise ValueError(f"Invalid Spotify {resource_type} URL: {url}")