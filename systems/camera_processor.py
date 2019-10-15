import utils.esper as esper
from components.camera import Camera
from components.position import Position
from components.renderable import Renderable
from components.joystick import Joystick
from utils.decorators import benchmark


class CameraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.camera = None

    def get_camera(self):
        for ent, cam in self.world.get_component(Camera):
            self.camera = cam

    @benchmark
    def process(self):
        for ent, (joyst, pos) in self.world.get_components(Joystick, Position):
            self.move_camera(pos.x, pos.y)

        for ent, (rend, pos) in self.world.get_components(Renderable, Position):
            rend.x, rend.y = self.to_camera_coordinates(pos.x, pos.y)

        self.entities_in_camera_view()

    def move_camera(self, x, y):
        # Двигаем камеру к заданным координатам
        self.camera.x = int(x - self.camera.width / 2)
        self.camera.y = int(y - self.camera.height / 2)

    def to_camera_coordinates(self, x, y):
        # Конвертируем координаты на карте в координаты на экране
        return x - self.camera.x, y - self.camera.y

    def to_map_coordinates(self, x, y):
        # Конвертируем координаты на экране в координаты на карте
        return x + self.camera.x, y + self.camera.y

    def entities_in_camera_view(self):
        self.camera.view = set()
        for ent, rend in self.world.get_component(Renderable):
            if rend.x in range(self.camera.width - 1) and rend.y in range(self.camera.height):
                self.camera.view.add(ent)
