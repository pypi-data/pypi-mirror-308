import re
from itertools import zip_longest, chain

import datetime as dt

from .terminalsize import get_terminal_size
from .shell import RESET, GREEN, MAGENTA, CYAN, YELLOW, RED, WHITE, ansisequence

from django.db import models

LOCK_ICON = '\U0001f512'
# LOCK_ICON = 'L'

def _get_field_types(obj):
    fields = obj._meta.fields
    many_to_many = obj._meta.many_to_many
    related_objects = obj._meta.related_objects

    lookup = {}
    for f in fields:
        related_model = getattr(f, 'related_model', None)
        lookup[f.name] = 'F' if not related_model else 'FR'
    for f in many_to_many:
        lookup[f.name] = 'M'
    for f in related_objects:
        lookup[f.name] = 'R'
    return lookup

def shell_print_model(obj):
    # from django.db.models.query_utils import DeferredAttribute
    # from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor
    # from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor

    '''
        obj._meta
        - concrete_fields
        - fields

        - fields_map
        - related_objects
    '''
    # rev_props = [getattr(obj._meta, x, None) for x in obj._meta.REVERSE_PROPERTIES]
    # local_fields = obj._meta.local_fields

    fields = obj._meta.fields
    many_to_many = obj._meta.many_to_many
    related_objects = obj._meta.related_objects

    # hidden = [v for k, v in obj._meta.fields_map.items() if '+' in k]


    from model_utils.choices import Choices
    from model_utils.tracker import FieldTracker
    from django.db.models import Manager


    # asdf = [x for x in dir(obj) if isinstance(getattr(obj, x), (str, Choices, FieldTracker, Manager)) and x not in ('__doc__', '__module__')]
    # meta = obj.Meta

    # print object name type meta

    header = repr(obj)


    primary_data = []
    for field in chain(fields, many_to_many):
        name = field.name
        unique = field.unique
        related_model = getattr(field, 'related_model', None)
        kind = type(field)
        _kind = _strip_class(kind)
        null_allowed = field.null
        has_default = field.has_default()

        editable = field.editable
        index = field.db_index
        primary = field.primary_key
        concrete = field.concrete

        color = color_lookup_label.get(_kind, cNONE)

        label = color('\x1b[4m' + name if unique else name)

        # extra = (None,)
        if related_model:
            rel_color = on_delete_lookup.get(field.remote_field.on_delete, cNONE)
            rel_symbol = '->' if not field.many_to_many else '=>'
            label = cMAGENTA(name)
            description = rel_color(rel_symbol + ' ') + cYELLOW(_strip_class(related_model))
            if field._related_name == '+': description += cBLACK_B(' +')
        elif _kind in ('CharField', 'UUIDField'):
            description = color(_kind) + f' {field.max_length}'
        elif _kind in ('DecimalField',):
            description = color(_kind) + f' {field.max_digits - field.decimal_places}+{field.decimal_places}'
        elif _kind in ('BooleanField',):
            description = color(_kind) + f' {field.default}'
        else:
            description = color(_kind) #+ (' null' if null else '')
            # extra = ('null' if field.null else '', 'blank' if field.blank else '')

        # if unique:
        #     label = '\x1b[4m' + label


        # description = (cWHITE('*') if null else ' ') + description

        icons = ''

        # if not editable:
        #     icons += cRED('E')
        # else:
        #      icons += ' '

        # if not concrete:
        #     icons += cMAGENTA('~')
        # else:
        #      icons += ' '

        # if field.hidden:
        #     icons += cBLACK_B('H')
        # else:
        #      icons += ' '

        # if field.auto_created:
        #     icons += cMAGENTA_B('a')
        # else:
        #      icons += ' '

        if (not null_allowed
            and not has_default
            and not field.many_to_many
            and not field.auto_created
            and not field.blank):

            icons += cWHITE('*')
        else:
            icons += ' '

        icons += ' '

        # icons += ' ' * max(0, 2 - num_chars(icons) )
        label = icons + label

        # label = (cWHITE('* ') if not null_allowed and not has_default and not field.many_to_many else '  ') + label
        # label = ('n' if null_allowed else '') + ('d' if has_default else '') + ' ' + label


        # if related_model:
        #     description = ' -> ' + description

        primary_data.append((label, description) )

    managers = [x for x in dir(obj) if isinstance(getattr(obj, x), Manager)]
    # if managers:
        # cell = ['  Managers:']
    for attr in managers:
        data = getattr(obj, attr)
        label = '  ' + attr
        description = _strip_class(type(data))
        if description == 'Manager':
            label = cBLACK_B(label)
            description = cBLACK_B(description)
        else:
            label = cMAGENTA_B(label)
            description = cMAGENTA_B(description)
        primary_data.append((label, description) )
            # cell.append(f'    {attr} - {_strip_class(type(data))}')
        # cells.append(cell)

    trackers = [x for x in dir(obj) if isinstance(getattr(obj, x), FieldTracker)]
    for attr in trackers:
        # cell = ['  Trackers:']
        # for attr in trackers:
        #     data = getattr(obj, attr)
        #     cell.append(f'    {attr} ({", ".join(data.field_map.keys())})')
        # cells.append(cell)
        data = getattr(obj, attr)
        label = '  ' + cRED(attr)
        _fields = list(data.field_map.keys())
        if len(_fields) > 3:
            _fields = _fields[:3] + ['...']
        description = cRED(f'FieldTracker({", ".join(_fields)})')
        primary_data.append((label, description) )

    secondary_data = []

    # for field in sorted(chain(related_objects, many_to_many), key=lambda x: x.name):
    for field in sorted(related_objects, key=lambda x: x.name):
        name = get_accessor(field) or field.name
        related_model = getattr(field, 'related_model', None)
        kind = type(field)
        _kind = _strip_class(kind)

        description =  cMAGENTA(name) + ' ' + cBLACK_B('(' +  _strip_class(related_model) + ')')
        if '+' in name:
        #     import ipdb; ipdb.set_trace(context=5) # TODO: remove this debug
        #     description = name + ': ' + _strip_class(field.model) + ' - ' + _strip_class(related_model)
        # if name == '+':
            description = cBLACK_B('(' +  _strip_class(related_model) + ')')

        # if related_model:
        #     label = cMAGENTA(name)
        #     description = '-> ' + cYELLOW(_strip_class(related_model))

        # else:
        #     description = color(_strip_class(kind))
        #     extra = ('null' if field.null else 'non-null', 'blank' if field.blank else 'non-blank')

        if field.many_to_one:
            label = '>'
        elif field.one_to_one:
            label = '-'
        elif field.many_to_many:
            label = '='
        elif field.one_to_many:
            label = '<'
        else:
            label = '?'


        secondary_data.append((label, description))

    col_primary = _output_table(
        primary_data,
        header=False,
        align=['<', '<'],
        format_only=True,
    )

    col_secondary = _output_table(
        secondary_data,
        header=False,
        align=['<', '<'],
        format_only=True,
    )

    props = _output_table(
        [(cRED('@') + attr_name,) for attr_name in dir(obj) if isinstance(getattr(obj, attr_name, None), property) and attr_name != 'pk'],
        header=False,
        format_only=True,
    )

    # we can print out info at this point
    lines = _parallel_cols(col_primary, col_secondary, props)

    # lines += _layout_cells(cells)

    lines.insert(0, header)
    lines = _center_output(lines)
    print('\n'.join(lines))

    # layout and print of rest of stuff
    lines = []

    choices = [x for x in dir(obj) if isinstance(getattr(obj, x), Choices)]
    rest = [x for x in dir(obj) if isinstance(getattr(obj, x), (str, int, dict, list, tuple)) and x not in ('__doc__', '__module__')]

    cells = []
    # group choices and rest
    for choice_attr in choices:
        cell = []
        choice_data = getattr(obj, choice_attr)
        choices = choice_data._triples if not (all(x[0] == x[1] for x in choice_data._triples)) else choice_data._doubles
        choices = sorted(choices, key=lambda x: x[0])
        if choice_attr == 'COMPANY_STATUSES': choices = [(_status_color_lookup.get(c[0], cNONE)(c[0]), c[1]) for c in choices]

        cell = _output_table(choices, header=False, format_only=True, left_pad=4)
        cell.insert(0, f'  {cWHITE(choice_attr)} (Choices)')
        cells.append(cell)

    if rest:
        cell = ['  Other:']
        for attr in rest:
            _data = getattr(obj, attr)
            cell.append(f'    {attr}: {_data} ({_strip_class(type(_data))})')
        cells.append(cell)

    # if managers:
    #     cell = ['  Managers:']
    #     for attr in managers:
    #         data = getattr(obj, attr)
    #         cell.append(f'    {attr} - {_strip_class(type(data))}')
    #     cells.append(cell)



    # lines = _parallel_cols(col_primary, col_secondary, props)

    lines += _layout_cells_wide(cells)

    # lines.insert(0, header)
    lines = _center_output(lines)


    if lines: print()
    print('\n'.join(lines))


