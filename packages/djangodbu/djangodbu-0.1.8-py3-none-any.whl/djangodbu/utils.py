#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io

# COLORS FOR TERMINAL

RED     = '\033[0;31m'
GREEN   = '\033[0;32m'
BLUE    = '\033[0;34m'
CYAN    = '\033[0;36m'
MAGENTA = '\033[0;35m'
YELLOW  = '\033[0;33m'
WHITE   = '\033[0;37m'
BLACK   = '\033[0;30m'

RED_B     = '\033[1;31m'
GREEN_B   = '\033[1;32m'
BLUE_B    = '\033[1;34m'
CYAN_B    = '\033[1;36m'
MAGENTA_B = '\033[1;35m'
YELLOW_B  = '\033[1;33m'
WHITE_B   = '\033[1;37m'
BLACK_B   = '\033[1;30m'

RESET = '\033[0m'


B_RED     = '\033[0;41m'
B_GREEN   = '\033[0;42m'
B_BLUE    = '\033[0;44m'
B_CYAN    = '\033[0;46m'
B_MAGENTA = '\033[0;45m'
B_YELLOW  = '\033[0;43m'
B_WHITE   = '\033[0;47m'
B_BLACK   = '\033[0;40m'

B_RED_B     = '\033[30;41m'
B_GREEN_B   = '\033[30;42m'
B_BLUE_B    = '\033[30;44m'
B_CYAN_B    = '\033[30;46m'
B_MAGENTA_B = '\033[30;45m'
B_YELLOW_B  = '\033[30;43m'
B_WHITE_B   = '\033[30;47m'
B_BLACK_B   = '\033[30;40m'

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
REVERSE = '\033[7m'

def get_types(thing):
    try:
        import types
        _all_types = types.__all__

        thing_type = type(thing)
        return [t for t in _all_types if thing_type is getattr(types, t)]
    except:
        pass

def dse(*args, **kwargs):
    import ipdb
    try:
        ds(*args, **kwargs)
    except Exception as e:
        ipdb.post_mortem()

def ds(dictlike, searchstring, case_insensitive=True):
    if isinstance(dictlike, list):
        return _list_search(dictlike, searchstring, case_insensitive=case_insensitive)
    elif isinstance(dictlike, dict):
        return _dict_search(dictlike, searchstring, case_insensitive=case_insensitive)
    return 0

def _dict_search(somedict, string, case_insensitive=True, path='', done=None):
    dictid = id(somedict)

    if done is None:
        done = set([dictid])
    elif not dictid in done:
        done.add(dictid)

    if isinstance(somedict, list):
        _list_search(somedict, string, done=done)
        return

    for key, value in somedict.items():
        if (
            case_insensitive and (key.lower().find(string.lower()) != -1) or
            not case_insensitive and (key.find(string) != -1)
        ):
            # print path, 'KEY:', key
            print("{path} {col2}{key}{col0}:{rst} {value}".format(
                col0=BLACK_B,
                # col1=YELLOW_B,
                col2=RED_B,
                rst=RESET,
                key=key,
                value=repr(value),
                path=path + BLACK_B + " >" + RESET if path else ''
            ))
            # print YELLOW_B + path, RED_B + 'KEY:' + RESET, repr(value)

        if isinstance(value, str) or isinstance(value, str):
            if (
                case_insensitive and (value.lower().find(string.lower()) != -1) or
                not case_insensitive and (value.find(string) != -1)
            ):
                print("{path} {col2}{key} {col0}:{rst} {value}".format(
                    col0=BLACK_B,
                    col1=YELLOW_B,
                    col2=RED_B,
                    rst=RESET,
                    key=key,
                    value=repr(value),
                    path=path + BLACK_B + " >" + RESET if path else ''
                ))
                # print BLACK_B + path, BLUE_B + 'VALUE:' + RESET, repr(value)

        elif isinstance(value, dict):
            valueid = id(value)
            if valueid in done:
                continue
            # print '+', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=RED_B, col0=BLACK_B, rst=RESET, path=path, key=key) if path else RED_B + key + RESET
            _dict_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)
        elif isinstance(value, list):
            valueid = id(value)
            if valueid in done:
                continue
            # print '-', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=RED_B, col0=BLACK_B, rst=RESET, path=path, key=key) if path else RED_B + key + RESET
            _list_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)




