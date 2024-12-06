import logging
from typing import List

from buco_db_controller.mongo_db.mongo_db_repository import MongoDBBaseRepository

logger = logging.getLogger(__name__)


class TeamLeguesRepository(MongoDBBaseRepository):
    DB_NAME = 'api_football'

    def __init__(self):
        super().__init__(self.DB_NAME)

    def upsert_many_team_leagues(self, team_leagues: list):
        self.bulk_upsert_documents('team_leagues', team_leagues)
        logger.info('Upserted fixture lineups data')

    def get_team_league(self, team_id: int, season: int) -> dict:
        query = {'parameters.team': team_id, 'parameters.season': season}

        lineups = self.find_document('team_leagues', query)
        return lineups
