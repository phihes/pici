from pici.decorators import report
from pici.metrics.basic import *
from pici.metrics.network import *
from pici.metrics.text import *


@report(
    level=CommunityDataLevel.COMMUNITY,
    returntype=MetricReturnType.TABLE
)
def summary(communities):
    return [
        (number_of_posts, {}),
        (agg_number_of_posts_per_interval, {'interval': '1d'}),
        (agg_number_of_posts_per_interval, {'interval': '1M'}),
        (agg_posts_per_topic, {})
    ]