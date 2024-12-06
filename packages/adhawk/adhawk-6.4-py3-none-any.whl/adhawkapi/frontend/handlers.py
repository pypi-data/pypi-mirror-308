'''Contains handlers for frontend requests and responses'''

import collections
import logging
import threading
import queue

import numpy as np

import adhawkapi

from .decoders import decode
from .encoders import encode

try:
    from .. import internal
except ImportError:
    internal = None


class ResponseEvent:
    '''Response class for handling sync responses'''

    def __init__(self):
        self._event = threading.Event()
        self._response = None

    @property
    def response(self):
        '''Get the response'''
        return self._response

    def set(self, *response):
        '''Set the response and wake up the waiting thread'''
        self._response = response
        self._event.set()

    def wait(self, timeout=None):
        '''Wait for the response'''
        return self._event.wait(timeout)


class PacketHandler:
    '''Class that wraps the comm layer and handles encoding and decoding requests and responses
    '''

    _ET_TYPE_MAPPINGS = {
        adhawkapi.EyeTrackingStreamTypes.GAZE: adhawkapi.PacketType.GAZE,
        adhawkapi.EyeTrackingStreamTypes.PER_EYE_GAZE: adhawkapi.PacketType.PER_EYE_GAZE,
        adhawkapi.EyeTrackingStreamTypes.PUPIL_POSITION: adhawkapi.PacketType.PUPIL_POSITION,
        adhawkapi.EyeTrackingStreamTypes.PUPIL_DIAMETER: adhawkapi.PacketType.PUPIL_DIAMETER,
        adhawkapi.EyeTrackingStreamTypes.GAZE_IN_IMAGE: adhawkapi.PacketType.GAZE_IN_IMAGE,
        adhawkapi.EyeTrackingStreamTypes.GAZE_IN_SCREEN: adhawkapi.PacketType.GAZE_IN_SCREEN,
    }

    _OLD_ET_MAPPINGS = {v: k for k, v in _ET_TYPE_MAPPINGS.items()}

    _FEATURE_TYPE_MAPPINGS = {
        adhawkapi.FeatureStreamTypes.GLINT: adhawkapi.PacketType.GLINT,
        adhawkapi.FeatureStreamTypes.PUPIL_ELLIPSE: adhawkapi.PacketType.PUPIL_ELLIPSE,
    }

    _OLD_FEATURE_MAPPINGS = {v: k for k, v in _FEATURE_TYPE_MAPPINGS.items()}

    def __init__(self, eye_mask):
        self._logger = logging.getLogger(__name__)
        self._request_queue = queue.Queue()
        self._pending_requests = collections.deque()
        self._registered_handlers = collections.defaultdict(list)
        self._com = None
        self._request_thread = None
        self._eye_mask = eye_mask

    def set_eye_mask(self, eye_mask):
        '''Set the current eye mask'''
        self._eye_mask = eye_mask

    def start(self, com):
        '''Start communication with AdHawk service'''
        self._com = com
        self._request_thread = threading.Thread(target=self._request_loop)
        self._request_thread.start()

    def shutdown(self):
        '''Shutdown the packet handler'''
        if self._request_thread:
            self._request_queue.put(None)
            self._request_thread.join()
            self._request_thread = None
        self._com = None

    def request(self, packet_type, *args, callback=None, **kwargs):
        '''Send a request to backend given a packet type and the arguments'''

        self._logger.debug(f'[tx] {repr(packet_type)}: {args}')
        # setup sync or async callbacks
        if callback is None:
            event = ResponseEvent()
            response_cb = event.set
        else:
            response_cb = callback

        # encode and send the message
        message = encode(packet_type, *args, *kwargs)
        self._request_queue.put((message, response_cb))

        # wait on response if required
        if callback:
            return None

        if event.wait(adhawkapi.REQUEST_TIMEOUT + 1):
            response = event.response
            if response[0] != adhawkapi.AckCodes.SUCCESS:
                raise adhawkapi.APIRequestError(response[0])
            return response
        raise adhawkapi.APIRequestError(adhawkapi.AckCodes.REQUEST_TIMEOUT)

    def register_stream_handler(self, packet_type, handler):
        '''Add a listener for a particular packet type'''
        if not packet_type.is_stream():
            # Ensure we only register or unregister stream packets
            # All other packets are automatically registered through
            # the api callback parameter
            return
        self.register_handler(packet_type, handler)

    def register_handler(self, packet_type, handler):
        '''Add a listener for a particular packet type'''
        if packet_type in self._OLD_ET_MAPPINGS:
            self._logger.warning(f'Deprecated stream type {packet_type}, use et stream handler')
        if packet_type in self._OLD_FEATURE_MAPPINGS:
            self._logger.warning(f'Deprecated stream type {packet_type}, use feature stream handler')

        assert handler
        self._registered_handlers[packet_type].append(handler)

    def unregister_stream_handler(self, packet_type, handler):
        '''Remove a listener for a particular packet type'''
        try:
            self._registered_handlers[packet_type].remove(handler)
        except ValueError:
            pass

    def _handle_et_data(self, et_data: adhawkapi.EyeTrackingStreamData):  # pylint: disable=too-many-branches
        ''' backwards compatibility for old streams '''
        # gaze
        if et_data.gaze is not None:
            if np.all(np.isfinite(et_data.gaze)):
                handlers = self._registered_handlers[adhawkapi.PacketType.GAZE]
                if handlers:
                    for handler in handlers:
                        handler(et_data.timestamp, *et_data.gaze)
        if et_data.per_eye_gaze is not None:
            if np.any(np.isfinite(et_data.per_eye_gaze)):
                handlers = self._registered_handlers[adhawkapi.PacketType.PER_EYE_GAZE]
                if handlers:
                    for handler in handlers:
                        handler(et_data.timestamp, *et_data.per_eye_gaze)
        if et_data.pupil_pos is not None:
            if np.any(np.isfinite(et_data.pupil_pos)):
                handlers = self._registered_handlers[adhawkapi.PacketType.PUPIL_POSITION]
                if handlers:
                    for handler in handlers:
                        handler(et_data.timestamp, *et_data.pupil_pos)
        if et_data.pupil_diameter is not None:
            if np.any(np.isfinite(et_data.pupil_diameter)):
                handlers = self._registered_handlers[adhawkapi.PacketType.PUPIL_DIAMETER]
                if handlers:
                    for handler in handlers:
                        handler(et_data.timestamp, *et_data.pupil_diameter)
        if et_data.gaze_in_image is not None:
            if np.all(np.isfinite(et_data.gaze_in_image)):
                handlers = self._registered_handlers[adhawkapi.PacketType.GAZE_IN_IMAGE]
                if handlers:
                    for handler in handlers:
                        handler(et_data.timestamp, *et_data.gaze_in_image)
        if et_data.gaze_in_screen is not None:
            if np.all(np.isfinite(et_data.gaze_in_screen)):
                handlers = self._registered_handlers[adhawkapi.PacketType.GAZE_IN_SCREEN]
                if handlers:
                    for handler in handlers:
                        handler(et_data.timestamp, *et_data.gaze_in_screen)

    def handle_packet(self, packet_type_int, data):  # pylint: disable=too-many-branches
        '''Determines the packet type and decodes it'''
        try:
            try:
                packet_type = adhawkapi.PacketType(packet_type_int)
            except ValueError:
                if internal is None:
                    raise
                packet_type = internal.PacketType(packet_type_int)
        except ValueError:
            self._logger.warning(f'Unrecognized packet: {hex(packet_type_int)}')
            return

        decoded = decode(packet_type, data, self._eye_mask)
        if decoded is None:
            return

        if packet_type == adhawkapi.PacketType.EYETRACKING_STREAM:
            self._handle_et_data(decoded)
            decoded = [decoded]
        if packet_type == adhawkapi.PacketType.FEATURE_STREAM:  # pylint: disable=too-many-nested-blocks
            decoded = [decoded]

        # handle udp comm packets and any registered stream handlers first
        handlers = self._registered_handlers[packet_type]
        if handlers:
            for handler in handlers:
                handler(*decoded)
            return

        # if no handler for udp comm packets, return without warning
        if packet_type in (adhawkapi.PacketType.UDP_CONN, adhawkapi.PacketType.END_UDP_CONN):
            return

        if not packet_type.is_stream():
            # Checking pending requests
            self._logger.debug(f'[rx] {repr(packet_type)} {decoded}')
            try:
                handler = self._pending_requests.popleft()
            except IndexError:
                self._logger.warning(f'Received unexpected packet: {repr(packet_type)}')
            else:
                handler(*decoded)

    def _request_loop(self):
        '''Main loop for sending requests'''
        while True:
            request = self._request_queue.get()
            if request is None:
                break

            message, callback = request
            self._pending_requests.append(callback)
            self._com.send(message)
