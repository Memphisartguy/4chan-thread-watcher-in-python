import sys, json, os, urllib
from urllib.parse import urlparse
from urllib.request import urlopen, urlretrieve

import argparse
import time

URL = 'https://a.4cdn.org/'
IMAGE_URL = 'http://i.4cdn.org/'
allowed_types = ['.jpg', '.png', '.gif']

parser = argparse.ArgumentParser()
parser.add_argument("url", help='The url of the thread.')
parser.add_argument("--watch", action='store_true', help='If this argument is passed, we will watch the thread for new images.')
args = parser.parse_args()


def download(board, url):
    response = urlopen(url)
    try:
        result = json.loads(response.read())
        for post in result['posts']:
            try:
                filename = str(post['tim']) + post['ext']
                if post['ext'] in allowed_types and not os.path.exists(filename):
                    urlretrieve(IMAGE_URL + board + '/' + filename, filename)
            except KeyError:
                continue
    except ValueError:
        sys.exit('No response. Is the thread deleted?')


def watch(board, url):
    while True:
        download(board, url)
        time.sleep(60)


def main():
    if 'boards.4chan.org' not in args.url:
        sys.exit("You didn't enter a valid 4chan URL")

    split = urlparse(args.url).path.replace('/', ' ').split()
    board, thread = split[0], split[2]
    url = '%s%s/thread/%s.json' % (URL, board, thread)

    try:
        os.mkdir(thread)
        print ('Created directory...')
    except OSError:
        print ('Directory already exists. Continuing. ')
        pass

    os.chdir(thread)

    if args.watch:
        print("Watching thread for new images")
        watch(board, url)
    else:
        print("Downloading")
        download(board, url)


if __name__ == '__main__':
    main()
