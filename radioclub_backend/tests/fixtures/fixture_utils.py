import pandas as pd
import pytest

CSV_DATA = {
    ''
}


@pytest.fixture
def csv_file(tmpdir_factory):
    dataframe = pd.DataFrame(CSV_DATA, index=range(len(CSV_DATA[...])))
    filename = str(tmpdir_factory.mktemp('data').join('data.csv'))
    dataframe.to_csv(filename)
    return filename
