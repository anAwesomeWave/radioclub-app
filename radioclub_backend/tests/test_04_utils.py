import pytest

from songs.management.utils import SongLoadCsvData


@pytest.mark.django_db(transaction=True)
class TestUtils:
    def test_wrong_filepath(self):
        ''' Test wrong csv path behavior'''
        data_loader = SongLoadCsvData(
            'csv_do_not_exist.csv',
            'Song',
            [],
            []
        )
        with pytest.raises(ValueError):
            data_loader.load_data()
