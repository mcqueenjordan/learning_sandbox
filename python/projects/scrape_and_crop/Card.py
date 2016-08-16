import urllib.request
import os, re, shutil, time


class Card:
    """ A magic card. """

    def __init__(self, **kwargs):
        #static setup, for now. this should be pushed to config file.
        self.adjacent_hyphens_re = re.compile(r"([-]){2,}")
        self.errors = []
        self.abbreviations = {
            'Eternal Masters': 'ema/cards',
            }
        self.slug_re = re.compile('[^a-zA-Z\-]')

        #main instantiation; dynamic stuff -- for the most part.
        self.title = kwargs['title']
        self.edition = kwargs['edition'] if 'edition' in kwargs else 'Eternal Masters'
        self.variation = kwargs['variation'] if 'variation' in kwargs else ''
        self.title_slug = self.get_slug('title')
        self.edition_slug = self.get_slug('edition')
        self.save_location = "{}/{}.jpg".format(self.edition_slug, self.title_slug)
        self.directory = '/'.join(self.save_location.split('/')[0:-1])
        self.filename = self.save_location.split('/')[-1]
        self.static = kwargs['static'] if 'static' in kwargs else ''
        self.url = kwargs['url'] if 'url' in kwargs else self.get_url()


    def get_slug(self, attribute):
        slug = getattr(self, attribute).strip()
        slug = slug.replace(" ", "-").lower()
        slug = self.slug_re.sub('', slug)
        slug = self.adjacent_hyphens_re.sub("-", slug)
        return slug


    def get_foreign_edition_slug(self):
        return self.abbreviations[self.edition]


    def get_url(self):
        if self.static:
            return "{}/{}/{}.jpg".format(self.static,
                                         self.foreign_edition_slug,
                                         self.foreign_name_slug)
        if not self.static:
            pass


    def get_foreign_name_slug(self):
        """ At present, this procedure is explicitly for mythicspoilers.com """
        foreign_slug = self.title_slug.replace('-', '')
        return foreign_slug


    def download(self):
        """ Handles the request, download, and saving. """
        #download prework -- check if exists, mkdir
        if os.path.isfile(self.save_location):
            print("++ (already saved) ", self.save_location)
            return
        os.makedirs(self.directory, exist_ok=True)

        #download core function -- make request, save
        try:
            req = urllib.request.Request(self.url)
            req.add_header('User-agent',
                           'Python 3.4.3; Jordan M.; jmcqueen@cardkingdom.com')
            with urllib.request.urlopen(req) as response, open(self.save_location, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                print("++ ", self.save_location)
                response.close()
                time.sleep(5)
        except Exception as error:
            print("-- ", error)
            self.errors.append((self.edition, self.title, self.url, error))
            time.sleep(5)
        finally:
            try:
                response.close()
            except NameError:
                pass

