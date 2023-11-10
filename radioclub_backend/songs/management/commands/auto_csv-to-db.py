from django.conf import settings
from django.core.management.base import BaseCommand

from songs.management.utils import SongLoadCsvData


class Command(BaseCommand):
    REL_CSV_DIR = 'static/data/csv/'
    CSV_DIR = str(settings.BASE_DIR / REL_CSV_DIR) + '/'

    help = f'''
        Команда автоматически переводит данные из {CSV_DIR}
        в соответствующие таблицы в базе данных.
    '''
    FILE_TO_MODEL = {
        'songs':
            (
                ('albums.csv', 'Album',
                 ('id', 'cover', 'title', 'description',
                  'published_year', 'slug'),
                 ('cover',)
                 ),
            ),
    }

    def handle(self, *args, **options):
        app_models = (
            ('songs', SongLoadCsvData),
        )
        for app in app_models:
            for data in self.FILE_TO_MODEL[app[0]]:
                file_path = self.CSV_DIR + data[0]
                class_name = data[1]
                print(file_path, class_name)
                load_instance = app[1](
                    file_path,
                    class_name,
                    data[2],
                    data[3],
                )

                self.stdout.write(
                    'Loading data from "%s" to database' % file_path
                )
                load_instance.load_data()
                self.stdout.write(
                    'Done!'
                )
