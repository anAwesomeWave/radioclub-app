from abc import ABC
import csv
import os

from django.core.files import File

from songs import models as song_models


class BaseLoadCsvData(ABC):
    """ Base abstract class for loading data from csv to db."""

    def __init__(self, file_path, field_names, file_fields):
        # принимает путь до csv файла и список колонок, в которые будут
        # записаны данные (порядок важен)
        self.file_path = file_path
        # self.model = getattr(r_models, model_name)
        self.field_names = field_names
        self.file_fields = file_fields

    def load_data(self):
        if os.path.isfile(self.file_path) and self.file_path.endswith('.csv'):
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                if self.field_names is not None:
                    headers = self.field_names
                for row in reader:
                    data = dict(zip(headers, row))
                    # convert path of file to file
                    for file_field in self.file_fields:
                        if file_field in data:
                            data[file_field] = File(
                                open(data[file_field], 'rb'),
                                name=data[file_field].split('/')[-1]
                            )
                    id = {'id': int(data.pop('id'))}
                    print(data)
                    _, created = self.model.objects.get_or_create(
                        **id,
                        defaults=data,
                    )
        else:
            raise ValueError(
                f'File "{self.file_path}" has '
                f'inappropriate format or doesn\'t exist'
            )


class SongLoadCsvData(BaseLoadCsvData):
    """ Class for loading data for 'songs' app. """

    def __init__(self, file_path, model_name, field_names, file_fields):
        super().__init__(file_path, field_names, file_fields)
        # get model instance from song app
        self.model = getattr(song_models, model_name)
