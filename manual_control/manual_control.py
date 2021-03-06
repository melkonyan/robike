import curses
import rospy
from std_msgs import Int32


class BikeProxy:
    def __init__(self, control_topic_name):
        self._steering_direction = 0
        self._speed = 0
        rospy.init_node("manual_input_node")
        self._pub = rospy.Publisher(control_topic_name, Int32, queue_size=10)

    def turn_left(self):
        self._steering_direction -= 100
        self._pub.publish(self._steering_direction)

    def turn_right(self):
        self._steering_direction += 100
        self._pub.publish(self._steering_direction)

    def slow_down(self):
        self._speed -= 10

    def speed_up(self):
        self._speed += 10

    def log_state(self):
        with open("out", "a") as file:
            file.write(str(self) + '\n')

    def __repr__(self):
        return "Bike: {speed: %d, steering direction: %d}" % \
               (self._speed, self._steering_direction)


def map_action(key, bike):
    if key == "KEY_LEFT":
        bike.turn_left()
    if key == "KEY_RIGHT":
        bike.turn_right()
    if key == "KEY_UP":
        bike.speed_up()
    if key == "KEY_DOWN":
        bike.slow_down()
    bike.log_state()


def input_loop(win):
    bike = BikeProxy(control_topic_name="control")
    win.nodelay(True)
    win.clear()
    win.addstr("Detected key:")
    while 1:
        try:
            key = win.getkey()
            win.clear()
            win.addstr("Detected key:")
            win.addstr(str(key))
            map_action(str(key), bike)
            if key == os.linesep:
                break
        except Exception:
            pass


if __name__ == '__main__':
    curses.wrapper(input_loop)
