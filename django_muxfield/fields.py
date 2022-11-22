"""
Code twith inspiration from https://github.com/dvl/django-videofield/blob/master/videofield/fields.py

Copyright 2022 Alexander Forselius <drsounds@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Footer

"""

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open('/dev/null', 'w')


from django import forms
from django.core import checks
from django.db import models
from django.conf import settings
import time
import mux_python
from mux_python.rest import NotFoundException

from django.db import models


# Authentication Setup
configuration = mux_python.Configuration()
configuration.username = settings.MUX_TOKEN_ID
configuration.password = settings.MUX_TOKEN_SECRET


assets_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))
playback_ids_api = mux_python.PlaybackIDApi(mux_python.ApiClient(configuration))

uploads_api = mux_python.DirectUploadsApi(mux_python.ApiClient(configuration))


class MuxField(models.URLField):
    widget = MuxInput
    default_error_messages = {
        'invalid_video': 'Upload a valid video. The file you uploaded was either not a video or a corrupted video.'
    }

    def to_python(self, data):
        f = super(MuxField, self).to_python(data)

        if f is None:
            return None

        if hasattr(data, 'temporary_file_path'):
            create_asset_request = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
            create_upload_request = mux_python.CreateUploadRequest(timeout=3600, new_asset_settings=create_asset_request, cors_origin="philcluff.co.uk")
            create_upload_response = uploads_api.create_direct_upload(create_upload_request)
