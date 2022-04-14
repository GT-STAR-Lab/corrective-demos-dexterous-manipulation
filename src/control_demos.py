from enum import IntEnum
import click
import requests

DESC = '''
Helper script to control collection of demonstrations via LeapMotion sensor.\n
USAGE:\n
    Control the collection of demonstrations via LeapMotion sensor.\n
    $ python control_demos.py --max_demos 10\n
'''
class Signal(IntEnum):
    START = 1
    STOP = 0

def read_and_send_signal(signal, message, url, send_no_signal=False):
    feedback = input(message + ' [Y/n] ')

    if feedback == '': # default case
        feedback = 'yes'

    if feedback[0].lower() == 'y':
        data = {
            'data': int(signal)
        }
        requests.get(url=url, params=data)
        return True

    if send_no_signal:
        data = {
            'data': 1 - signal
        }
        requests.get(url=url, params=data)
    return False

@click.command(help=DESC)
@click.option('--max_demos', type=int, help='max demos to record', required=False, default=35)
def main(max_demos):
    base_url = 'http://localhost:5000'
    record_url = base_url + '/record'
    save_url = base_url + '/save'

    collect_demos = False

    total_saved = 0

    print(max_demos, type(max_demos))

    while total_saved < max_demos:
        print('Total demonstrations saved: ', total_saved)

        if not collect_demos:
            collect_demos = read_and_send_signal(
                Signal.START,
                'Start collecting demo?',
                record_url
            )

        if collect_demos:
            collect_demos = not read_and_send_signal(
                Signal.STOP,
                'Stop collecting demo?',
                record_url
            )

            if not collect_demos:
                total_saved += read_and_send_signal(
                    Signal.START,
                    'Save the demo?',
                    save_url,
                    send_no_signal=True
                )

if __name__ == '__main__':
    main()
            