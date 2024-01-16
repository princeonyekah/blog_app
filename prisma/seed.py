import asyncio
import bcrypt
from prisma import Prisma

client = Prisma()
client.connect()

userData = [
    {
        'name': 'Alice',
        'email': 'alice@prisma.io',
        'password': 'password123',
        'posts': {
            'create': [
                {
                    'title': 'Join the Prisma Slack',
                    'content': 'https://slack.prisma.io',
                },
            ],
        },
    },
    {
        'name': 'Nilu',
        'email': 'nilu@prisma.io',
        'password': 'qazwsx123',
        'posts': {
            'create': [
                {
                    'title': 'Follow Prisma on Twitter',
                    'content': 'https://www.twitter.com/prisma',
                },
            ],
        },
    },
    {
        'name': 'Mahmoud',
        'email': 'mahmoud@prisma.io',
        'password': 'password456',
        'posts': {
            'create': [
                {
                'title': 'Ask a question about Prisma on GitHub',
                'content': 'https://www.github.com/prisma/prisma/discussions',
                },
                {
                'title': 'Prisma on YouTube',
                'content': 'https://pris.ly/youtube',
                },
            ],
        },
    },
]

def main():
    print('Start seeding ...')
    for u in userData:
        hashed_password = bcrypt.hashpw(u['password'].encode('utf-8'), bcrypt.gensalt())
        u['password'] = hashed_password.decode('utf-8')
        user = client.user.create(data=u)
        print(f'Created user with id: {user.id}')
    print('Seeding finished.')

if __name__ == '__main__':
    main()
    client.disconnect()
