# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import wikipedia
import gtts


def tts(text):
    _bytes = io.BytesIO()
    speech = gtts.gTTS(text)
    speech.write_to_fp(_bytes)
    _bytes.seek(0)
    return _bytes


def wikipedia_exec(page: str):
    page = page.replace("joe biden n", "joe biden")
    wikipedia.set_lang("en")
    result = wikipedia.search(f"{page}")
    return [result.url, result.title, wikipedia.summary(f"{page}", sentences=2)]
