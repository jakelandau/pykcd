from bs4 import BeautifulSoup
import os, wget, urllib, urllib.request, requests, shutil



class XKCDStrip():
    '''
    Strip object for given XKCD strip
    '''


    def __init__(self, strip_num):
        '''
        Constructs the strip object

        strip_num : The number of the strip
        json_domain : The location of the json for the strip
        url : The grabbed json document for the strip
        strip : The json parsed into dictionary format
        '''

        self.strip_num = strip_num
        self.json_domain = 'http://www.xkcd.com/{}/info.0.json'.format(strip_num)
        self.url = requests.get(self.json_domain)
        self.url.raise_for_status()
        self.strip = self.url.json()

    def get_strip_num(self):
        '''
        Retrieves the number of the strip
        '''

        return self.strip_num

    def get_transcript(self):
        '''
        Retrieves the transcript of the strip
        '''

        if self.get_strip_num() == 404:
            return '404 - Transcript Not Found'
        else:
            return self.strip['transcript']

    def get_news(self):
        '''
        Retrieves hardcoded news overwrite for the strip
        '''

        if self.get_strip_num() == 404:
            return '404 - News Not Found'
        else:
            return self.strip['news']

    def get_title(self):
        '''
        Retrieves the title of the strip
        '''

        if self.get_strip_num() == 404:
            return '404 - Title Not Found'
        else:
            return self.strip['title']

    def get_day(self):
        '''
        Retrieves the day of the year on which the strip was published
        '''
        if self.get_strip_num() == 404:
            return '1'
        else:
            return self.strip['day']

    def get_month(self):
        '''
        Retrieves the month of the year in which the strip was published
        '''
        if self.get_strip_num() == 404:
            return '4'
        else:
            return self.strip['month']

    def get_year(self):
        '''
        Retrieves the year in which the strip was published
        '''
        if self.get_strip_num() == 404:
            return '2008'
        else:
            return self.strip['year']

    def get_link(self):
        '''
        Retrieves the hyperlink of the strip
        '''

        if self.get_strip_num() == 404:
            return '404 - Hyperlink Not Found'
        else:
            return self.strip['link']

    def get_alt_text(self):
        '''
        Retrieves the alt text of the strip
        '''

        if self.get_strip_num() == 404:
            return '404 - Alt Text Not Found'
        else:
            return self.strip['alt']

    def get_image_link(self):
        '''
        Retrieves the link for the image of the strip
        '''

        if self.get_strip_num() == 404:
            return '404 - Image Link Not Found'
        else:
            if self.get_link() != '':
                    # If the strip links to a large version
                    # We get the image link for the large version instead
                    # Using a temporary web scraper
                    if 'large' in self.get_link():
                        temp_soup = BeautifulSoup(urllib.request.urlopen(self.get_link()))
                        link = temp_soup.img
                        return link.get('src')
            else:
                return self.strip['img']

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


        if self.get_strip_num() == 404:
            file = open('{}404 - Item Not Found'.format(archive_directory), mode='w')
            file.close()
        else:
            try:
                # Gets the name of the strip, filtering out any characters
                # which are invalid for Windows filenaming conventions
                strip_title = ''.join(filter(lambda x: x not in '\/:*?"<>|', self.get_title()))

                image_link = self.get_image_link()

                # The file name will be the strip title plus the file extension as grabbed by the image link
                file_name = strip_title + image_link[-4:]

                # Checks if the strip is already downloaded
                # if the strip is, notifies user and iterates loop
                # if the strip is not, downloads and renames
                if os.path.exists(file_name) or os.path.exists(archive_directory + str(self.get_strip_num()) + ' - ' + file_name):
                    print('-' * (shutil.get_terminal_size()[0] - 1))
                    print('{} ALREADY DOWNLOADED'.format(self.get_strip_num()))
                else:
                    wget.download(image_link)
                    os.rename(image_link[28:], '{}{} - {}'.format(archive_directory, self.get_strip_num(), file_name))

                # Runs if the system throws a UnicodeEncodeError, which will only happen
                # when it tries to print a unicode character to the console
                # In that case, we substitute the usual line printed to the console
                # for a cheeky, console-safe stand-in
            except UnicodeEncodeError:
                print('\n{} - This title cannot be printed because unicode hates you.'.format(self.get_strip_num()))
