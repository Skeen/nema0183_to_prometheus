import asyncio
import signal
import sys
from collections import defaultdict
from datetime import date, datetime, time

import pynmea2
from prometheus_client import Gauge, make_asgi_app
from pynmea2.types.talker import TalkerSentence
from uvicorn import Config, Server


def generate_metrics(subclass):
    class_name = subclass.__name__

    def generate_metric(field):
        help_text = field[0]
        short_name = field[1]
        metric_name = class_name + "_" + field[1]
        metric_name = metric_name.replace(" ", "_")
        return short_name, Gauge(metric_name, help_text)

    return class_name, dict(map(generate_metric, subclass.fields))


message_types = TalkerSentence.__subclasses__()
metrics = dict(map(generate_metrics, message_types))


class CustomServer(Server):
    def install_signal_handlers(self):
        pass


def install_signal_handlers(loop):
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, sys.exit, sig)


last_timestamp = None


async def handle_timestamp(timestamp):
    global last_timestamp

    if last_timestamp is None:
        last_timestamp = timestamp
        return

    difference = datetime.combine(date.today(), timestamp) - datetime.combine(
        date.today(), last_timestamp
    )
    sleep_seconds = difference.total_seconds()
    if sleep_seconds > 0:
        await asyncio.sleep(sleep_seconds)
    last_timestamp = timestamp


async def handle_message(msg):
    print(repr(msg))

    for field in msg.fields:
        short_name = field[1]
        raw_value = getattr(msg, short_name)
        if raw_value is None:
            continue
        try:
            value = float(raw_value)
        except:
            # print(raw_value, type(raw_value))
            continue
        metrics[msg.sentence_type][short_name].set(value)

    if hasattr(msg, "timestamp"):
        await handle_timestamp(msg.timestamp)


async def main():
    with open("nmea0183.dat", encoding="utf-8") as nema_file:
        for line in nema_file.readlines():
            try:
                msg = pynmea2.parse(line, check=True)
                await handle_message(msg)
            except pynmea2.ParseError as e:
                print("Parse error: {}".format(e))
                continue


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    app = make_asgi_app()
    config = Config(app=app, loop=loop, host="0.0.0.0")
    server = CustomServer(config)
    install_signal_handlers(loop=loop)

    loop.run_until_complete(asyncio.wait([server.serve(), main()]))
