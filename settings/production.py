from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'aoranprojectdb.csbmq0o4oy2b.us-west-1.rds.amazonaws.com',
        'NAME': 'aoranprojectdb',
        'USER': 'ranaoyang',
        'PASSWORD': '1991627yar'
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qgd(kc82*#anz6cyz*jg30wx+cdtav51dtoe5*a(30pqkg@%g*'


ins_tags = {'a.wen.z': ['instafood', 'food', 'foodnetwork', 'delicious', 'foodie', 'yummy', 'cooking',
                        'foodphotography', 'Chefmode', 'foodbloger', 'homechef', 'homecooking', 'foodlover',
                        'seattle', 'eater', 'foodgasm', 'foodporn', 'thekitch', 'hungry', 'dinner', 'lunch',
                        'asianfood', 'chinesefood', 'japanesefood', 'thaifood', 'koreanfood', 'souplover',
                        'spicy', 'lovelife', 'recipe', '料理', '美味しい', 'お腹いっぱい', '요리', '맛있다', '맵다',
                        '중국요리', '냠냠', '매운맛', '中餐', '점심', '晚餐', 'อาหาร', 'อร่อย', 'interiordesign',
                        'homedecor', 'homedesign', 'decoration', 'restaurantdesign', 'indiedesign', 'designer',
                        'yolo', 'restaurantdecor', 'coffeeshop', 'bookstore', '咖啡馆', '咖啡厅', '书店', '餐厅',
                        '室内设计', '设计师'],
            }

ins_comments = {'a.wen.z': ['Love the shot!', 'Nice shot!', 'Great shot!']}


ins_passwords = {'a.wen.z': 'wenzhangwen',
                 'ranaoyang@outlook.com': '1991627yar',
                 }