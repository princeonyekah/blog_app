import asyncio
import bcrypt
from prisma import Prisma

client = Prisma()
client.connect()

userData = [
    {
        'data': {
            'email': 'destiny@gmail.com',
            'password': 'destiny',
            'name': 'Destiny Williams',
            'bio': 'Hello World',
            'profilePic': 'profile1.jpg',  # Profile picture filename
            'posts': {
                'create': [
                    {
                        'title': '10 Essential Tips for Productivity',
                        'content': 'Boost your productivity with these tried-and-tested tips! From time management techniques to effective goal setting, this post covers everything you need to know to supercharge your productivity and achieve your goals.',
                        'published': True,
                        'imageFilename': 'default_photo1.jpg'  # Image filename for the post
                    }
                ]
            }
        }
    }
]


def main():
    print('Start seeding ...')
    for u in userData:
        hashed_password = bcrypt.hashpw(u['data']['password'].encode('utf-8'), bcrypt.gensalt())
        u['data']['password'] = hashed_password.decode('utf-8')
        user = client.user.create(data= u)
        print(f'Created user with id: {user.id}')
    print('Seeding finished.')

if __name__ == '__main__':
    main()
    client.disconnect()

