"""
The meat and bones of the YoloV5Node
"""

__author__ = ''
__date__ = ''

import logging
from PIL import Image
from scenera.node.logger import configure_logger
import torch
import requests

logger = logging.getLogger(__name__)
logger = configure_logger(logger, debug=True)

class Model:
    def __init__(self):
        self.model = torch.hub.load(
            'yolov5',
            'custom',
            path='yolov5/models/yolov5s.pt',
            source='local',
            autoshape = True
            ) # offline model with local weight
        self.device = torch.device('cpu')
        self.model = self.model.to(self.device)
        self.model.eval()

    def run_object_detection(
        self,
        image_uri : str
    ):

        try:
            file = requests.get(image_uri, stream=True).raw
            img = Image.open(file)

            results = self.model(img)
            results_df = results.pandas().xyxy[0]
            #results.save()

            ## Get original image size
            img_size = img.size
            img_height = img_size[0]
            img_width = img_size[1]

            # Example output
            # detections = [[0.1,0.2,0.3,0.4,'person'],[0.2,0.3,0.4,0.5,'stop sign']]

            ## Extracting inference data
            detections = []
            for i in range(len(results_df)):
                ## Converting box in case resizing is needed
                x_min = results_df['xmin'][i] # unit in pixels, x-coordinate of upper left point
                y_min = results_df['ymin'][i] # unit in pixels, y-coordinate of upper left point
                x_max = results_df['xmax'][i] # unit in pixels, x-coordinate of bottom right point
                y_max = results_df['ymax'][i] # unit in pixels, y-coordinate of bottom right point

                box_width = x_max - x_min # unit in pixels
                box_height = y_max - y_min # unit in pixels

                ## Relative bounding box
                x_min_ratio = x_min / img_width # relative unit, x-coordinate of upper left point
                y_min_ratio = y_min / img_height # relative unit, y-coordinate of upper left point
                box_width_ratio = box_width / img_width # relative unit
                box_height_ratio = box_height / img_height # relative unit

                # x_center = x_min + box_width/2
                # y_center = y_min + box_height/2
                # x_center_ratio = x_center / img_width
                # y_center_ratio = y_center / img_height

                ## using pixel unit
                # if results_df['confidence'][i] > 0.5:
                #     detections.append([x_min, y_min, box_width, box_height, results_df['name'][i]])

                ## using relative unit
                if results_df['confidence'][i] > 0.5:
                    detections.append([x_min_ratio, y_min_ratio, box_width_ratio, box_height_ratio, results_df['name'][i]])

        except Exception as _e:
            logger.exception("Error:", _e)
            return {'ProcessingStatus': "Error",
                    'Error_Message': _e,
                    'Uri': image_uri}

        if detections:
            return {'ProcessingStatus': "Recognized",
                    'Detections': detections,
                    'Uri': image_uri}

        return {'ProcessingStatus': "Undetected",
                'Error_Message': "No objects detected",
                'Uri': image_uri}

def map_det_to_itemtype(detection):
    """
    Maps the output of the algorithm to the NICEItemType

    Parameters
    ----------
    detection : string, name of output class

    Returns
    -------
    * corresponding NICEItemType
    """
    assert isinstance(detection, str)
    dti_dict = {
        'person': 'Human',
        'bicycle': 'Vehicle',
        'car': 'Vehicle',
        'motorbike': 'Vehicle',
        'aeroplane': 'Vehicle',
        'bus': 'Vehicle',
        'train': 'Vehicle',
        'truck': 'Vehicle',
        'boat': 'Vehicle',
        'traffic light': 'Label',
        'fire hydrant': 'Label',
        'stop sign': 'Label',
        'parking meter': 'Label',
        'bench': 'Furniture',
        'bird': 'Animal',
        'cat': 'Animal',
        'dog': 'Animal',
        'horse': 'Animal',
        'sheep': 'Animal',
        'cow': 'Animal',
        'elephant': 'Animal',
        'bear': 'Animal',
        'zebra': 'Animal',
        'giraffe': 'Animal',
        'backpack': 'Bag',
        'umbrella': 'Accessory',
        'handbag': 'Bag',
        'tie': 'Accessory',
        'suitcase': 'Bag',
        'frisbee': 'Label',
        'skis': 'Label',
        'snowboard': 'Label',
        'sports ball': 'Label',
        'kite': 'Label',
        'baseball bat': 'Weapon',
        'baseball glove': 'Label',
        'skateboard': 'Accessory',
        'surfboard': 'Label',
        'tennis racket': 'Accessory',
        'bottle': 'Label',
        'wine glass': 'Label',
        'cup': 'Accessory',
        'fork': 'Label',
        'knife': 'Weapon',
        'spoon': 'Label',
        'bowl': 'Label',
        'banana': 'Label',
        'apple': 'Label',
        'sandwich': 'Label',
        'orange': 'Label',
        'broccoli': 'Label',
        'carrot': 'Label',
        'hot dog': 'Label',
        'pizza': 'Label',
        'donut': 'Label',
        'cake': 'Label',
        'chair': 'Furniture',
        'sofa': 'Furniture',
        'pottedplant': 'Label',
        'bed': 'Furniture',
        'diningtable': 'Furniture',
        'toilet': 'Label',
        'tvmonitor': 'Label',
        'laptop': 'Accessory',
        'mouse': 'Label',
        'remote': 'Label',
        'keyboard': 'Label',
        'cell phone': 'Label',
        'microwave': 'Label',
        'oven': 'Label',
        'toaster': 'Label',
        'sink': 'Label',
        'refrigerator': 'Label',
        'book': 'Accessory',
        'clock': 'Label',
        'vase': 'Label',
        'scissors': 'Label',
        'teddy bear': 'Label',
        'hair drier': 'Label',
        'toothbrush': 'Label'
        }
    try:
        return dti_dict[detection]
    except:
        logger.info("Could not find the object in the list!")
        return "Custom"
