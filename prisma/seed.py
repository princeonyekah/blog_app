import asyncio
import bcrypt
from prisma import Prisma

client = Prisma()
client.connect()

userData = [
    {

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

    },
     {

            'email': 'usen@gmail.com',
            'password': 'usen',
            'name': 'Emmanuel Usen',
            'bio': 'I am Dauntless',
            'profilePic': 'profile2.jpg',  # Profile picture filename
            'posts': {
                'create': [
                    {
                        'title': 'How To Get Away With Murder',
                'content': " Master the art of remote work with these effective strategies! As remote work becomes increasingly prevalent, it's essential to adapt and thrive in virtual work environments. From setting up a productive home office to maintaining work-life balance, this post offers valuable insights for remote workers.",
                        'published': True,
                        'imageFilename': 'default_photo1.jpg'  # Image filename for the post
                    }
                ]
            }

    },
    {
        'name': 'Princewill Onyekah',
        'email': 'princewill@gmail.com',
        'password': 'princewill',
        'profilePic': 'profile3.jpg',  # Profile picture filename
        'bio':'keep moving forward',
        'posts': {
            'create' : [
            {
                'title': 'The Future of Artificial Intelligence in Healthcare',
                'content': 'Dive into the exciting world of AI in healthcare. From diagnosing diseases to personalized treatment plans, AI is revolutionizing the way we approach healthcare. Explore the latest advancements and potential future developments in this rapidly evolving field.',
                'published': True,
                'imageFilename': 'default_photo3.jpg'  # Image filename for the post
            }

            ] } }
           ,
    {

        'name': 'Daniel Apolola',
        'email': 'daniel@gmail.com',
        'password': 'princewill',
        'profilePic': 'profile5.jpg',  # Profile picture filename
        'bio':'keep moving forward',
        'posts': {
            'create' : [
            {
                'title': 'Traveling on a Budget: Tips and Tricks',
                'content': "Travel doesn't have to break the bank! In this post, we share budget-friendly travel tips and tricks for exploring the world on a shoestring budget. From finding affordable accommodation to saving money on transportation, discover how to make the most of your travel adventures without overspending.'",
                'published': True,
                'imageFilename': 'default_photo5.jpg'  # Image filename for the post
            },
        ],
    }},
]




def main():
    print('Start seeding ...')
    for u in userData:
        hashed_password = bcrypt.hashpw(u['password'].encode('utf-8'), bcrypt.gensalt())
        u['password'] = hashed_password.decode('utf-8')
        user = client.user.create(data= u)
        print(f'Created user with id: {user.id}')
    print('Seeding finished.')

if __name__ == '__main__':
    main()
    client.disconnect()

