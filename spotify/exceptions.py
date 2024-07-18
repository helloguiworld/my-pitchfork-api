class InvalidSpotifyToken(Exception):
    def __init__(self, message="Spotify access token is invalid or expired"):
        self.message = message
        super().__init__(self.message)