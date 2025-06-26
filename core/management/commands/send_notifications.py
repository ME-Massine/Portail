from django.core.management.base import BaseCommand
from django.utils import timezone
from core.signals import create_assignment_due_notifications, create_system_notifications


class Command(BaseCommand):
    help = 'Send scheduled notifications (assignment due reminders, etc.)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['assignment_due', 'system', 'all'],
            default='all',
            help='Type of notifications to send'
        )

    def handle(self, *args, **options):
        notification_type = options['type']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting notification process for type: {notification_type}')
        )
        
        if notification_type in ['assignment_due', 'all']:
            self.stdout.write('Creating assignment due notifications...')
            create_assignment_due_notifications()
            self.stdout.write(
                self.style.SUCCESS('Assignment due notifications created successfully')
            )
        
        if notification_type in ['system', 'all']:
            self.stdout.write('Creating system notifications...')
            create_system_notifications()
            self.stdout.write(
                self.style.SUCCESS('System notifications created successfully')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Notification process completed successfully')
        ) 