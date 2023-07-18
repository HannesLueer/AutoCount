import torch
import numpy as np
import cv2
#import pafy
from time import time


class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using Opencv2.
    """

    def __init__(self, url, out_file="Labeled_Video.avi"):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        self._URL = url
        self.model = self.load_model()
        self.classes = self.model.names
        self.out_file = out_file
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def getCompromisedVideo(self):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        """
        #play = pafy.new(self._URL).streams[-1]
        #assert play is not None
        cap = cv2.VideoCapture('HCPS Beispiel.mp4')
        # Rufen Sie die Breite und Höhe des ursprünglichen Videos ab

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Definieren Sie die gewünschte Breite und Höhe für das neue Video (360p)
        new_width = 852 
        new_height = 480
        #new_width = 1280
        #new_height = 720
        greyedVideoName = "greyVideo.mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(greyedVideoName, fourcc, fps, (new_width, new_height), isColor=False)

        while True:
            # Lesen Sie jedes Frame des ursprünglichen Videos
            ret, frame = cap.read()
            if not ret:
                break
            
            # Skalieren Sie das Frame auf die gewünschte Größe
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Konvertieren Sie das Frame in Graustufen
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

            # Schreiben Sie das transformierte Frame in den neuen VideoWriter
            out.write(gray_frame)

            # Zeigen Sie das transformierte Frame an
            cv2.imshow("Transformed Video", gray_frame)
            
            # Warten Sie entsprechend der gewünschten Framerate (10 FPS)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
             #   break
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        cap2 = cv2.VideoCapture(greyedVideoName)
     
        return cap2
        #return cv2.VideoCapture(play.url)

    def load_model(self):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if(self.class_to_label(labels[i]) == "car"):
                if row[4] >= 0.2:
                    x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                    bgr = (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                    cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame

    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        player = cv2.VideoCapture('HCPS Beispiel grau.mp4')
        #player = self.getCompromisedVideo()
        assert player.isOpened()
        x_shape = int(player.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter(self.out_file, four_cc, 20, (x_shape, y_shape))
        i = 0
        while True:
            i += 1
            start_time = time()
            ret, frame = player.read()
            if(i % 6 == 0):    
                #frame = cv2.resize(frame, (640, 360))
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                assert ret
                results = self.score_frame(frame)
                frame = self.plot_boxes(results, frame)
                end_time = time()
                fps = 1/np.round(end_time - start_time, 3)
                #print(f"Frames Per Second : {fps}")
                out.write(frame)

                cv2.imshow('video', frame)
                #cv2.imshow("Difference" , th)
                if cv2.waitKey(1) == 27:
                    break

# Create a new object and execute.
a = ObjectDetection("https://www.youtube.com/watch?v=dwD1n7N7EAg")
a()

cv2.destroyAllWindows()
