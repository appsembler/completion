"""
Production plugin settings i.e., aws, for completion.
"""


def plugin_settings(settings):
    """
    Modify the provided settings object with settings specific to this plugin.
    """
    settings.COMPLETION_ENABLE_EVENTTRACKING = settings.ENV_TOKENS.get(
        'COMPLETION_ENABLE_EVENTTRACKING',
        settings.COMPLETION_ENABLE_EVENTTRACKING,
    )

    settings.COMPLETION_TRACKED_BLOCK_TYPE_BLACKLIST = set(settings.ENV_TOKENS.get(
        'COMPLETION_TRACKED_BLOCK_TYPE_BLACKLIST',
        settings.COMPLETION_TRACKED_BLOCK_TYPE_BLACKLIST,
    ))