cRED     = lambda x: f'\033[0;31m{x}\033[0m'
cGREEN   = lambda x: f'\033[0;32m{x}\033[0m'
cBLUE    = lambda x: f'\033[0;34m{x}\033[0m'
cCYAN    = lambda x: f'\033[0;36m{x}\033[0m'
cMAGENTA = lambda x: f'\033[0;35m{x}\033[0m'
cYELLOW  = lambda x: f'\033[0;33m{x}\033[0m'
cWHITE   = lambda x: f'\033[0;37m{x}\033[0m'
cBLACK   = lambda x: f'\033[0;30m{x}\033[0m'

cRED_B     = lambda x: f'\033[1;31m{x}\033[0m'
cGREEN_B   = lambda x: f'\033[1;32m{x}\033[0m'
cBLUE_B    = lambda x: f'\033[1;34m{x}\033[0m'
cCYAN_B    = lambda x: f'\033[1;36m{x}\033[0m'
cMAGENTA_B = lambda x: f'\033[1;35m{x}\033[0m'
cYELLOW_B  = lambda x: f'\033[1;33m{x}\033[0m'
cWHITE_B   = lambda x: f'\033[1;37m{x}\033[0m'
cBLACK_B   = lambda x: f'\033[1;30m{x}\033[0m'

