from buco_db_controller.models.team_ratings import TeamRatings
from buco_db_controller.repositories.team_ratings_repository import TeamRatingsRepository


class TeamRatingsService:
    def __init__(self):
        self.team_ratings_repository = TeamRatingsRepository()

    def upsert_many_team_ratings(self, team_ratings: list):
        self.team_ratings_repository.upsert_many_team_ratings(team_ratings)

    def insert_team_ratings(self, team_ratings: dict):
        self.team_ratings_repository.insert_team_ratings(team_ratings)

    def get_team_ratings(self, league_id: int, season: int) -> TeamRatings:
        response = self.team_ratings_repository.get_team_ratings(league_id, season)
        return TeamRatings.from_dict(response)
