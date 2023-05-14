import numpy as np
import cv2
import datetime
import time
import os


def main():
    def exit():
        # Release everything if job is finished
        cap.release()
        out.release()

    # create output folder
    folder_name = "out"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = f'{folder_name}/output_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.avi'
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    last_second = None
    print(f'The recording is now started and saved as {filename}')
    print("Press ctrl + c to quit")

    try:
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.flip(frame, 0)

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
