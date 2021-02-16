# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io


def tts(text):
    import gtts
    _bytes = io.BytesIO()
    speech = gtts.gTTS(text)
    speech.write_to_fp(_bytes)
    _bytes.seek(0)
    return _bytes
