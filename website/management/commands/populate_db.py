from django.core.management.base import BaseCommand
from database.models import MemberShip


class Command(BaseCommand):

    def _create_memberships(self):
        member = MemberShip(id=1, title="free", kind="1")
        member.save()
        member = MemberShip(id=2, title="Premium", kind="5")
        member.save()
        member = MemberShip(id=3, title="Admin", kind="10")
        member.save()
        member = MemberShip(id=4, title="TEST", kind="00")
        member.save()

    def handle(self, *args, **options):
        self._create_memberships()