cWHITE_F = lambda x: f'\x1b[2;37m{x}\033[0m'
cCYAN_F = lambda x: f'\x1b[2;36m{x}\033[0m'
cBLUE_F = lambda x: f'\x1b[2;34m{x}\033[0m'
cNONE = lambda x: x


shortlistc = lambda *args, **kwargs: kwargs.pop('joiner', ', ').join([cGREEN(l) if b else cRED(l) for (l, b) in args])

color_lookup_label = {
    'AutoField': cMAGENTA_B,
    'AutoCreatedField': cMAGENTA_B,
    'AutoLastModifiedField': cMAGENTA_B,
    'OrderWrt': cMAGENTA_B,
    'UUIDField': cWHITE,
    'BooleanField': cBLUE_B,
    'CharField': cGREEN,
    'TextField': cGREEN_B,
    'EmailField': cRED_B,
    'DecimalField': cWHITE,
    'IntegerField': cWHITE,
    'PositiveSmallIntegerField': cWHITE,
    'SmallIntegerField': cWHITE,
    'PositiveIntegerField': cWHITE,
    'DateField': cCYAN,
    'DateTimeField': cCYAN,
    'ImageField': cRED_B,
    'VersatileImageField': cRED,
    'FileField': cRED,
}

on_delete_lookup = {
    models.PROTECT: cBLUE_B,
    models.SET_NULL: cYELLOW_B,
    models.CASCADE: cRED_B,
    models.DO_NOTHING: cWHITE,
    models.SET: cGREEN,
    models.SET_DEFAULT: cGREEN_B,
}


