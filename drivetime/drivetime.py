from selenium import webdriver
import re
from datetime import timedelta


class drivetime():

    def __init__(self, backend='web', autostart=True, mode='headless',
                 chromedriver_path=None):

        # backend validation
        assert backend in ['web', 'api'], 'Invalid backend argument'
        self.backend = backend

        # backend setup
        if self.backend == 'web':
            if autostart: self._web_start(mode=mode,
                                          chromedriver_path=chromedriver_path)
        else:
            raise Exception('Backend {0} not implemented yet'.format(backend))

    def _web_start(self, mode='headless', chromedriver_path=None):
        """Starts selenium driver"""

        # default path if not present
        if chromedriver_path is None: chromedriver_path = './chromedriver'

        # set options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True

        # start driver
        self.driver = webdriver.Chrome(chromedriver_path, options=chrome_options)

    def _web_stop(self):
        """Stops selenium driver"""

        self.driver.quit()

    def _web_parse_gmaps(self, t_string):
        """Parses time string from gmaps into timedelta"""

        # abbreviations used in gmaps
        abbreviations = {'d': 'days',
                         'h': 'hours',
                         'min': 'minutes'}

        # break string into parts
        t_parts = re.findall('[0-9]+ [a-z]+', t_string)
        t_dict = {}
        if not t_parts: return None

        # map each part to dictionary for timedelta
        for t_part in t_parts:
            # for each possible time part
            for map_in, map_out in abbreviations.items():
                # grab value
                values = re.findall('[0-9]+(?= {0})'.format(map_in), t_string)
                if values:
                    if not len(values) == 1: raise Exception('Failed to parse time string')
                    t_dict[map_out] = int(values[0])

        # convert to timedelta
        tdelta = timedelta(**t_dict)

        # convert to minutes and return
        time = int((tdelta.days * 24 * 60) + (tdelta.seconds / 60))
        return time

    def get_time(self, start, end):
        """Fetches list of drive times in minutes"""

        # build string for search
        search_string = '{start}/{stop}'.format(start=start.replace(' ', '+'),
                                                stop=end.replace(' ', '+'))

        # fetch page
        url = 'https://www.google.com/maps/dir/{0}'.format(search_string)
        self.driver.get(url)

        # grab each drive time
        try:
            elements = self.driver.find_elements_by_class_name('section-directions-trip-duration')
        except Exception as e:
            raise Exception('Unable to parse page; address is {0}'.format(url))
        times = []
        for element in elements:
            time = self._web_parse_gmaps(element.text)
            if time: times.append(time)
        if not times: raise Exception('No results; address is {0}'.format(url))

        # return list
        return times

    def cleanup(self):
        """Closes connections"""

        if self.backend == 'web':
            self._web_stop()
