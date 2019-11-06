from utils.esper import Processor
from components.renderable import Renderable
from components.camera import Camera
from bearlibterminal import terminal as blt
from systems.camera_processor import CameraProcessor


class RenderProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.fps = 4
        pass

    def process(self, *args, **kwargs):
        print(f'Render Processor {self.world.timer=}')
        blt.clear()
        for ent in self.world.get_processor(CameraProcessor).camera.view:
            rend = self.world.component_for_entity(ent, Renderable)
            blt.color(rend.color)
            blt.layer(rend.layer.value)
            blt.put(rend.x, rend.y, rend.char)
            blt.color('white')
            blt.layer(0)
            # print(f'{ent.name=}, {rend.x=}, {rend.y=}')

        self.render_camera_canvas()

        blt.refresh()

        self.world.timer += 1

    def render_camera_canvas(self):
        cam = self.world.get_processor(CameraProcessor).camera
        blt.layer(5)
        for x in range(0, cam.width + 1):
            blt.color('red')
            blt.put(x, 0, "#")
        for x in range(0, cam.width + 1):
            blt.color('blue')
            blt.put(x, cam.height, "#")
        for y in range(1, cam.height):
            blt.color('yellow')
            blt.put(0, y, '#')
        for y in range(1, cam.height):
            blt.color('cyan')
            blt.put(cam.width, y, '#')
