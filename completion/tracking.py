# -*- coding: utf-8 -*-
"""
Tracking and analytics events for block completions.
"""

from django.conf import settings

from eventtracking import tracker

from openedx.core.djangoapps.site_configuration import helpers


TRACKER_EVENT_NAME_FORMAT = u'edx.completion.{block_type}.{event_type}'


def _is_trackable_block_type(block_type):
    """
    Checks settings to see if we want to track this block type.
    We use a black list and assume tracking of all, otherwise.
    """
    return block_type not in helpers.get_value(
        'COMPLETION_TRACKED_BLOCK_TYPE_BLACKLIST',
        settings.COMPLETION_TRACKED_BLOCK_TYPE_BLACKLIST)


def track_completion_event(blockcompletion, completion_percent, is_new):
    """
    Logic for emitting or skipping a tracking event for a completed block.

    """
    if helpers.get_value(
        'COMPLETION_ENABLE_EVENTTRACKING', settings.COMPLETION_ENABLE_EVENTTRACKING) is not True:
        return

    if not _is_trackable_block_type(blockcompletion.block_type):
        return

    if is_new:
        if completion_percent == 1.0:
            event_type = 'completed'
        else:
            return
    elif not is_new:
        if completion_percent == 1.0:
            event_type = 'completed'
        # this code executes before new completion percentage saved to BlockCompletion
        elif blockcompletion.completion == 1.0 and completion_percent < 1:
            event_type = 'uncompleted'
        else:
            return

    event_name = TRACKER_EVENT_NAME_FORMAT.format(
        block_type=blockcompletion.block_type, 
        event_type=event_type
    )

    block_id = str(blockcompletion.block_key)
    course_id = str(blockcompletion.course_key)

    tracker.emit(event_name, {
        'label': '{} {} {}'.format(blockcompletion.block_type, block_id, event_type),
        'course_id': str(blockcompletion.course_key),
        'block_id': block_id,
        'block_type': blockcompletion.block_type,
    })
