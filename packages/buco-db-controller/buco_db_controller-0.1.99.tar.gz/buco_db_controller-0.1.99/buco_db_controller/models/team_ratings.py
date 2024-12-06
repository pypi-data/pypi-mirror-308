

class TeamRatings:
    def __init__(self, league_id: int, season: int, team_ratings: dict):
        self.league_id: int = league_id
        self.season: int = season
        self.team_ratings: dict = team_ratings

    @classmethod
    def from_dict(cls, response):
        league_id = response['parameters']['league']
        season = response['parameters']['season']
        team_ratings = response['data']

        return cls(league_id=league_id, season=season, team_ratings=team_ratings)
