from django.core.management.base import BaseCommand
from core.services import NotificationService


class Command(BaseCommand):
    help = 'Clean up old notifications from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete notifications older than this many days (default: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        days_old = options['days']
        dry_run = options['dry_run']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting notification cleanup for notifications older than {days_old} days')
        )
        
        if dry_run:
            from django.utils import timezone
            from datetime import timedelta
            from core.models import Notification
            
            cutoff_date = timezone.now() - timedelta(days=days_old)
            old_notifications = Notification.objects.filter(
                date_creation__lt=cutoff_date,
                lu=True
            )
            count = old_notifications.count()
            
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would delete {count} old notifications')
            )
            
            if count > 0:
                self.stdout.write('Sample notifications that would be deleted:')
                for notification in old_notifications[:5]:
                    self.stdout.write(f'  - {notification.titre} ({notification.date_creation})')
        else:
            deleted_count = NotificationService.cleanup_old_notifications(days_old)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {deleted_count} old notifications')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Notification cleanup completed')
        ) 