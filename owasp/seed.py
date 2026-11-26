from django.contrib.auth.models import User
from django.db import connection

from flaws.models import Account

# delete existing accounts
User.objects.filter(is_superuser=False).delete()


# Reset ID counters
with connection.cursor() as cursor:
    cursor.execute("""
        DELETE FROM sqlite_sequence
        WHERE name IN ('auth_user', 'flaws_account')
    """)


alice = User.objects.create_user(username='alice', password='12345')

bob = User.objects.create_user(username='bob', password='12345')

charlie = User.objects.create_user(username='charlie', password='12345')


# Create accounts
Account.objects.create(user=alice, balance=1000)
Account.objects.create(user=bob, balance=500)
Account.objects.create(user=charlie, balance=250)
