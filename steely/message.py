# TODO(iandioch): Migrate to python3.7 so we can annotate this with @dataclass
class SteelyMessage:
    """Class containing information about a single activity in a single channel.
    Usually means a message with text was sent, but also could have been an
    image sent (with no associated text message), etc."""

    author_id: str
    thread_id: str
    thread_type: str
    text: str
    # TODO(iandioch): Add image_id.
