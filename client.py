import requests
import argparse
import json


def post_message(message, queue_alias='0'):
    payload = {'message': message, 'queue_alias': queue_alias}
    r = requests.post('http://localhost:8000', json=payload)
    return r.status_code


def get_message(queue_alias='0'):
    r = requests.get(f'http://localhost:8000/{queue_alias}')
    if r.status_code == 200:
        print(json.loads(r.text)['message'])
    return r.status_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Message Exchanger Client')
    parser.add_argument('--post', type=str, help='Message to post')
    parser.add_argument('--get', action='store_true', help='Retrieve a message')
    parser.add_argument('--queue', type=str, default='0', help='Queue alias')
    args = parser.parse_args()

    if args.post:
        post_message(args.post, args.queue)
    elif args.get:
        get_message(args.queue)
