from telegram.ext import Updater, CommandHandler
from re import fullmatch
from io import StringIO
from ngram import Trainer, Generator
from .wiki_parser import WikiParser, WikiError
from .stat_model import StatisticsModel
from .resources import Replies


class Bot:
    def __init__(self, token, **kwargs):
        updater = Updater(token, **kwargs)

        add = updater.dispatcher.add_handler
        add(CommandHandler('start', self.start))
        add(CommandHandler('teach', self.teach, pass_chat_data=True))
        add(CommandHandler('write', self.write, pass_chat_data=True))
        add(CommandHandler('top', self.top, pass_chat_data=True))
        add(CommandHandler('stop_words', self.stop_words, pass_chat_data=True))
        add(CommandHandler('word_cloud', self.word_cloud, pass_chat_data=True))
        add(CommandHandler('describe', self.describe, pass_chat_data=True))
        add(CommandHandler('help', self.help))

        updater.start_polling()

        self.updater = updater

    def idle(self):
        self.updater.idle()

    def start(self, bot, update):
        update.message.reply_text(Replies.START, 'Markdown')

    def help(self, bot, update):
        update.message.reply_text(Replies.HELP, 'Markdown')

    def teach(self, bot, update, chat_data):
        args = update.message.text.split(' ', 2)
        if len(args) < 3 or not args[1].isnumeric():
            update.message.reply_text(Replies.WRONG_ARGS, 'Markdown')
            return

        max_depth = int(args[1])
        link = args[2]

        match = fullmatch(r'.*(..)\.wikipedia\.org/wiki/(.+)', link)
        if match is None:
            update.message.reply_text(Replies.WRONG_URL)
            return

        wiki_parser = WikiParser(max_depth, match[1])
        try:
            wiki_parser.check_title(match[2])
        except WikiError as ex:
            if len(ex.options):
                update.message.reply_text(Replies.DISAMBIGUATION
                                          .format('\n'.join(ex.options)),
                                          'Markdown')
            else:
                update.message.reply_text(f'No such page: {match[2]}')
            return

        update.message.reply_text('Started learning process.')

        trainer = Trainer(model=StatisticsModel(n=3))
        for text in wiki_parser.links_iter(match[2]):
            trainer.train(StringIO(text))

        model = trainer.get_model()
        chat_data['model'] = model
        update.message.reply_text('Successfully learned.')

    @staticmethod
    def _check_model(update, chat_data):
        if 'model' not in chat_data:
            update.message.reply_text(Replies.NOT_LEARNED, 'Markdown')
            return False
        return True

    def write(self, bot, update, chat_data):
        args = update.message.text.split(' ')
        if len(args) != 2 or not args[1].isnumeric():
            update.message.reply_text(Replies.WRONG_ARGS, 'Markdown')
            return

        length = int(args[1])

        if not self._check_model(update, chat_data):
            return

        model = chat_data['model']
        generator = Generator(model)

        text = generator.generate(length)

        update.message.reply_text(text.capitalize())

    def describe(self, bot, update, chat_data):
        self._check_model(update, chat_data)

        args = update.message.text.split(' ')
        if len(args) > 2:
            update.message.reply_text(Replies.WRONG_ARGS, 'Markdown')
            return

        if len(args) == 2:
            stats = chat_data['model'].describe_word(args[1])
            if stats is None:
                update.message.reply_text('Word `{}` was not found in texts.'
                                          .format(args[1]),  'Markdown')
            else:
                update.message.reply_text(Replies.WORD_STATS
                                          .format(args[1], stats[0], stats[1],
                                                  ', '.join(stats[2]),
                                                  ', '.join(stats[3]),
                                                  ', '.join(stats[4]),),
                                          'Markdown')
        else:
            freqs, lens = chat_data['model'].describe_all()
            freqs = [[str(i).ljust(4) for i in j] for j in zip(*freqs)]
            lens = [[str(i).ljust(4) for i in j] for j in zip(*lens)]
            update.message.reply_text(Replies.DISTRIBUTIONS
                                      .format(''.join(freqs[0]),
                                              ''.join(freqs[1]),
                                              ''.join(lens[0]),
                                              ''.join(lens[1])),
                                      'Markdown')

    def stop_words(self, bot, update, chat_data):
        self._check_model(update, chat_data)

        stops = sorted(chat_data['model'].get_stop_words())

        update.message.reply_text('Stop words are:\n`{}`'
                                  .format('\n'.join(stops)), 'Markdown')

    def top(self, bot, update, chat_data):
        args = update.message.text.split(' ', 2)
        if len(args) < 3 or not args[1].isnumeric()\
                or not (args[2] == 'asc' or args[2] == 'desc'):
            update.message.reply_text(Replies.WRONG_ARGS, 'Markdown')
            return

        self._check_model(update, chat_data)

        count = int(args[1])
        order = args[2] == 'desc'

        words = '\n'.join(chat_data['model'].get_top(count, order))

        update.message.reply_text('{} popular words:\n'
                                  '`{}`\n'
                                  .format('Most' if order else 'Least',
                                          words), 'Markdown')

    def word_cloud(self, bot, update, chat_data):
        self._check_model(update, chat_data)

        image = chat_data['model'].word_cloud(0)

        update.message.reply_photo(photo=image)
