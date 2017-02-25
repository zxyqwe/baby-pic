#!/bin/python

import os
import time, hashlib
from PIL import Image
import oss2
from config import ACCESS, KEY, BNAME

auth = oss2.Auth(ACCESS, KEY)
endpoint = 'http://oss-cn-beijing.aliyuncs.com'
bucket = oss2.Bucket(auth, endpoint, BNAME)

for m in os.walk('video'):
    b = m[2]
for m in os.walk('pic'):
    a = m[2]


def resize(name, r=100.0):
    im = Image.open('pic/' + name)
    lam = int(round(min(im.width / r, im.height / r)))
    im = im.resize((im.width / lam, im.height / lam), Image.BILINEAR)
    im.save('pic1/' + name)
    with open('pic1/' + name, 'rb') as f:
        return f.read()


def s(a):
    s = str(len(a)) + '-' + hashlib.sha256(a).hexdigest()
    return str(s)


def up(name, headers={'Content-Type': 'image/jpeg', 'Cache-Control': 'public'}):
    sha = s(name)
    try:
        bucket.object_exists(sha)
    except:
        bucket.put_object(sha, name, headers=headers)
    return sha


def pic(r=100.0):
    a.reverse()
    for m in a:
        with open('pic/' + m, 'rb') as f:
            all = f.read()
        all = up(all)
        m = resize(m, r)
        m = up(m)
        print '{ori:"' + all + '",thu:"' + m + '"},'


def video():
    b.reverse()
    for m in b:
        with open('video/' + m, 'rb') as f:
            all = f.read()
        all = up(all, {'Content-Type': 'video/mp4', 'Cache-Control': 'public'})
        print "{ href: '" + all + "', time: '" + m + "' },"


def index():
    bucket.put_object('index.html', open('html/index.html').read(),
                      headers={'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'})
    bucket.batch_delete_objects(['test.html'])  # ,'video.html'


def test():
    bucket.put_object('test.html', open('index.html').read(),
                      headers={'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'})


def js():
    for m in []:  # 'v1611.js','v1612.js','v1610.js','p1610.js','p1611.js','p1612.js','v1607.js','v1608.js','v1609.js','p1607.js','p1608.js','p1609.js'
        bucket.put_object(m, open(m).read())
