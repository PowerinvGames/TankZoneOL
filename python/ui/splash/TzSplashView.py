import arcade
from arcade.types import RGB

from python.ui.TzAbstractView import TzAbstractView
from python.util.ConfigureUtil import ConfigureUtil


class TzSplashView(TzAbstractView):
    def __init__(self):
        super().__init__()
        self.bg_color: RGB = ConfigureUtil.get_config("view.splash.background")
        self.texture_color: RGB = ConfigureUtil.get_config("view.splash.texture")

    def on_draw(self) -> bool | None:
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window.width, self.window.height, self.bg_color)
        arcade.draw_lbwh_rectangle_outline(20, 20, self.window.width - 40, self.window.height - 40, self.texture_color)