RE_CLASS = r"<class '(.*)'>"

def _strip_class(thing):
    text = str(thing)
    full_class = re.match(RE_CLASS, text).group(1)
    return full_class.split('.')[-1]


ap = lambda v, w: max(0, w - num_chars(v)) * ' '
apr = lambda v, w: ap(v, w) + v
apl = lambda v, w: v + ap(v, w)

num_chars = lambda line: 0 if line is None else len(ansisequence.sub('', line))

_field_colors = {
    'CharField': cGREEN,
    'ForeignKey': cMAGENTA,
    'DateField': cCYAN,
    'DateTimeField': cCYAN,
    'AutoField': cYELLOW,
    'BooleanField': cRED,
    'IntegerField': cWHITE,
    'PositiveSmallIntegerField': cWHITE,
}

def _center_output(rows):
    if not rows: return rows
    terminal_width, terminal_height = get_terminal_size()
    row_length_max = max(num_chars(r) for r in rows)
    padding = (terminal_width - row_length_max) // 2
    _p = ' ' * padding
    return [_p + r for r in rows]

def _parallel_cols(*line_cols):
    output = []
    filtered = list(filter(None, line_cols))
    col_widths = [max(num_chars(row) for row in col) for col in filtered]

    for col_vals in zip_longest(*filtered, fillvalue=''):
        output.append(
            '    '.join(apl(x, w) for x, w in zip(col_vals, col_widths))
        )

    return output


def get_structure(thing, child=False):
    enclose = None
    values = None
    if isinstance(thing, list):
        enclose = ('[', ']')
        values = [get_structure(x, child=True) for x in thing]
    elif isinstance(thing, tuple):
        enclose = ('(', ')')
        values = [get_structure(x, child=True) for x in thing]
    elif isinstance(thing, dict):
        enclose = ('{', '}')
        values = [get_structure(x, child=True) for x in thing.values()]
    elif isinstance(thing, str):
        enclose = ("'", "'")
    elif isinstance(thing, int):
        values = '0'
    else:
        values = f'{type(thing)}'

    v = ''
    if values and isinstance(values, list):
        v = '\n'.join(values)
    elif values:
        v = values
    if enclose:
        return enclose[0] + v + enclose[1]
    return v



def _get_output(value):
    if isinstance(value, SPACE): return value
    if isinstance(value, type):
        t = _strip_class(value)
        c = _field_colors.get(t, cNONE)
        return c(t)
    if isinstance(value, str): return value
    if isinstance(value, (int, float)): return str(value)
    if isinstance(value, dt.datetime): return value.strftime('%Y-%m-%d')
    return str(value)

class SPACE:
    def __len__(*args, **kwargs): return 0
    def __repr__(*args, **kwrags): return ''


def _output_table(rows, header=None, align=None, format_only=False, left_pad=0):
    if not rows: return None


    _a = align or ['<'] * len(rows[0])

    processed = [[_get_output(v) for v in row] if row is not SPACE else row for row in rows]

    widths = [[0 if v is None else num_chars(v) for v in row] for row in [header or [''] * len(rows[0])] + processed if row != SPACE]  # value widths
    col_widths = [max(d) for d in zip_longest(*widths, fillvalue=0)]                                # maximum of each col

    output = []

    _A = {'<': apl,
          '>': apr,
          '': apl,
          None: apl}

    pad = left_pad * ' '

    # header row
    if header:
        output.append(pad + ('  '.join(_A[a](h, w) for h, w, a in zip_longest(header, col_widths, _a))))
        output.append('-' * len(output[-1]))

    for row in processed:
        if row == SPACE:
            output.append('')
        else:
            output.append(pad + ('  '.join(_A[a](r, w) for r, w, a in zip_longest(row, col_widths, _a, fillvalue=''))))

    if format_only: return output
    print('\n'.join(output))

