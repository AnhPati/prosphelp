from constants.labels import *
from constants.schema.columns import *

MARKET_FIELDS = [
    {"key": COL_MARKET, "label": FIELD_MARKET_EXISTING, "type": "select"},
    {"key": "new_market", "label": FIELD_MARKET_NEW, "type": "text"},
    {"key": COL_DATE, "label": FIELD_DATE, "type": "date"},
    {"key": COL_NUMBER_OF_OFFERS, "label": FIELD_NUMBER_OF_OFFERS, "type": "number"},
    {"key": COL_NOTES, "label": FIELD_NOTES, "type": "text"}
]
