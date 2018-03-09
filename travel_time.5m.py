#!/usr/bin/env LC_ALL=en_US.UTF-8 /usr/local/bin/python3

import requests
import dateparser
from datetime import datetime
import json
import re
import html
import base64
import os

START = ""
DESTINATION = ""
API_KEY = ""
TAG_RE = re.compile(r"<[^>]+>")


def main():
    url = ("https://maps.googleapis.com/maps/api/directions/json?"
           "origin={}&destination={}&mode=driving&departure_time=now&"
           "key={}".format(START, DESTINATION, API_KEY))
    data = json.loads(requests.get(url).content)
    routes = data.get("routes")
    parse_route(routes[0])


def load_config():
    global START
    global DESTINATION
    global API_KEY

    directory = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(directory, "config.json")) as f:
        json_config = json.loads(f.read())

    START = json_config.get("start")
    DESTINATION = json_config.get("destination")
    API_KEY = json_config.get("api_key")


def parse_route(route):
    leg = route.get("legs")[0]
    duration = leg.get("duration").get("text")
    duration_in_traffic = leg.get("duration_in_traffic").get("text")
    print("{}|color={}".format(
        duration_in_traffic, get_colour(duration, duration_in_traffic)))
    print("---")
    print(get_steps(leg).encode().decode())
    print("{} | image={}".format(route.get("summary"), get_map(route)))


def get_colour(duration, duration_in_traffic):
    """Return a colour to provide an idea of the current traffic.

    Gives a visual representation of the amount of traffic on route.

    :param duration: A duration string, like "4 mins"
    :param duration_in_traffic: A duration in traffic
    """
    now = datetime.now()
    # dateparser will put the duration in traffic before the duration without
    # traffic. In this funtion, we basically use it to work out the potential
    # set off time for each scenario with the same arrival time
    set_off_time = dateparser.parse(duration,  settings={"RELATIVE_BASE": now})
    set_off_time_in_traffic = dateparser.parse(
        duration_in_traffic,  settings={"RELATIVE_BASE": now})

    if set_off_time_in_traffic > set_off_time:
        # If real duration is less than the normal duration, return green
        return "green"

    difference = set_off_time - set_off_time_in_traffic
    minutes = difference.seconds / 60

    if minutes < 10:
        return "green"
    elif minutes >= 10 and minutes <= 25:
        return "orange"
    else:
        return "red"


def get_steps(leg):
    return "\n".join([step_to_string(step) for step in leg.get("steps")])


def step_to_string(step):
    return "{} - {}".format(clean(step.get("html_instructions")),
                            step.get("duration").get("text"))


def get_map(route):
    points = route.get("overview_polyline").get("points")
    url = ("https://maps.googleapis.com/maps/api/staticmap?"
           "size=640x400&path=enc%3A{}&key={}".format(points, API_KEY))
    image = requests.get(url).content
    return base64.b64encode(image).decode("utf-8")


def clean(text):
    text = html.unescape(text)
    return TAG_RE.sub("", text)


if __name__ == "__main__":
    load_config()
    main()
