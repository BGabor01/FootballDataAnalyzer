from mongoengine import Document, EmbeddedDocument, fields, ObjectIdField


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
