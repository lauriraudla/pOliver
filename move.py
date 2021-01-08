from datetime import datetime
import omni_movement
from threading import Thread
state = 0

class move:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self, info=None):
        self.info = info
        self.stopped = False

    def start(self):
        # self.info = (0, 0)
        Thread(target=self.movement(), args=()).start()
        return self

    def movement(self):
        while not self.stopped:
            try:
                print(self.info)
                x = self.info[0]
                y = self.info[1]
                if x < 580:
                    print("right go brrrrrrrrrr")
                    # ser.write(right.encode())
                    omni_movement.turnRight()
                                    # right
                elif x > 700:
                    print("left go brrrrrrrrrr")
                    # ser.write(left.encode())
                    omni_movement.turnLeft()
                    # left
                else:
                    # print("else")
                    try:
                        # dist = cap.getDistance(int(pt[0][0]), int(pt[0][1]))
                        # print(dist)
                        if y < 380:
                            # omni_movement.omni_move(40, -90)
                            omni_movement.stop()
                        else:
                            omni_movement.stop()

                    except:
                        print("puutsad")
                        pass
                    # #ser.write(stop.encode())

            except:
                print("spin go brrrrrrrrr")
                omni_movement.turnFast()
                # suurem pööre

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurrences / elapsed_time if elapsed_time > 0 else 0

    def stop(self):
        self.stopped = True
