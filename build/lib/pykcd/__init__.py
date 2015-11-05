from bs4 import BeautifulSoup
import os, wget, urllib, urllib.request, requests, shutil



class XKCDStrip():
    '''
    Strip object for given XKCD strip

    Functions:
    .. __init__(self, strip_num) : Constructs the object
    .. get_alt_text(self) : The Alt Text for the Strip
    .. get_strip(self) : Downloads the Strip
    '''


    def __init__(self, strip_num):
        '''
        Constructs the strip object

        strip_num : The number of the strip
        directory : The folder in which XKCD stores their strips
        '''

        self.strip_num = strip_num
        self.directory = '//imgs.xkcd.com/comics/'

    def get_alt_text(self):
        '''
        Retrieves the alt text of the strip
        '''

        if self.strip_num == 404:
            return '404 - Title Text Not Found'
        else:
            url = requests.get('http://www.xkcd.com/{}/info.0.json'.format(self.strip_num))
            url.raise_for_status()
            strip = url.json()
            return strip['alt']

    def get_strip(self):
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
                # Sets url for the selected strip
                url = requests.get('http://www.xkcd.com/{}/info.0.json'.format(self.strip_num))
                url.raise_for_status()
                # Makes a dictionary of the strip's json
                strip = url.json()

                # Gets the name of the strip, filtering out any characters
                # which are invalid for Windows filenaming conventions
                strip_title = ''.join(filter(lambda x: x not in '\/:*?"<>|', strip['title']))

                if strip['link'] != '':
                    # If the strip links to a large version
                    # We get the image link for the large version instead
                    # Using a temporary web scraper
                    if 'large' in strip['link']:
                        temp_soup = BeautifulSoup(urllib.request.urlopen(strip['link']))
                        link = temp_soup.img
                        image_link = link.get('src')
                else:
                    image_link = strip['img']

                # The file name will be the strip title plus the file extension as grabbed by the image link
                file_name = strip_title + image_link[-4:]

                # Checks if the strip is already downloaded
                # if the strip is, notifies user and iterates loop
                # if the strip is not, downloads and renames
                if os.path.exists(file_name) or os.path.exists(archive_directory + str(self.strip_num) + ' - ' + file_name):
                    print('-' * (shutil.get_terminal_size()[0] - 1))
                    print('{} ALREADY DOWNLOADED'.format(self.strip_num))
                else:
                    wget.download(image_link)
                    os.rename(image_link[28:], '{}{} - {}'.format(archive_directory, self.strip_num, file_name))

                # Runs if the system throws a UnicodeEncodeError, which will only happen
                # when it tries to print a unicode character to the console
                # In that case, we substitute the usual line printed to the console
                # for a cheeky, console-safe stand-in
            except UnicodeEncodeError:
                print('\n{} - This title cannot be printed because unicode hates you.'.format(self.strip_num))
