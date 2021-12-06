#OUTDATED - use jupiter notebook
import aql_features
from AQL import AQL

features = [
    ("command_classification", aql_features.classify_audio),
    ("tempo", aql_features.find_tempo),
    ("sample_rate", aql_features.get_sample_rate)
]

aql_database = AQL("audio.db", "audio", features)
aql_database.insert_batch("audioFiles")