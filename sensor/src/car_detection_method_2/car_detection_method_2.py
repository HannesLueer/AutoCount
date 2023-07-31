import torch
import numpy as np
import cv2
import time
import requests
import json


class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a video using Opencv2.
    """

    def __init__(self, out_file="Labeled_Video.avi"):
        """
        Initializes the class with output file.
        :param out_file: A valid output file name.
        """
        self.model = self.load_model()
        self.classes = self.model.names
        self.out_file = out_file
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def load_model(self):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        model = torch.hub.load('ultralytics/yolov5',
                               'yolov5n', pretrained=True)
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
        labels, cord = results.xyxyn[0][:, -
                                        1].numpy(), results.xyxyn[0][:, :-1].numpy()

        # just return boxes with car label
        filtered_cords = []
        for label, coordinates in zip(labels, cord):
            if label == 2.0:  # label for car
                filtered_cords.append(coordinates)

        return [2.0]*len(filtered_cords), filtered_cords

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
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(
                    row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(
                    labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame

    def plot_centers(self, center_coords, frame):
        """
        Takes a frame and its center coordinates as input, and plots the center points on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """

        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for center_c in center_coords:
            x, y = center_c
            x_fs, y_fs = int(x*x_shape), int(y*y_shape)
            cv2.circle(frame, (x_fs, y_fs), 2, (0, 0, 255), 2)

        return frame

    def get_center_coords(self, rec_cords):
        center_coords = []
        for r_cord in rec_cords:
            x1, y1, x2, y2, _ = r_cord
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            center_coords.append([center_x, center_y])
        return center_coords

    def get_movement_vectors(self, curr_frame_points, prev_frame_points, prev_movement_vectors):
        # Initialize an empty dictionary to store the motion vectors for each point
        movement_vectors = {}

        # Initialize a dictionary to store the distances for each point in the current frame
        distances = {}

        # Initialize a list to store the already used points from the previous frame
        used_points = []

        # Calculate the distances for each point in the current frame to all points in the previous frame
        for curr_point in curr_frame_points:
            for prev_point in prev_frame_points:
                curr_point_np = np.array(curr_point)
                prev_point_np = np.array(prev_point)

                # Calculate the Euclidean distance between the points
                distance = np.linalg.norm(curr_point_np - prev_point_np)

                # Add the distance to the corresponding point in the dictionary
                if tuple(curr_point) in distances:
                    distances[tuple(curr_point)].append(
                        (tuple(prev_point), distance))
                else:
                    distances[tuple(curr_point)] = [
                        (tuple(prev_point), distance)]

        # Sort the distances for each point in the current frame in ascending order
        for curr_point, dist_list in distances.items():
            dist_list.sort(key=lambda x: x[1])

        # Determine the nearest point in the previous frame for each point in the current frame
        for curr_point, nearest_distance in distances.items():
            nearest_point, min_distance = nearest_distance[0]
            if nearest_point in used_points or min_distance > 0.2:
                continue
            else:
                used_points.append(nearest_point)

            # Calculate the motion vector between the current point and the nearest point
            movement_vector = np.array(curr_point) - nearest_point

            # Add or initialize the motion vector to the corresponding point in the dictionary
            if tuple(nearest_point) in prev_movement_vectors:
                movement_vectors[tuple(
                    curr_point)] = movement_vector + prev_movement_vectors[tuple(nearest_point)]
            else:
                movement_vectors[tuple(curr_point)] = movement_vector

        # get ending vectors
        unused_vectors = {}
        for p_point, m_vector in prev_movement_vectors.items():
            if tuple(p_point) not in used_points:
                unused_vectors[p_point] = m_vector

        return movement_vectors, unused_vectors

    def plot_movement_vectors(self, movement_vectors, frame):
        for point, vector in movement_vectors.items():
            end_point = tuple((np.array(point) - vector))

            scaled_end_point = tuple(
                (np.array(point) * frame.shape[1::-1]).astype(int))
            scaled_point = tuple(
                (np.array(end_point) * frame.shape[1::-1]).astype(int))

            cv2.arrowedLine(frame, scaled_point,
                            scaled_end_point, (255, 0, 0), 2)
        return frame

    def plot_ending_vectors(self, ending_vectors, frame):
        for e_v in ending_vectors:
            for point, vector in e_v.items():
                end_point = tuple((np.array(point) - vector))

                scaled_end_point = tuple(
                    (np.array(point) * frame.shape[1::-1]).astype(int))
                scaled_point = tuple(
                    (np.array(end_point) * frame.shape[1::-1]).astype(int))

                cv2.arrowedLine(frame, scaled_point,
                                scaled_end_point, (255, 200, 200), 2)
        return frame

    def determine_movement_direction(self, movement_vectors, threshold=0.1):
        car_change = 0
        for p_point, m_vector in movement_vectors.items():
            # Check if the y-component of the vector is positive (car movement downwards)
            if m_vector[1] > threshold:
                car_change += 1
            # Check if the y-component of the vector is negative (car movement upwards)
            elif m_vector[1] < -threshold:
                car_change += -1
        return car_change

    def send_put_request(self, site_id, username, password, current_cars):
        # URL for the PUT request
        url = f"http://localhost:5000/api/v1/c/{site_id}"

        # JSON-Payload
        payload = {
            "currentCars": current_cars
        }

        # HTTP Basic Auth
        auth = (username, password)

        # Set header with Content-Type for JSON
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # Send the PUT request
            response = requests.put(url, data=json.dumps(
                payload), headers=headers, auth=auth)

            # Check the response status code
            if response.status_code == 200:
                print("PUT Request sent successfully!")
            else:
                print(
                    f"Error sending the PUT request. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending the PUT request: {e}")

    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        player = cv2.VideoCapture('../../video_examples/10MinTest.mp4')
        assert player.isOpened()
        x_shape = int(player.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter(self.out_file, four_cc, 20, (x_shape, y_shape))
        i = 0
        prev_center_coords = []
        prev_movement_vectors = {}
        ending_vectors_all = []
        current_cars = 0
        times = []
        while True:
            i += 1
            start_time = time.time()
            ret, frame = player.read()

            if not ret:
                break

            if (i % 6 == 0):
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                results = self.score_frame(frame)
                frame = self.plot_boxes(results, frame)

                labels, cords = results
                center_coords = self.get_center_coords(cords)
                self.plot_centers(center_coords, frame)

                movement_vectors, ending_vectors = self.get_movement_vectors(
                    center_coords, prev_center_coords, prev_movement_vectors)
                self.plot_movement_vectors(movement_vectors, frame)

                ending_vectors_all.append(ending_vectors)
                self.plot_ending_vectors(ending_vectors_all, frame)

                car_change = self.determine_movement_direction(
                    ending_vectors, threshold=0.2)

                current_cars += car_change
                print(f"current_cars: {current_cars}")
                if (car_change != 0):
                    self.send_put_request("HS_Coburg", "HS_Coburg",
                                          "Test123", current_cars)

                prev_center_coords = center_coords
                prev_movement_vectors = movement_vectors

                out.write(frame)
                cv2.imshow('video', frame)

                if cv2.waitKey(1) == 27:
                    break

                end_time = time.time()
                times.append(end_time - start_time)

        with open('../../../demo/test_times/frame_times_method_2.txt', 'w') as file:
            for time_val in times:
                file.write(str(time_val) + '\n')


# Create a new object and execute.
a = ObjectDetection()
a()

cv2.destroyAllWindows()
