ROI_WIDTH, ROI_HEIGHT = 300, 300


class ScreenRegion:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_absolute_region_of_interest(self) -> tuple[int, int, int, int]:
        """
        :return: (x1, y1, x2, y2) absolute on the screen
        """
        x1, y1, x2, y2 = self.get_relative_region_of_interest()
        return x1 + self.x, y1 + self.y, x2 + self.x, y2 + self.y

    def get_relative_region_of_interest(self) -> tuple[int, int, int, int]:
        """
        :return: (x1, y1, x2, y2) relative to the screen region of the player
        """
        # The ROI is <ROI_WIDTH>x<ROI_HEIGHT> px in the horizontal center and 100px from the bottom
        x1 = self.width // 2 - ROI_WIDTH // 2
        y1 = self.height - ROI_HEIGHT - 100
        x2 = x1 + ROI_WIDTH
        y2 = y1 + ROI_HEIGHT

        return x1, y1, x2, y2


def get_screen_regions(player_count, w, h) -> list[ScreenRegion]:
    """
    :param player_count: number of players from 1 to 4
    :param w: width of the whole screen
    :param h: height of the whole screen
    :return: ScreenRegion(x, y, width, height) of the frame specific to the player (player = [1, 2, 3, 4])
    """
    if player_count == 1:  # 1 player
        return [ScreenRegion(0, 0, w, h)]           # fullscreen
    elif player_count == 2:  # 2 players
        return [
            ScreenRegion(0, 0, w // 2, h),          # left
            ScreenRegion(w // 2, 0, w // 2, h)         # right
        ]
    elif player_count == 3:  # 3 players
        return [
            ScreenRegion(0, 0, w // 2, h // 2),     # top-left
            ScreenRegion(w // 2, 0, w // 2, h // 2),   # top-right
            ScreenRegion(0, h // 2, w // 2, h // 2)    # bottom-left
        ]
    else:  # 4 players
        return [
            ScreenRegion(0, 0, w // 2, h // 2),     # top-left
            ScreenRegion(w // 2, 0, w // 2, h // 2),   # top-right
            ScreenRegion(0, h // 2, w // 2, h // 2),   # bottom-left
            ScreenRegion(w // 2, h // 2, w // 2, h // 2)  # bottom-right
        ]
