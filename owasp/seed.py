from django.contrib.auth.models import User

from flaws.models import Account

# delete existing accounts
User.objects.filter(is_superuser=False).delete()


alice = User.objects.create_user(username='alice', password='1245')

bob = User.objects.create_user(username='bob', password='1245')

charlie = User.objects.create_user(username='charlie', password='12345')


# Create accounts
Account.objects.create(user=alice, balance=1000)
Account.objects.create(user=bob, balance=500)
Account.objects.create(user=charlie, balance=250)
