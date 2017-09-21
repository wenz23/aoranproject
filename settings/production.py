# -*- coding: utf-8 -*-

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


ins_tags = {'a.wen.z': ['instafood', 'food', 'foodnetwork', 'delicious', 'foodie', 'yummy', 'cooking',  'breakfast',
                        'foodphotography', 'Chefmode', 'foodbloger', 'homechef', 'homecooking', 'foodlover',
                        'seattle', 'eater', 'foodgasm', 'foodporn', 'thekitch', 'hungry', 'dinner', 'lunch',
                        'asianfood', 'chinesefood', 'japanesefood', 'thaifood', 'koreanfood', 'souplover',
                        'spicy', 'lovelife', 'recipe', '料理', '美味しい', 'お腹いっぱい', '요리', '맛있다', '맵다',
                        '중국요리', '냠냠', '매운맛', '中餐', '점심', '晚餐', 'อาหาร', 'อร่อย', 'interiordesign',
                        'homedecor', 'homedesign', 'decoration', 'restaurantdesign', 'indiedesign', 'designer',
                        'yolo', 'restaurantdecor', 'coffeeshop', 'bookstore', '咖啡馆', '咖啡厅', '书店', '餐厅',
                        '室内设计', '设计师'],
            }

ins_comments = {'a.wen.z': ['❤️', 'Love the shot!', 'Nice shot!', 'Great shot!', 'Love it', 'Nice photo', 'Nice photo!',
                            'Wonderful!', 'Great!', 'Nice!', 'Good shot!', 'Nice pic!', 'Like this!', 'Like this',
                            'Good one!', 'Prefect!', 'Nice', 'Good shot', 'Nice pic', 'Like this one!', 'Like this one',
                            'Love this one', 'Love this one!', 'Great', 'Love it!', 'Amazing!', 'Amazing', 'Beautiful!',
                            'Love this one!', 'Nice shot', 'Prefect', 'Wonderful', 'Beautiful', 'Splendida!',
                            ]}


ins_passwords = {'a.wen.z': 'wenzhangwen',
                 'ranaoyang': 'Yar1991627--',
                 'ranaoyang@outlook.com': '1991627yar'
                 }

api_gateway = {
    "CrawlerAPIKey-P": ["25yv6Zxmyo4n7ogCLOn6E3WX71FBy16Q97IvrO5y",
                        "https://8v0n6wy852.execute-api.us-west-1.amazonaws.com/prod/crawlerFunction"],
    "CrawlerAPIKey-C": ["zWZq46glFJaEqbPUcNskf4Og84y3DeVk72YIPA6G",
                        "https://ltmjmfb4lc.execute-api.us-west-1.amazonaws.com/prod/aoranlambdafunction"],
}


ins_xpath = {'login_in_username': "//*[@id='react-root']/section/main/article/header/div[2]/div[1]/h1",
             'search_box': "//span[contains(@class,'coreSpriteSearchIcon')]",
             'search_box_input': "//input[contains(@placeholder, 'Search')]",
             }
