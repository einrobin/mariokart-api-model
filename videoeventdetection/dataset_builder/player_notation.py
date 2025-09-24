import re

from screen_regions import get_screen_regions, ScreenRegion


class PlayerNotation(object):

    def __init__(self, player_count: int, player_ids: list[int]):
        self.player_count = player_count
        self.player_ids = player_ids

    def get_screen_regions(self, frame_width: int, frame_height: int) -> list[ScreenRegion]:
        regions = get_screen_regions(self.player_count, frame_width, frame_height)
        return [regions[pid - 1] for pid in self.player_ids]


def parse_player_notation(raw: str) -> PlayerNotation:
    """
    The format for the player notation looks like this: "<player_count>-p<player_id>" (e.g. 1-p1, 4-p2, etc.)

    Instead of <player_id> a literal 'a' may also be inserted to include all players

    :param raw: the player notation as a string representation
    :return: the parsed player notation
    """

    player_count = int(raw[0])
    if raw.endswith("pa"):
        return PlayerNotation(player_count, list(range(1, player_count + 1)))
    else:
        return PlayerNotation(player_count, [int(raw[-1])])


def extract_player_notation(label: str) -> tuple[PlayerNotation, str]:
    """
    Extracts the player notation from the label such as '1-p1', '2-p2', '3-p3', '4-p4'.
    The player notation can only be parsed when it is at the end of the label.
    Example: 'event-hit4-p2' -> '4-p2'

    :param label The raw event label such as 'event-hit4-p2'
    :return The parsed player notation and the label with the player notation removed (e.g. 'event-hit')
    :raises ValueError when the label doesn't contain a valid player notation
    """
    match = re.search(r'([1234]-p[1-4a])$', label)
    if not match:
        raise ValueError(f"No player notation found in: {label}")
    notation = match.group(1)
    parsed_notation = parse_player_notation(notation)

    return parsed_notation, label[: -len(notation)]
