#!/usr/bin/python

import re
import hashlib
import glob
from PIL import Image
import oss2
from config import ACCESS, KEY, BNAME, ENDPOINT
import subprocess


def main():
    auth = oss2.Auth(ACCESS, KEY)
    bucket = oss2.Bucket(auth, ENDPOINT, BNAME)

    vlist = list(glob.glob(r'./video/*.mp4'))
    plist = list(glob.glob(r'./pic/*.JPG'))
    vlist.reverse()
    plist.reverse()

    print vlist, plist

    if len(plist) > 0:
        pic(plist, bucket)

    if len(vlist) > 0:
        video(vlist, bucket)
        pass

    replace(bucket)
    js(bucket)
    index(bucket)


def replace(bucket):
    plist = list(glob.glob(r'./js/p*.js'))
    pattern = re.compile(r'\d+-[a-z0-9A-Z]{64}')
    for m in plist:
        print m
        content = open(m).read()
        flist = re.findall(pattern, content)
        for f in flist:
            num = f.split('-')[0]
            num = int(num)
            if num > 200 * 1000:
                bucket.get_object_to_file(f, r'./pic/tmp.jpg')
                cnew = resize(r'./pic/tmp.jpg', bucket, 1000)
                print f, cnew
                content = content.replace(f, cnew)
                open(m, 'w').write(content)
                bucket.delete_object(f)


def resize(name, bucket, r=100.0):
    im = Image.open(name)
    lam = int(round(max(im.width / r, im.height / r)))
    if lam == 0:
        lam = 1
    im = im.resize((im.width / lam, im.height / lam), Image.BILINEAR)
    im.save('./pic1/' + name)
    with open('./pic1/' + name, 'rb') as f:
        content = f.read()
    return up(content, bucket)


def s(a):
    s256 = str(len(a)) + '-' + hashlib.sha256(a).hexdigest()
    return str(s256)


def up(name, bucket, headers=None):
    if headers is None:
        headers = {'Content-Type': 'image/jpeg', 'Cache-Control': 'public'}
    sha = s(name)
    try:
        bucket.object_exists(sha)
    except:
        bucket.put_object(sha, name, headers=headers)
    return sha


def pic(a, bucket, r=100.0):
    for m in a:
        content = resize(m, bucket, 1000)
        m = resize(m, bucket, r)
        print '{ori:"' + content + '",thu:"' + m + '"},'


def video(b, bucket):
    for m in b:
        with open(m, 'rb') as f:
            content = f.read()
        headers = {'Content-Type': 'video/mp4', 'Cache-Control': 'public'}
        content = up(content, bucket, headers)
        print "{ href: '" + content + "', time: '" + m + "' },"


def index(bucket):
    out = subprocess.check_output('export NODE_PATH=/usr/local/lib/node_modules;gulp html', shell=True,
                                  stderr=subprocess.STDOUT)
    print out
    bucket.put_object('index.html', open('html/index.html').read(),
                      headers={'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'})
    bucket.batch_delete_objects(['test.html'])  # ,'video.html'


def test(bucket):
    bucket.put_object('test.html', open('index.html').read(),
                      headers={'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'})


def js(bucket):
    plist = list(glob.glob(r'./js/p*.js'))
    for m in plist:
        key = m.split('/')[-1]
        print key, m
        bucket.put_object(key, open(m).read())


if __name__ == '__main__':
    main()
