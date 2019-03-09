import wikipedia


class WikiParser:
    def __init__(self, max_depth=2, lang='en'):
        self.used_titles = set()
        self.lang = lang
        self.max_depth = max_depth

    def check_title(self, title):
        wikipedia.set_lang(self.lang)
        try:
            wikipedia.page(title)
        except wikipedia.DisambiguationError as ex:
            raise WikiError(title, ex.options)
        except wikipedia.PageError:
            raise WikiError(title, [])

    def links_iter(self, title):
        return self._links_iter(title, suggest_title=True)

    def _links_iter(self, title, depth=1, suggest_title=False):
        if title in self.used_titles:
            return

        wikipedia.set_lang(self.lang)
        try:
            if suggest_title:
                page = wikipedia.page(title)
            else:
                page = wikipedia.WikipediaPage(title)
        except (wikipedia.DisambiguationError, wikipedia.PageError):
            return

        self.used_titles.add(title)

        text = page.content.split('\n')
        for line in text:
            if line[:2] == '==':
                text.remove(line)
        text = '\n'.join(text)

        yield text

        if depth < self.max_depth:
            links = page.links
            for link in links:
                yield from self._links_iter(link, depth + 1)


class WikiError(wikipedia.DisambiguationError):
    pass


if __name__ == '__main__':
    for text in WikiParser(lang='en').links_iter('Forsen'):
        print(text)