def _list_search(somelist, string, case_insensitive=True, path='', done=None):
    listid = id(somelist)

    if done is None:
        done = set([listid])
    elif not listid in done:
        done.add(listid)

    if isinstance(somelist, dict):
        _dict_search(somelist, string, case_insensitive=case_insensitive, done=done)
        return

    for i, value in enumerate(somelist):
        if isinstance(value, str) or isinstance(value, str):
            if (
                case_insensitive and (value.lower().find(string.lower()) != -1) or
                not case_insensitive and (value.find(string) != -1)
            ):
                print("{path} {col2}{key}{rst} {col0}:{rst} {value}".format(
                    col0=BLACK_B,
                    col1=YELLOW_B,
                    col2=BLUE_B,
                    rst=RESET,
                    key=i,
                    value=repr(value),
                    path=path + BLACK_B + ' >' + RESET if path else ''
                ))
                # print BLACK_B + path, i, BLUE_B + 'VALUE:' + RESET, value
        elif isinstance(value, dict):
            valueid = id(value)
            if valueid in done:
                continue
            # print '+', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=BLUE_B, col0=BLACK_B, rst=RESET, path=path, key=i) if path else BLUE_B + str(i) + RESET
            _dict_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)
        elif isinstance(value, list):
            valueid = id(value)
            if valueid in done:
                continue
            # print '-', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=BLUE_B, col0=BLACK_B, rst=RESET, path=path, key=i) if path else BLUE_B + str(i) + RESET
            _list_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)


def ruler(length=71, pad=0, start_from_zero=True):
    rulermrks = "|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|"
    rulerdata = "0        10        20        30        40        50        60        70        80        90        100       110       120       130       140       150"

    if start_from_zero:
        return "{}\n{}".format(
            ''.join([' ' for _ in range(pad)]) + rulermrks[:length],
            ''.join([' ' for _ in range(pad)]) + rulerdata[:length]
        )

    return "{}\n{}".format(
        ''.join([' ' for _ in range(pad)]) + rulermrks[1:(length + 1)],
        ''.join([' ' for _ in range(pad)]) + rulerdata[1:(length + 1)]
    )

_encodings = [
    'utf-8',
    'latin1',
    'ascii',
    'ISO-8859-1',
    'ISO-8859-15',
]

_bytes_mapping = {
    9: '→',
    10: '␤',
    13: '␍',
}

def format_bytes(data):
    was_ascii = False
    buff = io.StringIO()
    for c in data:
        if 31 < c < 127:
            buff.write(chr(c))
            was_ascii = True
        elif was_ascii and (c in (10, 13, 9)):
            buff.write(f'\033[0;90m{_bytes_mapping[c]}\033[0m')
        else:
            # buff.write('\\' + hex(c)[])
            # buff.write(rf'\x{c:02x}')
            buff.write(f'\033[0;90m{c:02x}\033[0m')
            was_ascii = False

    return buff.getvalue()


def ascfix(input_text):
    if isinstance(input_text, bytes):
        print(input_text)
        # print type(input_text),
        print('bytes', end=' ')
        print("-decode-> unicode", end=' ')
        try:
            import chardet
            res = chardet.detect(input_text)
            print("({en} at ~{con})".format(en=res.get('encoding'), con=res.get('confidence')))
        except:
            print()

        for enc in _encodings:
            print("{}: ".format(enc))

            try:
                data = input_text.decode(enc, 'replace')
                # print "-> OK"

                for enc2 in _encodings:
                    print("  -> {}:".format(enc2), end=' ')
                    try:
                        data2 = str(data.encode(enc2, 'replace'))
                        print(data2)
                    except Exception as e:
                        print('Error')
                print()

            except Exception as e:
                print("-> Error")

    elif isinstance(input_text, str):
        print(input_text)
        # print type(input_text),
        print('str')
        print("-encode-> bytes")

        for enc in _encodings:
            print("{}: ".format(enc))
            print("  e: ", end=' ')
            try:
                data = str(input_text.encode(enc, 'replace'))
                print(data, input_text.encode(enc, 'replace'))
            except Exception as e:
                print("Error", e, end=' ')
                try:
                    data = input_text.encode(enc, 'replace')
                    print("-> OK")
                except Exception as e:
                    print("-> Error")

    else:
        print("-> not string")
        return
