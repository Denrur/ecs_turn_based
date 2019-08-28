from bearlibterminal import terminal as blt


class Joystick:
    def __init__(self):
        self.action = None

    def handle_player_turn_keys(self, key):
        # r = blt.TK_KEY_RELEASED
        if key == blt.TK_UP or key == blt.TK_W:
            self.action = {'move': (0, -1)}
            return {'move': (0, -1)}
        elif key == blt.TK_DOWN or key == blt.TK_X:
            self.action = {'move': (0, 1)}
            return {'move': (0, 1)}
        elif key == blt.TK_LEFT or key == blt.TK_A:
            self.action = {'move': (-1, 0)}
            return {'move': (-1, 0)}
        elif key == blt.TK_RIGHT or key == blt.TK_D:
            self.action = {'move': (1, 0)}
            return {'move': (1, 0)}
        elif key == blt.TK_Q:
            self.action = {'move': (-1, -1)}
            return {'move': (-1, -1)}
        elif key == blt.TK_E:
            self.action = {'move': (1, -1)}
            return {'move': (1, -1)}
        elif key == blt.TK_Z:
            self.action = {'move': (-1, 1)}
            return {'move': (-1, 1)}
        elif key == blt.TK_C:
            self.action = {'move': (-1, 1)}
            return {'move': (1, 1)}

        if key == blt.TK_G:
            self.action = {'pickup': True}
            return {'pickup': True}

        if key == blt.TK_MOUSE_SCROLL:
            return {'scroll': True}
        # elif key == blt.TK_O:
        #     return{'scroll_up': True}
        # elif key == blt.TK_L:
        #     return{'scroll_down': True}

        elif key == blt.TK_I:
            self.action = {'show_inventory': True}
            return {'show_inventory': True}

        elif key == blt.TK_O:
            self.action = {'drop_inventory': True}
            return {'drop_inventory': True}

        elif key == blt.TK_S:
            self.action = {'pass': True}
            return {'pass': True}

        if key == blt.TK_RETURN and blt.TK_ALT:
            return {'fullscreen': True}
        elif key == blt.TK_ESCAPE:
            return {'exit': True}

        if key == 133:
            return {'mouse': True}
        return {}