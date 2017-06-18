#!/usr/local/bin/python3

import requests
import json
import re
import html
import base64
import os

START = ''
DESTINATION = ''
API_KEY = ''
TAG_RE = re.compile(r'<[^>]+>')


def main():
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}'.format(
        START, DESTINATION, API_KEY)
    data = json.loads(requests.get(url).content)
    routes = data.get('routes')
    parse_route(routes[0])


def load_config():
    global START
    global DESTINATION
    global API_KEY

    directory = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(directory, 'config.json')) as f:
        json_config = json.loads(f.read())

    START = json_config.get('start')
    DESTINATION = json_config.get('destination')
    API_KEY = json_config.get('api_key')


def parse_route(route):
    leg = route.get('legs')[0]
    print(leg.get('duration').get('text'))
    print('---')
    print(get_steps(leg))
    print('{} | image={}'.format(route.get('summary'), get_map(route)))


def get_steps(leg):
    return '\n'.join([step_to_string(step) for step in leg.get('steps')])


def step_to_string(step):
    return '{} - {}'.format(clean(step.get('html_instructions')),
                            step.get('duration').get('text'))


def get_map(route):
    points = route.get('overview_polyline').get('points')
    url = 'https://maps.googleapis.com/maps/api/staticmap?size=640x400&path=enc%3A{}&key={}'.format(
        points, API_KEY)
    image = requests.get(url).content
    return base64.b64encode(image).decode('utf-8')


def clean(text):
    text = html.unescape(text)
    return TAG_RE.sub('', text)

if __name__ == '__main__':
    load_config()
    main()
