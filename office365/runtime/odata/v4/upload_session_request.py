import os

from office365.runtime.client_request import ClientRequest
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.types.event_handler import EventHandler


class UploadSessionRequest(ClientRequest):

    def __init__(self, context, file_object, chunk_size):
        """
        :param typing.IO file_object:
        """
        super(UploadSessionRequest, self).__init__(context)
        self._file_object = file_object
        self.chunk_uploaded = EventHandler(True)
        self._chunk_size = chunk_size
        self._range_start = 0
        self._range_end = 0

    def build_request(self, query):
        """
        :type query: office365.runtime.queries.upload_session.UploadSessionQuery
        """
        range_data = self._read_next()
        request = RequestOptions(query.upload_session_url)
        request.method = HttpMethod.Put
        request.set_header('Content-Length', str(len(range_data)))
        request.set_header('Content-Range',
                           'bytes {0}-{1}/{2}'.format(self._range_start, self._range_end - 1, self.file_size))
        request.set_header('Accept', '*/*')
        request.data = range_data
        return request

    def process_response(self, response):
        response.raise_for_status()
        if self.has_pending_read:
            self.add_query(self.current_query)

    def _read_next(self):
        self._range_start = self._file_object.tell()
        content = self._file_object.read(self._chunk_size)
        self._range_end = self._file_object.tell()
        return content

    @property
    def has_pending_read(self):
        return self._range_end < self.file_size

    @property
    def file_size(self):
        return os.fstat(self._file_object.fileno()).st_size

    @property
    def range_start(self):
        return self._range_start

    @property
    def range_end(self):
        return self._range_end
