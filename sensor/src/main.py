import numpy as np
import cv2
import datetime
import time
import os

# VIDEO_WIDTH = 1920
# VIDEO_HEIGHT = 1080

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

# VIDEO_WIDTH = 1640
# VIDEO_HEIGHT = 1232
# FPS = 40

# VIDEO_WIDTH = 820
# VIDEO_HEIGHT = 616

# VIDEO_WIDTH = 3280
# VIDEO_HEIGHT = 2464

FPS = 20


def main():
    def exit():
        # Release everything if job is finished
        cap.release()
        out.release()

    # create output folder
    folder_name = "out"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # create capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    act_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    act_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    act_fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # fourcc = cv2.VideoWriter_fourcc(*'H264')
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    filename = f'{folder_name}/output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.avi'
    out = cv2.VideoWriter(filename, fourcc, act_fps, (act_width, act_height))

    last_second = None
    print(f'The recording is now started and saved as {filename}')
    print(f'\tResolution: {act_width}×{act_height}')
    print(f'\tFPS: {act_fps:.2f}')
    print("Press ctrl + c to quit")

    try:
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.flip(frame, -1)  # flipping around both axes

                # write the flipped frame
                out.write(frame)

                # print time
                current_second = int(time.time())
                if current_second != last_second:
                    last_second = current_second
                    if current_second % 10 == 0:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            else:
                print(f'ret={ret}')
                break

        exit()

    except KeyboardInterrupt:
        exit()
        print("\nExiting...")


if __name__ == "__main__":
    main()
