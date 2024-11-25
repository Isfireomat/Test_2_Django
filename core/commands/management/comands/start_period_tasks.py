
# from django.core.management.base import BaseCommand, CommandError
# from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
# from users.models import User

# class Command(BaseCommand):
#     help = 'Комманда для парсинга сайтов в 00:00 по UTC'

#     def add_arguments(self, parser):
#         parser.add_argument('switcher', 
#                             type=str,
#                             choices=['up', 'down'],
#                             help='up - up task; \n \
#                                 down - down task')

#     def handle(self, *args, **options):
#         switcher: str = options['switcher']
#         try:
#             match switcher:
#                 case 'up':
#                     schedule, _ = CrontabSchedule.objects.get_or_create(
#                         minute=0,
#                         hour=0,
#                     )
#                     task, created = PeriodicTask.objects.update_or_create(
#                         crontab=schedule,
#                         name="Парсинг сайтов в 00:00 по UTC",
#                         task="parsing_all",
#                     )        
#                     if created:
#                         self.stdout.write(self.style.SUCCESS('Задача успешно создана.'))
#                     else:
#                         self.stdout.write(self.style.SUCCESS('Задача обновлена.'))
#                 case 'down': 
#                     PeriodicTask.objects.filter(name='Парсинг сайтов в 00:00 по UTC').delete()
#                     self.stdout.write(self.style.SUCCESS('Задача успешно создана.'))
#         except Exception as e:
#             raise CommandError(f'Ошибка выполнения команды: {e}')