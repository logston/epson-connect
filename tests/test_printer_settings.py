import random

from epson_connect.printer_settings import merge_with_default_settings

random.seed(0)


def test_merge_with_default_settings_none():
    settings = merge_with_default_settings()
    assert settings == {
        'job_name': 'job-yWAcqGFz',
        'print_mode': 'document',
    }


def test_merge_with_default_settings_basic_overrides():
    settings = merge_with_default_settings({
        'job_name': 'my-job',
        'print_mode': 'photo',
    })
    assert settings == {
        'job_name': 'my-job',
        'print_mode': 'photo',
    }


def test_merge_with_default_settings_with_single_print_setting():
    settings = merge_with_default_settings({
        'print_setting': {
            'media_size': 'ms_tabloid',
        },
    })
    assert settings == {
        'job_name': 'job-YtEwLnGi',
        'print_mode': 'document',
        'print_setting': {
            'media_size': 'ms_tabloid',
            '2_sided': 'none',
            'borderless': False,
            'collate': True,
            'color_mode': 'color',
            'copies': 1,
            'media_type': 'mt_plainpaper',
            'print_quality': 'normal',
            'reverse_order': False,
            'source': 'auto'
        },
    }


def test_merge_with_default_settings_with_full_overrides():
    settings = merge_with_default_settings({
        'job_name': 'job-123',
        'print_mode': 'photo',
        'print_setting': {
            'media_size': 'ms_postcard',
            '2_sided': 'long',
            'borderless': True,
            'collate': False,
            'color_mode': 'mono',
            'copies': 45,
            'media_type': 'mt_hagaki',
            'print_quality': 'draft',
            'reverse_order': True,
            'source': 'rear',
        },
    })
    assert settings == {
        'job_name': 'job-123',
        'print_mode': 'photo',
        'print_setting': {
            'media_size': 'ms_postcard',
            '2_sided': 'long',
            'borderless': True,
            'collate': True,  # Forced true by 2-sided printing.
            'color_mode': 'mono',
            'copies': 45,
            'media_type': 'mt_hagaki',
            'print_quality': 'draft',
            'reverse_order': False, # Forced false by 2-sided printing.
            'source': 'rear',
        },
    }


def test_merge_with_default_settings_with_full_overrides_non_two_sided():
    settings = merge_with_default_settings({
        'job_name': 'job-123',
        'print_mode': 'photo',
        'print_setting': {
            'media_size': 'ms_postcard',
            '2_sided': 'none',
            'borderless': True,
            'collate': False,
            'color_mode': 'mono',
            'copies': 45,
            'media_type': 'mt_hagaki',
            'print_quality': 'draft',
            'reverse_order': True,
            'source': 'rear',
        },
    })
    assert settings == {
        'job_name': 'job-123',
        'print_mode': 'photo',
        'print_setting': {
            'media_size': 'ms_postcard',
            '2_sided': 'none',
            'borderless': True,
            'collate': False,
            'color_mode': 'mono',
            'copies': 45,
            'media_type': 'mt_hagaki',
            'print_quality': 'draft',
            'reverse_order': True,
            'source': 'rear',
        },
    }
