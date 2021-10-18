# File to configure simple substitution plugins, like /goth, /bubble, etc.,
# which just translate the alphabet [a-zA-Z] to some equivalents in another
# script.

from plugin import create_plugin
from message import SteelyMessage

# Helper method to create a plugin that just translates the alphabet.


def create_substitution_plugin(command, author, help, trans, normal=None):
    NORMAL = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if normal is not None:
        NORMAL = normal

    TRANS = str.maketrans(NORMAL, trans)

    plugin = create_plugin(name=command, author=author, help=help)

    @plugin.listen(command=command)
    def plugin_listener(bot, trigger: SteelyMessage, **kwargs):
        message = bot.fetchThreadMessages(
            thread_id=trigger.thread_id, limit=2)[1]
        text = message.text.translate(TRANS)
        bot.sendMessage(text,
                        thread_id=trigger.thread_id,
                        thread_type=trigger.thread_type)

create_substitution_plugin('goth', 'iandioch', 'It\'s not just a phase mom',
                           '𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ')

create_substitution_plugin('vape', ['alexkraak', 'sentriz'], 'gives the previous command ａｅｓｔｈｅｔｉｃ',
                           trans='　０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［\\］＾＿｛｜｝～',
                           normal=' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[\\]^_{|}~')


# TODO(iandioch): Make RUNE_TRANS consist of unique letters, so that it can
# allow a two-way translation.
RUNE_TRANS = '🜣🜖🝔🜵🞌🝗🜶🜘🜶🜶🝁🜾🝀🝀🜃🜵🜣🜛🜖🜟🜫🜾🝁🝖🜞🜖🜺🜾🜴🜃🜵🝞🜶🝔🝁🜖🜴🝔🜾🝁🝳🜵🜃🜾🝗🜶🝁🞌🝀🜣🜶🝁'
RUNE_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
create_substitution_plugin('rune', 'iandioch', 'buenos dias',
                           trans=RUNE_TRANS + RUNE_ALPHABET,
                           normal=RUNE_ALPHABET + RUNE_TRANS)

BUBBLE_TRANS = 'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ'
BUBBLE_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
create_substitution_plugin('bubble', 'iandioch', 'ⓐyy lmao',
                           trans=BUBBLE_TRANS + BUBBLE_ALPHABET,
                           normal=BUBBLE_ALPHABET + BUBBLE_TRANS)

EGYPT_TRANS = '𓊏𓊐𓊑𓊒𓊓𓊔𓊕𓊖𓊗𓊘𓊙𓊚𓊛𓊜𓊝𓊞𓊟𓊠𓊡𓊢𓊣𓊤𓊥𓊦𓊧𓊨𓊩𓊪𓊫𓊬𓊭𓊮𓊯𓊰𓊱𓊲𓊳𓊴𓊵𓊶𓊷𓊸𓊹𓊺𓊻𓊼𓊽𓊾𓊿𓋀𓋁𓋂'
EGYPT_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
create_substitution_plugin('egypt', 'iandioch', 'walklikeanegyptian',
                           trans=EGYPT_TRANS + EGYPT_ALPHABET,
                           normal=EGYPT_ALPHABET + EGYPT_TRANS)

LEET_TRANS = '48(d3f9#|jklmn0pqr5+uvwxy2'
LEET_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
create_substitution_plugin('leet', 'sentriz', 'gives the previous command leet',
                           trans=LEET_TRANS + LEET_ALPHABET,
                           normal=LEET_ALPHABET + LEET_TRANS)

PROD_TRANS = '𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵'
PROD_ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
create_substitution_plugin('prod', 'iandioch', 'Get te fuck ye taigy bastards',
                           trans=PROD_TRANS + PROD_ALPHABET,
                           normal=PROD_ALPHABET + PROD_TRANS)
