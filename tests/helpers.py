import json


def get_json(res):
    """Return json response as a dictionary or list."""
    return json.loads(res.data)


user1 = {
    'email': 'montaro@gmail.com',
    'password': 'password'
}

user2 = {
    'email': 'kenpachi@bleach.com',
    'password': 'bankai'
}

admin = {
    'email': 'admin@example.com',
    'password': 'iamadmin'
}

cat1 = {'name': 'codility'}

cat2 = {'name': 'hackerrank'}

algo1 = {
    'title': 'Binary Sort',
    'content': 'print("hi")',
    'category': '1',
    'sub_category': 'sorting'
}

algo2 = {
    'title': 'Binary Search',
    'sub_category': 'searching'
}
