from typing import Dict
import cv2
import numpy as np
import requests
import json
from supervision.detection.core import Detections
from supervision.draw.color import Color
from supervision.geometry.core import Point, Rect, Vector


class LineZone:
    """
    Count the number of objects that cross a line.
    """

    def __init__(self, start: Point, end: Point):
        """
        Initialize a LineCounter object.
        Attributes:
            start (Point): The starting point of the line.
            end (Point): The ending point of the line.
        """
        self.vector = Vector(start=start, end=end)
        self.tracker_state: Dict[str, bool] = {}
        self.in_count: int = 0
        self.out_count: int = 0
        self.current_cars: int = 100

    def calculate_center(anchors):
        x_sum = 0
        y_sum = 0
        num_points = len(anchors)

        for point in anchors:
            x_sum += point.x
            y_sum += point.y
        center_x = x_sum / num_points
        center_y = y_sum / num_points
        return Point(center_x, center_y)
   

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


    def trigger(self, detections: Detections):
        """
        Update the in_count and out_count for the center of detections that cross the line.
        Attributes:
            detections (Detections): The detections for which to update the counts.
        """
        for xyxy, confidence, class_id, tracker_id in detections:
            # handle detections with no tracker_id
            if tracker_id is None:
                continue
            # calculate the center point of the bbox
            x1, y1, x2, y2 = xyxy
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            center_point = Point(x=center_x, y=center_y)
            trigger = self.vector.is_in(point=center_point)

            # handle new detection
            if tracker_id not in self.tracker_state:
                self.tracker_state[tracker_id] = trigger
                continue

            # handle detection on the same side of the line
            if self.tracker_state.get(tracker_id) == trigger:
                continue

            self.tracker_state[tracker_id] = trigger

            if trigger:
                self.in_count += 1
                self.current_cars -= 1
            else:
                self.out_count += 1
                self.current_cars += 1

            print("Autos im Parkhaus: " + str(self.current_cars))
            self.send_put_request("HS_Coburg", "HS_Coburg",
                                          "Test123", self.current_cars)


class LineZoneAnnotator:
    def __init__(
        self,
        thickness: float = 2,
        color: Color = Color.red(),
        text_thickness: float = 2,
        text_color: Color = Color.black(),
        text_scale: float = 0.5,
        text_offset: float = 1.5,
        text_padding: int = 10,
    ):

        """
        Initialize the LineCounterAnnotator object with default values.
        Attributes:
            thickness (float): The thickness of the line that will be drawn.
            color (Color): The color of the line that will be drawn.
            text_thickness (float): The thickness of the text that will be drawn.
            text_color (Color): The color of the text that will be drawn.
            text_scale (float): The scale of the text that will be drawn.
            text_offset (float): The offset of the text that will be drawn.
            text_padding (int): The padding of the text that will be drawn.
        """
        self.thickness: float = thickness
        self.color: Color = color
        self.text_thickness: float = text_thickness
        self.text_color: Color = text_color
        self.text_scale: float = text_scale
        self.text_offset: float = text_offset
        self.text_padding: int = text_padding

    def annotate(self, frame: np.ndarray, line_counter: LineZone) -> np.ndarray:
        """
        Draws the line on the frame using the line_counter provided.
        Attributes:
            frame (np.ndarray): The image on which the line will be drawn.
            line_counter (LineCounter): The line counter that will be used to draw the line.
        Returns:
            np.ndarray: The image with the line drawn on it.
        """

        cv2.line(
            frame,
            line_counter.vector.start.as_xy_int_tuple(),
            line_counter.vector.end.as_xy_int_tuple(),
            self.color.as_bgr(),
            self.thickness,
            lineType=cv2.LINE_AA,
            shift=0,
        )

        cv2.circle(
            frame,
            line_counter.vector.start.as_xy_int_tuple(),
            radius=5,
            color=self.text_color.as_bgr(),
            thickness=-1,
            lineType=cv2.LINE_AA,
        )

        cv2.circle(
            frame,
            line_counter.vector.end.as_xy_int_tuple(),
            radius=5,
            color=self.text_color.as_bgr(),
            thickness=-1,
            lineType=cv2.LINE_AA,
        )

        in_text = f"in: {line_counter.out_count}"

        out_text = f"out: {line_counter.in_count}"

        (in_text_width, in_text_height), _ = cv2.getTextSize(
            out_text, cv2.FONT_HERSHEY_SIMPLEX, self.text_scale, self.text_thickness
        )

        (out_text_width, out_text_height), _ = cv2.getTextSize(
            in_text, cv2.FONT_HERSHEY_SIMPLEX, self.text_scale, self.text_thickness
        )

        in_text_x = int(
            (line_counter.vector.end.x + line_counter.vector.start.x - in_text_width)
            / 2
        )

        in_text_y = int(
            (line_counter.vector.end.y + line_counter.vector.start.y + in_text_height)
            / 2
            - self.text_offset * in_text_height
        )

        out_text_x = int(
            (line_counter.vector.end.x + line_counter.vector.start.x - out_text_width)
            / 2
        )

        out_text_y = int(
            (line_counter.vector.end.y + line_counter.vector.start.y + out_text_height)
            / 2
            + self.text_offset * out_text_height
        )

        in_text_background_rect = Rect(
            x=in_text_x,
            y=in_text_y - in_text_height,
            width=in_text_width,
            height=in_text_height,
        ).pad(padding=self.text_padding)

        out_text_background_rect = Rect(
            x=out_text_x,
            y=out_text_y - out_text_height,
            width=out_text_width,
            height=out_text_height,
        ).pad(padding=self.text_padding)

        cv2.rectangle(
            frame,
            in_text_background_rect.top_left.as_xy_int_tuple(),
            in_text_background_rect.bottom_right.as_xy_int_tuple(),
            self.color.as_bgr(),
            -1,
        )

        cv2.rectangle(
            frame,
            out_text_background_rect.top_left.as_xy_int_tuple(),
            out_text_background_rect.bottom_right.as_xy_int_tuple(),
            self.color.as_bgr(),
            -1,
        )

        cv2.putText(
            frame,
            out_text,
            (in_text_x, in_text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.text_scale,
            self.text_color.as_bgr(),
            self.text_thickness,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            in_text,
            (out_text_x, out_text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.text_scale,
            self.text_color.as_bgr(),
            self.text_thickness,
            cv2.LINE_AA,
        )
