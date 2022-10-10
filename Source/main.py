"""
An example of a YoloV5 Node using the Scenera Node SDK
"""

__author__ = 'Taekyu Ryu'
__date__ = ''

import logging
import ssl
from scenera.node import SceneMark
from scenera.node.logger import configure_logger
from object_detection import Model, map_det_to_itemtype
from flask import Flask, request
from flask_cors import CORS
from os import getenv

# pylint: disable = protecrted-access
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
CORS(app)

NODE_ID = getenv('NODE_ID', "yolov5node").lower()
FLASK_RUN_HOST = getenv("FLASK_RUN_HOST", "127.0.0.1")
FLASK_RUN_PORT = getenv("FLASK_RUN_PORT", "2222")

model = Model()

logger = logging.getLogger(__name__)
logger = configure_logger(logger, debug=True)

## The Node ID assigned by the Developer Portal is used as a URI
@app.route(f'/{NODE_ID}/1.0', methods = ['POST'])
def obj_detect_node_endpoint(test = False, load_test = False):
    """
    A Flask implementation of YoloV5 using the Scenera Node SDK

    Parameters
    ----------
    request : incoming request
        The incoming request including a SceneMark and a NodeSequencerHeader

    Returns
    -------
        Returns a SceneMark to the Data Pipeline's Node Sequencer - using the return_scenemark_to_ns
        method

    """

    ## This first thing we do is load the request into the SceneMark object,
    ## and load the information from the Developer Portal
    scenemark = SceneMark(
        request = request,
        node_id = NODE_ID
        )

    ## For testing purposes, you can log what is coming in.
    # scenemark.save_request("SM", name = "scenemark_received")
    # scenemark.save_request("NSH", name= "ns_info")

    results = [model.run_object_detection(uri) for uri in scenemark.targets]
    
    detected_objects = []
    for result in results:
        if result['ProcessingStatus'] != "Recognized":
            logger.exception("Error:", result['Error_Message'])
            scenemark.add_analysis_list_item(
                event_type="ItemPresence",
                processing_status = result['ProcessingStatus'],
                error_message = f"{result['Error_Message']}, processing {scenemark.get_id_from_uri(result['Uri'])}"
            )

        else:
            ## We add detected objects for each object that we find within the image
            for detection in result['Detections']:
                logger.info(detection)

                bounding_box = scenemark.generate_bounding_box(
                    detection[0],
                    detection[1],
                    detection[2],
                    detection[3]
                    )

                detected_objects.append(
                    scenemark.generate_detected_object_item(
                    nice_item_type = map_det_to_itemtype(detection[4]),
                    custom_item_type = detection[4],
                    item_id = "",
                    item_type_count = 1,
                    related_scenedata_id = scenemark.get_id_from_uri(result['Uri']),
                    bounding_box = bounding_box
                    )
                )

    if detected_objects:
        ## When we have the detected objects, we log them in the top level of the analysis list
        scenemark.add_analysis_list_item(
            processing_status = 'Detected',
            event_type = 'ItemPresence',
            total_item_count = len(result['Detections']),
            detected_objects = detected_objects,
            )

    ## For testing purposes we save the outgoing SceneMark, such that we can
    ## inspect it in case any errors occur
    # scenemark.save_request("SM", "scenemark_to_be_sent")

    ## We automatically return the SceneMark back to the NodeSequencer
    scenemark.return_scenemark_to_ns(test, load_test)
    return "Success"

@app.route(f'/{NODE_ID}/1.0/test', methods=['POST'])
def test_endpoint():
    logger.info("Received a request on the test endpoint")
    """
    This endpoint returns the SceneMark back to the sender, rather than the NodeSequencer
    for example for testing through Postman
    """
    return obj_detect_node_endpoint(test = True)

@app.route(f'/{NODE_ID}/1.0/loadtest', methods = ['POST'])
def load_test_endpoint():
    logger.info("Received a request on the load test endpoint.")
    """
    This endpoint returns just 200 OK, so the Load Test can shoot activation
    at the Node without the node having to send it somewhere else.
    """
    return obj_detect_node_endpoint(load_test = True)

## Use this to check whether the Node is live
@app.route(f'/{NODE_ID}/health')
def health_endpoint():
    return {}, 200

if __name__ == "__main__":
    print(f"\nHi I'm an AI node and my main endpoint is http://{FLASK_RUN_HOST}:{FLASK_RUN_PORT}/{NODE_ID}/1.0\n")
    print("and my name is", NODE_ID,'\n')
    app.run(
        host=FLASK_RUN_HOST,
        port=FLASK_RUN_PORT
        )
