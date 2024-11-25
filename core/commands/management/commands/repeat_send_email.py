import os
import json
from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from library.serializers import EmailSerializer

class Command(BaseCommand):
    help = 'Комманда для надоедания человеку письмами'

    def add_arguments(self, parser):
        parser.add_argument('switcher', 
                            type=str,
                            help='up - up task; \n \
                                down - down task')
        parser.add_argument('--email', 
                            type=str,
                            help='input email',
                            required=False)
        parser.add_argument('--time', 
                            type=int,
                            help='input time',
                            required=False)

    def handle(self, *args, **options):
        switcher: str = options['switcher']
        try:
            match switcher:
                case 'up':
                    email: str = str(os.getenv('EMAIL') if not options.get('time') else options['email'])
                    serializer: EmailSerializer = EmailSerializer(data={'email': email})
                    if not serializer.is_valid():
                        raise CommandError('Данные не валидны')
                    time = int(os.getenv('MINUTES', 1) if not options.get('time') else options['time'])
                    if time<0: time = 1
                    schedule, _ = IntervalSchedule.objects.update_or_create(
                        every=time,
                        period=IntervalSchedule.MINUTES
                    )
                    _ , created = PeriodicTask.objects.update_or_create(
                        interval=schedule,
                        name="Отправка писем",
                        task="send_email",
                        kwargs=json.dumps({'email':email})
                    )        
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Задача успешно создана на {time} минут.'))
                    else:
                        self.stdout.write(self.style.SUCCESS('Задача обновлена.'))
                case 'down': 
                    PeriodicTask.objects.filter(name='Отправка писем').delete()
                    
                    self.stdout.write(self.style.SUCCESS('Задача успешно прекращена.'))
        except Exception as e:
            raise CommandError(f'Ошибка выполнения команды: {e}')