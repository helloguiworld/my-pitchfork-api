from requests import Response

class InvalidSpotifyToken(Exception):
    def __init__(self, message="Spotify access token is invalid or expired"):
        self.message = message
        super().__init__(self.message)

class SpotifyResponseException(Exception):
    def __init__(self, response:Response):
        self.response = response
        self.message = f"Spotify API error: {response.status_code}, {response.text}"
        self.data = {
            'error': self.message,
            'spotify_error': {
                'status': self.response.status_code,
                'text': self.response.text,
            }
        }
        super().__init__(self.message)