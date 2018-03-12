import numpy as np

from Detector import Detector
from MultiRotorConnector import MultiRotorConnector

class State():
    VEL_X    = None
    VEL_Y    = None
    VEL_Z    = None
    POS_X    = None
    POS_Y    = None
    WIDTH    = None
    HEIGHT   = None
    ALTITUDE = None
    pass

class Environment:
    def __init__(self):
        self._connector = MultiRotorConnector()
        self._detector  = Detector()

    def state_to_array(self, state):
        out = np.zeros((8,), dtype='float32')
        out[0] = state.VEL_X
        out[1] = state.VEL_Y
        out[2] = state.VEL_Z
        out[3] = state.POS_X
        out[4] = state.POS_Y
        out[5] = state.WIDTH
        out[6] = state.HEIGHT
        out[7] = state.ALTITUDE
        return out

    def update(self, state):
        velocity = self._connector.get_velocity()
        state.VEL_X = velocity.x_val
        state.VEL_Y = velocity.y_val
        state.VEL_Z = velocity.z_val

        position = self._connector.get_position()
        state.ALTITUDE = position.z_val

        frame        = self._connector.get_frame()
        output       = self._detector.detect(frame)
        if not output:
            return None

        state.POS_X  = output[0]
        state.POS_Y  = output[1]
        state.WIDTH  = output[2]
        state.HEIGHT = output[3]

        print "----State Values----"
        print "Velocity X:", state.VEL_X
        print "Velocity Y:", state.VEL_Y
        print "Velocity Z:", state.VEL_Z
        print "Altitude  :", state.ALTITUDE
        print "Position X:", state.POS_X
        print "Position Y:", state.POS_Y
        print "Width     :", state.WIDTH
        print "Height    :", state.HEIGHT

        return 1

    def reset(self):
        # TODO - Implement Reset Environment
        # Get the position of car and take the multirotor above it
        _state = State()
        flag = self.update(_state)
        if not flag:
            raise Exception('Unable to detect any Object')
        return self.state_to_array(_state)

    def step(self, action, duration=5):
        _state = State()
        self._connector.move_by_velocity(action, duration=duration)
        collision_info = self._connector.get_collision_info()
        flag = self.update(_state)
        if not flag:
            raise Exception('Unable to detect any Object')
        return self.state_to_array(_state), collision_info