import logging
log = logging.getLogger(__name__)
import chardet
def uni(thing):
    if thing is None:
        return None

    if isinstance(thing, str):
        # log.debug(u'unicode: {}'.format(thing))
        # log.debug('is unicode')
        return thing

    if isinstance(thing, bytes):
        # log.debug('str {}'.format(thing))
        # log.debug('is str')
        try:
            return thing.decode('utf-8')
        except UnicodeDecodeError as e:

            return format_bytes(thing)

            # # log.debug(' not utf-8')
            # result = chardet.detect(thing)
            # charenc = result['encoding']
            # if charenc:
            #     return thing.decode(charenc, 'replace')
            # else:
            #     return '<undecodable bytes>'



    if isinstance(thing, (int, float)):
        # log.debug(u'number: {}'.format(thing))
        # log.debug('is number')
        return '{}'.format(thing)

    if hasattr(thing, '__unicode__'):
        try:
            # log.debug('__unicode__ {} -> {}'.format(repr(thing), thing.__unicode__()))
            # log.debug('has __unicode__()')
            return thing.__unicode__()
        except:
            # log.debug('  could not __unicode__()')
            pass
    if hasattr(thing, '__str__') and not isinstance(thing, type):
        # log.debug('__str__() {} -> {}'.format(repr(thing), uni(thing.__str__())))

        return uni(thing.__str__())

    return repr(thing)

def get_subqueus_req(elements, first=True):
    if not elements:
        # print '-'
        yield None
    elif len(elements) == 1:
        # print ' .', [elements]
        yield [elements]
    else:
        for w in range(1, len(elements)):
            for rest in get_subqueus_req(elements[w:], first=False):
                # if first:
                #     print '=> ', [elements[:w]], '+', rest
                # else:
                #     print '  <-', [elements[:w]], '+', rest
                yield [elements[:w]] + rest if rest else [elements]
        # yield [elements] if first else [elements]
        # if first:
        #     print '=> ', elements
        # else:
        #     print ' <=', [elements]
        yield [elements]



