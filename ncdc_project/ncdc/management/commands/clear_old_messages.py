from django.core.management.base import BaseCommand
from ncdc.models import ChatMessage
from datetime import timedelta
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Delete chat messages older than 24 hours"

    def handle(self, *args, **kwargs):
        cutoff = now() - timedelta(hours=24)
        deleted_count, _ = ChatMessage.objects.filter(timestamp__lt=cutoff).delete()
        self.stdout.write(f"{deleted_count} old messages cleared.")
