import os

from mongoengine import Document, EmbeddedDocument, fields, connect
from pymongo import UpdateOne

connect(
    db=os.environ.get("MONGO_INITDB_DATABASE"),
    username=os.environ.get("MONGO_INITDB_ROOT_USERNAME"),
    password=os.environ.get("MONGO_INITDB_ROOT_PASSWORD"),
    host="mongo_db",
    port=27017,
    authentication_source="admin",
)


class Area(EmbeddedDocument):
    area_id = fields.IntField()
    name = fields.StringField()
    code = fields.StringField()
    flag = fields.StringField()


class Competition(EmbeddedDocument):
    competition_id = fields.IntField()
    name = fields.StringField()
    code = fields.StringField()
    type = fields.StringField()
    emblem = fields.StringField()


class Season(EmbeddedDocument):
    season_id = fields.IntField()
    startDate = fields.DateTimeField()
    endDate = fields.DateTimeField()
    currentMatchday = fields.IntField()
    winner = fields.StringField(required=False)


class Team(EmbeddedDocument):
    team_id = fields.IntField()
    name = fields.StringField()
    shortName = fields.StringField()
    tla = fields.StringField()
    crest = fields.StringField()


class ScoreDetails(EmbeddedDocument):
    home = fields.IntField(required=False, null=True)
    away = fields.IntField(required=False, null=True)


class Score(EmbeddedDocument):
    winner = fields.StringField()
    duration = fields.StringField()
    fullTime = fields.EmbeddedDocumentField(ScoreDetails)
    halfTime = fields.EmbeddedDocumentField(ScoreDetails)


class Referee(EmbeddedDocument):
    referee_id = fields.IntField(required=False)
    name = fields.StringField()
    type = fields.StringField()
    nationality = fields.StringField()


class Match(Document):
    id = fields.IntField(primary_key=True)
    area = fields.EmbeddedDocumentField(Area)
    competition = fields.EmbeddedDocumentField(Competition)
    season = fields.EmbeddedDocumentField(Season)
    utcDate = fields.DateTimeField()
    status = fields.StringField()
    matchday = fields.IntField()
    stage = fields.StringField()
    group = fields.StringField(required=False, null=True)
    lastUpdated = fields.DateTimeField()
    homeTeam = fields.EmbeddedDocumentField(Team)
    awayTeam = fields.EmbeddedDocumentField(Team)
    score = fields.EmbeddedDocumentField(Score)
    odds = fields.DictField()
    referees = fields.ListField(fields.EmbeddedDocumentField(Referee), default=[])

    meta = {"collection": "matches"}

    @classmethod
    def bulk_upsert(cls, matches):
        bulk_operations = [
            UpdateOne(
                {"id": match["id"]},
                {"$set": match},
                upsert=True,
            )
            for match in matches
        ]

        if bulk_operations:
            results = cls._get_collection().bulk_write(bulk_operations)
            return {
                "Upserted": results.bulk_api_result.get("nUpserted", 0),
                "Matched": results.bulk_api_result.get("nMatched", 0),
                "Modified": results.bulk_api_result.get("nModified", 0),
            }
        return None
