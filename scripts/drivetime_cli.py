import argparse
from datetime import datetime
import time

import sys
sys.path.insert(0, '..')

from drivetime.drivetime import drivetime


if __name__ == "__main__":

    # define parser
    parser = argparse.ArgumentParser()
    parser.add_argument('start', help='starting location (str)')
    parser.add_argument('end', help='ending location (str)')
    parser.add_argument('--filepath', help='filepath to write to (str)')
    parser.add_argument('--interval', help='interval (mins) to write (int)',
                        type=int)

    # parse args
    args = parser.parse_args()
    start = args.start
    end = args.end
    filepath = args.filepath
    interval = args.interval

    # assertions
    if filepath:
        assert interval is not None, 'must specify interval'
        assert interval > 0, 'invalid interval'

    # setup
    dt = drivetime()

    # write headers
    with open(filepath, 'w+') as file:
        file.write('timestamp, time_1, time_2, time_3, time_4, time_5\n')

    # if filename is present, loop infinitely writing to file
    if filepath:

        while True:

            # data holder
            data = []

            # capture time
            timestamp = datetime.now()
            data.append(timestamp)

            # write line with comma separated times
            with open(filepath, 'a') as file:

                # get time
                times = dt.get_time(start, end)

                # add times, assemble line
                data.extend(times)
                line = ','.join(str(x) for x in data) + '\n'

                # write
                file.write(line)

            # print to terminal
            print('%s -- %s minutes' % (timestamp, times))

            # wait for interval to be exceeded
            time.sleep(60 * interval)

    # if no filename, print time once
    else:
        times = dt.get_time(start, end)
        print('Drive time(s) currently %s minutes' % times)