from itertools import permutations

def _layout_cells(cells):
    if not cells: return []
    output = []

    terminal_width, terminal_height = get_terminal_size()

    def get_dims(_c):
        if isinstance(_c, (list, tuple)):
            if not _c: return 0, 0
            return len(_c), max(num_chars(x) for x in _c)
        return 1, len(_c) # for everything else?

    dims = [(i, get_dims(cell)) for i, cell in enumerate(cells)]

    # layout to columns
    # bruteforce all layouts into columns
    # all sequences -> divided into columns
    # for seq in permutations(dims):
    #     pass

    # layout from first to last
    output = [row for cell in cells for row in cell]
    return output

def _layout_cells_wide(cells):
    if not cells: return []
    output = []

    terminal_w, terminal_h = get_terminal_size()

    def get_dims(_c):
        if isinstance(_c, (list, tuple)):
            if not _c: return 0, 0
            return len(_c), max(num_chars(x) for x in _c)
        return 1, len(_c) # for everything else?

    dims = [(i, get_dims(cell)) for i, cell in enumerate(cells)]

    # lay out to columns, starting from left -> right until no more space
    # then start new "row"
    current_row = []
    cell_rows = [current_row]
    used_w = 0
    for (i, (dim_h, dim_w)), cell in zip(dims, cells):
        if used_w and dim_w + used_w > terminal_w:
            # print('new row')
            current_row = []
            cell_rows.append(current_row)
            used_w = 0

        current_row.append(cell)
        # print('cell', terminal_w, used_w, dim_w)
        used_w += dim_w + 2

    output = []

    for row in cell_rows:
        lines = _parallel_cols(*row)
        output += lines
        output += ['']  # add empty line between cell rows

    return output


    # layout to columns
    # bruteforce all layouts into columns
    # all sequences -> divided into columns
    # for seq in permutations(dims):
    #     pass

    # layout from first to last
    # output = [row for cell in cells for row in cell]
    # return output


def get_accessor(field):
    try: return field.get_accessor_name()
    except: pass


_status_color_lookup = {
    'ACCOUNTING'             : cMAGENTA,
    'ACTIVE_BILLING'         : cGREEN_B,
    'BILLED_NORECEIPTS'      : cGREEN_B,
    'DELETABLE'              : cYELLOW,
    'DEMO'                   : cMAGENTA,
    'DID_NOT_PAY'            : cYELLOW,
    'DOCUMENT'               : cBLUE,
    'ERROR'                  : cRED,
    'FORMER_CUSTOMER'        : cBLACK_B,
    'FREE'                   : cMAGENTA,
    'HANDLED'                : cYELLOW,
    'HANDLED_BUT_STILL_USING': cRED,
    'INACTIVE'               : cBLACK_B,
    'LEFT_DURING_TESTUSE'    : cBLACK_B,
    'NEW'                    : cWHITE,
    'NOT_ENOUGH_USE'         : cYELLOW,
    'NOT_SUITABLE'           : cYELLOW,
    'ORDER_CANCELLED'        : cBLACK_B,
    'ORDER_CANCELLED_TESTUSE': cBLACK_B,
    'PARTNER'                : cMAGENTA,
    'PAYER'                  : cMAGENTA,
    'PAYING_CUSTOMER'        : cGREEN,
    'PILOT'                  : cYELLOW,
    'SUPPORTER'              : cGREEN_B,
    'SWEDEN'                 : cYELLOW_B,
    'TEST'                   : cGREEN_B,
    'TESTUSE_STARTED'        : cGREEN,
    'TO_BILLING'             : cGREEN,
}