class _dict2props(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

cols = _dict2props(**{
    'black'         : (30, 40),
    'red'           : (31, 41),
    'green'         : (32, 42),
    'yellow'        : (33, 43),
    'blue'          : (34, 44),
    'magenta'       : (35, 45),
    'cyan'          : (36, 46),
    'white'         : (37, 47),
    'bright_black'  : (90, 100),
    'bright_red'    : (91, 101),
    'bright_green'  : (92, 102),
    'bright_yellow' : (93, 103),
    'bright_blue'   : (94, 104),
    'bright_magenta': (95, 105),
    'bright_cyan'   : (96, 106),
    'bright_white'  : (97, 107 ),
})


# 0	Reset / Normal
# 1	Bold or increased intensity
# 2	Faint (decreased intensity)
# 3	Italic
# 4	Underline
# 5	Slow Blink
# 6	Rapid Blink
# 7	reverse video
# 8	Conceal
# 9	Crossed-out
# 10	Primary(default) font
# 11–19	Alternative font


def shc(fg=None, bg=None, rev=None, under=None, bold=None, faint=None, italic=None, blinks=None, blinkr=None, con=None, cross=None, palette=None, true=None):
    '''
Colors:
- [bright_]black
- [bright_]red
- [bright_]green
- [bright_]yellow
- [bright_]blue
- [bright_]magenta
- [bright_]cyan
- [bright_]white

palette  = True
  colors: 0-255
true     = True
  colors:  (0,0,0) - (255,255,255)
    '''
    esc = '\x1b['  # \033[
    sep = ';'
    end = 'm'

    if not any((fg, bg, rev, under, bold, faint, italic, blinks, blinkr, con, cross)):
        return esc + '0' + end

    command = []

    if bold is not None and bold: command.append('1')
    if bold is not None and not bold: command.append('22')
    if faint is not None and faint: command.append('2')
    if faint is not None and not faint: command.append('22')
    if italic is not None and italic: command.append('3')
    if italic is not None and not italic: command.append('23')
    if under is not None and under: command.append('4')
    if under is not None and not under: command.append('24')
    if blinks: command.append('5')
    if blinkr: command.append('6')
    if rev is not None and rev: command.append('7')
    if rev is not None and not rev: command.append('27')
    if con: command.append('8')
    if cross: command.append('9')

    if fg:
        if palette:
            command.extend(['38', '5', str(fg)])
        elif true:
            if isinstance(fg, tuple):
                _r, _g, _b = fg
            else:
                _r, _g, _b = (fg, fg, fg)
            command.extend(['38', '2', str(_r), str(_g), str(_b)])
        else:
            command.append(str(getattr(cols, fg)[0]))

    if bg:
        if palette:
            command.extend(['48', '5', str(bg)])
        elif true:
            if isinstance(bg, tuple):
                _r, _g, _b = bg
            else:
                _r, _g, _b = (bg, bg, bg)
            command.extend(['48', '2', str(_r), str(_g), str(_b)])
        else:
            command.append(str(getattr(cols, bg)[1]))

    if not command:
        command.append('0')

    return esc + sep.join(command) + end

def print_colors():
    colornames = [
        'black',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ]

    print('RESET    ' + \
          'NORMAL   ' + \
          'BOLD     ' + \
          'BRIGHT   ' + \
          'FAINT    ' + \
          'REVERSE  ')

    print('{name:9}{norm}{name:9}{rst}{bold}{name:9}{rst}{bright}{name:9}{rst}{faint}{name:9}{rst}{rev}{name:9}{rst}'.format(
        name="text",
        rst=shc(),
        norm=shc(),
        bold=shc(bold=True),
        bright='',
        faint=shc(faint=True),
        rev=shc(rev=True),
    ))

    for c in colornames:
        print('{name:9}{norm}{name:9}{rst}{bold}{name:9}{rst}{bright}{name:9}{rst}{faint}{name:9}{rst}{rev}{name:9}{rst}'.format(
            name=c,
            rst=shc(),
            norm=shc(c),
            bold=shc(c, bold=True),
            bright=shc('bright_'+c),
            faint=shc(c, faint=True),
            rev=shc(c, rev=True),
        ))

def color_bool(value):
    if value:
        return '{}{}{}'.format(GREEN, value, RESET)
    return '{}{}{}'.format(RED, value, RESET)


def ddiff(da, db, annotate=None):
    from collections import OrderedDict
    ka = set(da.keys())
    kb = set(db.keys())

    path = '[{}]'.format(annotate) if annotate else ''

    for k in ka.union(kb):
        if k not in ka:
            print('{} + {}'.format(path, k))
            continue

        if k not in kb:
            print('{} - {}'.format(path, k))
            continue

        va = da[k]
        vb = db[k]

        if type(va) != type(vb):
            if isinstance(va, (dict, OrderedDict)) and isinstance(vb, (dict, OrderedDict)):
                pass
            elif isinstance(va, str) and isinstance(vb, str):
                pass
            else:
                print('{} ~ {}: MOD  {}{} -> {}{}'.format(path, k, type(va), va, type(vb), vb))
                continue

        if isinstance(va, (tuple, list)):
            ldiff(va, vb)
            continue

        if isinstance(va, (dict, OrderedDict)):
            ddiff(va, vb, k)
            continue

        if va != vb:
            print('{} ~ {}: MOD  {} -> {}'.format(path, k, va, vb))

def ldiff(la, lb, annotate=None):
    if len(la) != len(lb):
        print('{}: LEN  {} - {}'.format(annotate, len(la), len(lb)))
        return

    for i, (va, vb) in enumerate(zip(la, lb)):
        if va != vb:
            print('{} DIFF  {} -> {}'.format('[{}][{}]'.format(annotate, i), va, vb))


def parse_parens_notation(text):
    '''
    'asdf, bsdf(csdf), dsdf(esdf, hsdf), isdf(jsdf(ksdf))'
    ->
    'asdf', 'bsdf__csdf', 'dsdf__esdf', 'dsdf__hsdf', 'isdf__jsdf__ksdf'
    '''
    a = 0
    prev_levels = []
    current_level = []

    for i, c in enumerate(text):
        if c in ',()':
            chunk = text[a: i].strip()
            # print(f"'{chunk}'")
            if chunk: current_level.append(chunk)
            a = i + 1

            if c == '(':
                # print(' >')
                prev_levels.append(current_level)
                current_level = []

            elif c == ')':
                # print(' <')
                if not prev_levels:
                    raise Exception(f'unexpected ) at {i}')
                children = current_level
                current_level = prev_levels.pop()
                parent = current_level.pop()
                current_level.extend([f'{parent}__{child}' for child in children])

            # print(f':: {current_level}   : {prev_levels}')

        else: pass

    if prev_levels:
        raise Exception('unclosed (')

    if a != len(text):
        chunk = text[a:].strip()
        if chunk:
            current_level.append(chunk)

    return current_level

def _indent(text, indentation, skip_first=False):
    if isinstance(text, list):
        _indent = ' ' * indentation
        return [_indent + line for line in text]

    import re
    def ansi_sequence_positions(_t):
        ansq = re.compile(r'\x1B\[[0-9;]+m')
        ansq_ranges = []
        current = 0
        while True:
            m = ansq.search(_t, current)
            if not m: break
            start, stop = m.span()
            ansq_ranges.append((start, stop))
            current = stop + 1
        return ansq_ranges

    def non_ansi_chunk(_t, width):
        ansq_ranges = ansi_sequence_positions(_t)
        # from .unihl import symbolize
        char_count = 0
        seg_start = 0

        inside_sq = False
        sq_start, sq_stop = None, None
        if ansq_ranges: sq_start, sq_stop = ansq_ranges.pop(0)
        # TODO: change this to non iterating style, since all the chunks can be calculated
        for i, c in enumerate(_t):
            if not inside_sq and sq_start and i == sq_start:
                inside_sq = True
                # print('(')
            elif inside_sq and sq_stop and i == sq_stop - 1:
                inside_sq = False
                if ansq_ranges: sq_start, sq_stop = ansq_ranges.pop(0)
                # print(')', symbolize(c))
            elif not inside_sq:
                # print('.', symbolize(c), i)
                char_count += 1
                if char_count == width + 1:
                    yield _t[seg_start : i + 1]
                    char_count = 0
                    seg_start = i + 1
            else:
                # print('*', symbolize(c))
                pass
        yield _t[seg_start : ]

    from .terminalsize import get_terminal_size
    twidth, _ = get_terminal_size()

    lines = []
    skip = skip_first
    _indent = ' ' * indentation
    for chunk in non_ansi_chunk(text, width=twidth - indentation - 1):
        if skip:
            lines.append(chunk)
            skip = False
            continue
        lines.append(_indent + chunk)

    return lines


    # print(f'tw:{twidth}  i:{indentation}  w:{twidth - indentation}')

    # for chunk in non_ansi_chunk(text, width=twidth - indentation - 1):
        # print(' ' * indentation + chunk)

def _columnize(list_of_strings):
    from .terminalsize import get_terminal_size
    import math

    tw, th = get_terminal_size()
    num_lines = len(list_of_strings)
    sizes = [len(x) for x in list_of_strings]
    optimal_cols = math.ceil(num_lines / th)

    longest = max(sizes)
    num_cols = math.floor(tw / (longest + 1))

    # return longest, num_cols, optimal_cols

    # split lines to <num_cols> columns
    col_lines = math.ceil(num_lines / num_cols)
    col_chunks = []
    for a, b in zip(range(num_cols), range(1, num_cols+1)):
        # print(a, b)
        col_chunks.append(list_of_strings[a*col_lines: b*col_lines])
    # return col_chunks

    from itertools import zip_longest
    for _cols in zip_longest(*col_chunks, fillvalue=''):
        print(' '.join('{data:{longest}}'.format(data=_c, longest=longest) for _c in _cols))

