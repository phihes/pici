from pici.helpers import where_all
import pandas as pd


def test_where_all():
    df = pd.DataFrame.from_dict({
        'id': [1,2,3,4,5],
        'a': [5,10,15,20,25],
        'b': [500, 499, 498, 497, 496]
    })
    conditions_0 = [
        df['id'] > 1,
        df['a'] < 20
    ]
    conditions_1 = [
        df['id'] > 1,
        df['a'] < 20,
        df['b'] < 499
    ]
    print(df[where_all(conditions_0)])
    assert(df[where_all(conditions_0)].shape[0] == 2)
    assert(df[where_all(conditions_1)].shape[0] == 1)


if __name__ == "__main__":
    test_where_all()
    print("Everything passed")