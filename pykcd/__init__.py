from bs4 import BeautifulSoup
import os, wget, requests, shutil



class XKCDStrip():
    '''
    Strip object for given XKCD strip
    '''


    def __init__(self, strip_num):
        '''
        Constructs the strip object

        :param strip_num: The number of the strip
        '''

        # The location of the API for the strip
        # Interpolates the strip number into the domain
        self.json_domain = 'http://www.xkcd.com/{}/info.0.json'.format(strip_num)
        self.user_agent = 'pykcd/1.0.0 (+https://github.com/JacobLandau/pykcd/)'

        # Creates the identifiers for each property,
        # so the value can be assigned later, when needed
        self.strip_num = strip_num
        self.transcript = None
        self.news = None
        self.title = None
        self.day = None
        self.month = None
        self.year = None
        self.link = None
        self.alt_text = None
        self.image_link = None

        # If the strip is No. 404, there is no API.
        # Thus, we continue the April Fools joke by
        # returning 'value not found' for each property
        if self.strip_num == 404:
            self.transcript = '404 - Transcript Not Found'
            self.news = '404 - News Not Found'
            self.title = '404 - Title Not Found'
            self.day = '404 - Day Not Found'
            self.month = '404 - Month Not Found'
            self.year = '404 - Year Not Found'
            self.link = '404 - Hyperlink Not Found'
            self.alt_text = '404 - Alt Text Not Found'
            self.image_link = '404 - Image Link Not Found'
        else:
            # This grabs the JSON document and parses it into a dictionary
            # It is saved for here because since the JSON for No. 404
            # doesn't exist, it would fittingly return a 404 error.
            self.url = requests.get(self.json_domain, headers={'user-agent':self.user_agent, 'content-type':'application/json'})
            self.url.raise_for_status()
            self.strip = self.url.json()

            # Grabs the value for each from their dictionary entry
            self.transcript = self.strip['transcript']
            self.news = self.strip['news']
            self.title = self.strip['title']
            self.day = self.strip['day']
            self.month = self.strip['month']
            self.year = self.strip['year']
            self.link = self.strip['link']
            self.alt_text = self.strip['alt']

            # If the strip has a hyperlink, it may lead to a larger version
            if self.link != '':
                # If the strip links to a large version
                # We get the image link for the large version instead
                # Using a temporary web scraper
                if 'large' in self.link:
                    temp_soup = BeautifulSoup(requests.get(self.link, headers={'user-agent':self.user_agent, 'content-type':'text/html'}).content, 'lxml')
                    link = temp_soup.img
                    self.image_link = link.get('src')
                else:
                    self.image_link = self.strip['img']
            else:
                self.image_link = self.strip['img']

    @property
    def strip_num(self):
        '''
        The strip's number
        '''
        return self._strip_num

    @strip_num.setter
    def strip_num(self, strip_num):
        self._strip_num = strip_num

    @property
    def transcript(self):
        '''
        The strip's transcript
        '''
        return self._transcript

    @transcript.setter
    def transcript(self, transcript):
        self._transcript = transcript

    @property
    def news(self):
        '''
        The strip's news posting
        '''
        return self._news

    @news.setter
    def news(self, news):
        self._news = news

    @property
    def title(self):
        '''
        The strip's title
        '''
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def day(self):
        '''
        Day strip was published
        '''
        return self._day

    @day.setter
    def day(self, day):
        self._day = day

    @property
    def month(self):
        '''
        Month strip was published
        '''
        return self._month

    @month.setter
    def month(self, month):
        self._month = month

    @property
    def year(self):
        '''
        Year strip was published
        '''
        return self._year

    @year.setter
    def year(self, year):
        self._year = year

    @property
    def link(self):
        '''
        Domain strip is hyperlinked towards
        '''
        return self._link

    @link.setter
    def link(self, link):
        self._link = link

    @property
    def alt_text(self):
        '''
        The strip's alt text
        '''
        return self._alt_text

    @alt_text.setter
    def alt_text(self, alt_text):
        self._alt_text = alt_text

    @property
    def image_link(self):
        '''
        The strip's image link
        '''
        return self._image_link

    @image_link.setter
    def image_link(self, image_link):
        self._image_link = image_link

    def download_strip(self):
        '''
        Downloads the strip into the working directory
        '''

        # Creates the archive folder if it doesn't already exist
        if os.path.exists('XKCD Archive'):
            pass
        else:
            os.mkdir('XKCD Archive')

        archive_directory = './XKCD Archive/'

        if self.strip_num == 404:
            file = open('{}404 - Item Not Found'.format(archive_directory), mode='w')
            file.close()
        else:
            try:
                # Gets the name of the strip, filtering out any characters
                # which are invalid for Windows filenaming conventions
                strip_title = ''.join(filter(lambda x: x not in '\/:*?"<>|', self.title))

                image_link = self.image_link

                # The file name will be the strip title plus the file extension as grabbed by the image link
                file_name = strip_title + image_link[-4:]

                # Checks if the strip is already downloaded
                # if the strip is, notifies user and iterates loop
                # if the strip is not, downloads and renames
                if os.path.exists(archive_directory + file_name) or os.path.exists(archive_directory + str(self.strip_num) + ' - ' + file_name):
                    print('-' * (shutil.get_terminal_size()[0] - 1))
                    print('{} ALREADY DOWNLOADED'.format(self.strip_num))
                else:
                    wget.download(image_link, archive_directory)
                    os.rename('{}{}'.format(archive_directory, image_link[28:]), '{}{} - {}'.format(archive_directory, self.strip_num, file_name))

                # Runs if the system throws a UnicodeEncodeError, which will only happen
                # when it tries to print a unicode character to the console
                # In that case, we substitute the usual line printed to the console
                # for a cheeky, console-safe stand-in
            except UnicodeEncodeError:
                print('\n{} - This title cannot be printed because unicode hates you.'.format(self.strip_num))
