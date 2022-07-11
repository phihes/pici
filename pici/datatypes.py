from enum import Enum


class CommunityDataLevel(Enum):
    """
    View on community.

    TODO:
        Document properly
    """
    POSTS = "posts"
    TOPICS = "topics"
    CONTRIBUTORS = "contributors"
    COMMUNITY = "community"


class MetricReturnType(Enum):
    """
    Category of representation of metrics' return type.
    """

    PLAIN = "plain"
    """
    Metric's original return value (not modified).
    """
    TABLE = "table"
    """
    Metric's return value(s) in table format.
    """
    DATAFRAME = "dataframe"
    """
    Metric's return values as series in Pandas.Dataframe
    """