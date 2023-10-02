import settings
from entities.assets.direction import Direction
from entities.commands.command import Command
from entities.grid.position import Position, RobotPosition

# UPDATE COMMAND ONLY FOR ANDROID


class UpdateCommand(Command):
    def __init__(self, position: Position):
        super().__init__(0)
        self.position = position
        #print(self.position)

    def __str__(self):
        return str(self.position)

    __repr__ = __str__

    def process_one_tick(self, robot):
        if self.total_ticks == 0:
            return

        self.tick()

    def apply_on_pos(self, curr_pos):
        pass

    def convert_to_message(self):

        match self.position.direction:
            case Direction.TOP:
                direction = 'N'
            case Direction.BOTTOM:
                direction = 'S'
            case Direction.LEFT:
                direction = 'W'
            case Direction.RIGHT:
                direction = 'E'
        return f"U{self.position.x // settings.SCALING_FACTOR}-{self.position.y // settings.SCALING_FACTOR}-{direction}"
