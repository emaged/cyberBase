# run after seeding to check the current password hash
# run before and after applying fix 2 to see different password hashes

# python manage.py shell < passwordHash.py


from time import perf_counter

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

alice = User.objects.get(username='alice')
password_hash = alice.password

print(password_hash)

start = perf_counter()
result = check_password('12345', password_hash)
end = perf_counter()

print(f'Password matches: {result}')
print(f'Time taken: {end - start:.8f} seconds')
