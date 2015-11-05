# pykcd [![PyPI version](https://badge.fury.io/py/pykcd.svg)](https://badge.fury.io/py/pykcd)
Python interface for the XKCD API

## Usage

The strip object can be initialized like so:

    Strip = pykcd.XKCDStrip(strip_number)

The full berth of accessors can be found using the help function. Here's a sampling.

* Alt text

        In [1]: XKCDStrip(50).get_alt_text()
        Out[1]: 'Of course, Penny Arcade has already mocked themselves for this. They don't care."

* Image link

        In [2]: XKCDStrip(732).get_image_link()
        Out[2]: 'http://imgs.xkcd.com/comics/hdtv.png'

* Downloading Strips

        In [3]: XKCDStrip(178).download_strip()
        100% [...................................] 18611 / 18611
        // Downloaded to /XKCD_Archive/ in the working directory

## Under the Hood

Each XKCD strip, barring Strip #404 ([Funny funny](http://www.explainxkcd.com/wiki/index.php/404)), has a JSON document located at "www.xkcd.com/#/info.0.json". This contains references to data such as the day, month and year published, the strip transcript, the image hotlink, the alt text, and other details. By using the requests library, this document can be grabbed and parsed into a standard Python dictionary, through which the data can be referenced and accessed by it's respective keys.

Image links present a unique challenge in the case of large strips such as [Strip #802: Online Communities 2](http://www.explainxkcd.com/wiki/index.php/802:_Online_Communities_2), which have their img key point to a thumbnail rather than the full-resolution hotlink. The solution lies within the link key, which points to a page containing only the full resolution image. We can scrape out the link from this page using BeautifulSoup, and return this value when the user asks for the image link from one of these large strips.

Wget is used in order to download the strips to the '/XKCD_Archive/' folder in the working directory, which will be created if the directory does not already exist. It will check to see if the file is already present, and names the file according to a "Number - Title" scheme. Any characters in the title not friendly with Windows filesystems will be filtered out using a lambda function.

## Why?

Why not.
