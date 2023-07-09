import random

import pytest

from epson_connect.printer_settings import (
    PrintSettingError,
    merge_with_default_settings,
    validate_settings,
)

# Fix randomized job names for tests.
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
            'collate': False,
            'color_mode': 'mono',
            'copies': 45,
            'media_type': 'mt_hagaki',
            'print_quality': 'draft',
            'reverse_order': True,
            'source': 'rear',
        },
    }


def test_validate_settings():
    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'extra-key': None,
        })
    assert "Invalid settings keys {'extra-key'}." == str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': ''.join('a' for _ in range(300)),
        })
    assert 'Job name is greater than 256 chars' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'non-mode',
        })
    assert 'Invalid print mode' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': '1',
            },
        })
    assert 'Invalid paper size' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': '1',
            },
        })
    assert 'Invalid media type' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': 'False',
            },
        })
    assert 'borderless must be a bool' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'bad',
            },
        })
    assert 'Invalid print quality' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'up',
            },
        })
    assert 'Invalid source' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'rear',
                'color_mode': 'vibrant',
            },
        })
    assert 'Invalid color mode' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'rear',
                'color_mode': 'mono',
                '2_sided': 'both',
            },
        })
    assert 'Invalid 2-sided value' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'rear',
                'color_mode': 'mono',
                '2_sided': 'long',
                'reverse_order': 'yes',
            },
        })
    assert 'Reverse order must be a bool' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'rear',
                'color_mode': 'mono',
                '2_sided': 'long',
                'reverse_order': True,
            },
        })
    assert 'Can not use reverse order when using two-sided printing.' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'rear',
                'color_mode': 'mono',
                '2_sided': 'long',
                'reverse_order': False,
                'copies': 100,
            },
        })
    assert 'Invalid number of copies' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'rear',
                'color_mode': 'mono',
                '2_sided': 'long',
                'reverse_order': False,
                'copies': 45,
                'collate': 'yes',
            },
        })
    assert 'Collate must be a bool' in str(e.value)

    with pytest.raises(PrintSettingError) as e:
        validate_settings({
            'job_name': 'abc123',
            'print_mode': 'document',
            'print_setting': {
                'media_size': 'ms_a4',
                'media_type': 'mt_plainpaper',
                'borderless': False,
                'print_quality': 'high',
                'source': 'rear',
                'color_mode': 'mono',
                '2_sided': 'long',
                'reverse_order': False,
                'copies': 45,
                'collate': False,
            },
        })
    assert 'Must collate when using two-sided printing.' in str(e.value)

    # No errors.
    validate_settings({
        'job_name': 'abc123',
        'print_mode': 'document',
        'print_setting': {
            'media_size': 'ms_a4',
            'media_type': 'mt_plainpaper',
            'borderless': False,
            'print_quality': 'high',
            'source': 'rear',
            'color_mode': 'mono',
            '2_sided': 'long',
            'reverse_order': False,
            'copies': 45,
            'collate': True,
        },
    })
