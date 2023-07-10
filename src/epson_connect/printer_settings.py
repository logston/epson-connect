import random
import string

VALID_PRINT_MODES = {
    'document',
    'photo',
}

VALID_MEDIA_SIZES = {
    'ms_a3',
    'ms_a4',
    'ms_a5',
    'ms_a6',
    'ms_b5',
    'ms_tabloid',
    'ms_letter',
    'ms_legal',
    'ms_halfletter',
    'ms_kg',
    'ms_l',
    'ms_2l',
    'ms_10x12',
    'ms_8x10',
    'ms_hivision',
    'ms_5x8',
    'ms_postcard',
}

VALID_MEDIA_TYPES = {
    'mt_plainpaper',
    'mt_photopaper',
    'mt_hagaki',
    'mt_hagakiphoto',
    'mt_hagakiinkjet',
}

VALID_PRINT_QUALITIES = {
    'high',
    'normal',
    'draft',
}

VALID_PAPER_SOURCES = {
    'auto',
    'rear',
    'front1',
    'front2',
    'front3',
    'front4',
}

VALID_COLOR_MODES = {
    'color',
    'mono',
}

VALID_TWO_SIDE = {
    'none',
    'long',
    'short',
}


def merge_with_default_settings(settings=None):
    settings = settings or {}

    job_name = settings.get('job_name') or ''
    if not job_name:
        # Generate random name if one is not given.
        job_name = 'job-' + ''.join(random.choice(string.ascii_letters) for _ in range(8))

    settings['job_name'] = job_name

    settings['print_mode'] = settings.get('print_mode') or 'document'

    print_setting = settings.get('print_setting') or {}

    # print_setting is optional so we can exit early if its not present.
    if not print_setting:
        return settings

    collate = print_setting.get('collate')
    settings['print_setting'] = {
        'media_size': print_setting.get('media_size') or 'ms_a4',
        'media_type': print_setting.get('media_type') or 'mt_plainpaper',
        'borderless': print_setting.get('borderless') or False,
        'print_quality': print_setting.get('print_quality') or 'normal',
        'source': print_setting.get('source') or 'auto',
        'color_mode': print_setting.get('color_mode') or 'color',
        '2_sided': print_setting.get('2_sided') or 'none',
        'reverse_order': print_setting.get('reverse_order') or False,
        'copies': print_setting.get('copies') or 1,
        'collate': collate if collate is not None else True,
    }

    return settings


def validate_settings(settings: dict):  # noqa: C901
    """
    Validate all parts of a settings object.
    """
    extra_keys = set(settings.keys()) - {'job_name', 'print_mode', 'print_setting'}
    if extra_keys:
        raise PrintSettingError(f'Invalid settings keys {extra_keys}.')

    job_name = settings['job_name']
    if len(job_name) > 256:
        raise PrintSettingError(f'Job name is greater than 256 chars: {job_name}')

    print_mode = settings['print_mode']
    if print_mode not in VALID_PRINT_MODES:
        raise PrintSettingError(f'Invalid print mode {print_mode}')

    # print_setting is optional so we can exit early if its not present.
    print_setting = settings.get('print_setting')
    if not print_setting:
        return

    # Media Size
    media_size = print_setting['media_size']
    if media_size not in VALID_MEDIA_SIZES:
        raise PrintSettingError(f'Invalid paper size {media_size}')

    # media_type
    media_type = print_setting['media_type']
    if media_type not in VALID_MEDIA_TYPES:
        raise PrintSettingError(f'Invalid media type {media_size}')

    # borderless
    borderless = print_setting['borderless']
    if not isinstance(borderless, bool):
        raise PrintSettingError('borderless must be a bool')

    # print_quality
    print_quality = print_setting['print_quality']
    if print_quality not in VALID_PRINT_QUALITIES:
        raise PrintSettingError(f'Invalid print quality {print_quality}')

    # Paper source
    source = print_setting['source']
    if source not in VALID_PAPER_SOURCES:
        raise PrintSettingError(f'Invalid source {source}')

    # color_mode
    color_mode = print_setting['color_mode']
    if color_mode not in VALID_COLOR_MODES:
        raise PrintSettingError(f'Invalid color mode {color_mode}')

    # two_sided
    two_sided = print_setting['2_sided']
    if two_sided not in VALID_TWO_SIDE:
        raise PrintSettingError(f'Invalid 2-sided value {two_sided}')

    # reverse_order
    reverse_order = print_setting['reverse_order']
    if not isinstance(reverse_order, bool):
        raise PrintSettingError('Reverse order must be a bool')

    if print_setting['2_sided'] in ('long', 'short') and reverse_order:
        raise PrintSettingError('Can not use reverse order when using two-sided printing.')

    # copies
    copies = print_setting['copies']
    if copies < 1 or copies > 99:
        raise PrintSettingError(f'Invalid number of copies {copies}')

    # collate
    collate = print_setting['collate']
    if not isinstance(collate, bool):
        raise PrintSettingError('Collate must be a bool')

    if print_setting['2_sided'] in ('long', 'short') and not collate:
        raise PrintSettingError('Must collate when using two-sided printing.')


class PrintSettingError(ValueError):
    pass
