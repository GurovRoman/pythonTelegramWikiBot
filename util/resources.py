class Replies():
    WRONG_ARGS = 'Incorrect arguments, please refer to `/help`.'
    WRONG_URL = 'Incorrect URL.\n' \
                'An example of correct url:\n' \
                'https://en.wikipedia.org/wiki/Billy_Herrington'
    DISAMBIGUATION = 'This page may refer to:\n`{}`'
    NOT_LEARNED = 'The bot needs a wiki page to learn from.' \
                  'Use `/teach`.'
    START = 'Yo, dawg.\n' \
            'Use `/help` to get all the required information'
    HELP = 'CAN DO:\n' \
           '`/teach <depth> <wikipedia_URL>`' \
           ' - scan the page and all the links recursively up to `depth`\n' \
           '`/write <count>` - generates `count` words\n' \
           '`/top <count> <asc|desc>` - outputs `count` most|least popular words\n' \
           '`/stop_words` - words that stand out too much\n' \
           '`/word_cloud <COLOR>` - Draws word cloud in specified color palette\n' \
           '`/describe [word]` - GIVES YOU INFORMATION ABOUT A WORD OR WHOLE MODEL\n'
    WORD_STATS = 'Stats for word `{}`:\n' \
                 'Times occurred: `{}`\n' \
                 'Rank by times occurred: `{}`\n' \
                 'Most popular words after:\n' \
                 '`{}`\n' \
                 'Most popular words before:\n' \
                 '`{}`\n' \
                 'Most popular words after the next:\n' \
                 '`{}`'
    DISTRIBUTIONS = 'Distribution of frequencies:\n' \
                    '`{}`\n' \
                    '`{}`\n' \
                    'Distribution of lengths:\n' \
                    '`{}`\n' \
                    '`{}`'
