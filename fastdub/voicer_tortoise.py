import logging
import os
from hashlib import md5
from pathlib import Path
from shutil import rmtree

from fastdub.audio import AudioSegment
from fastdub.voicer import UnknownVoice, _no_update_voice_anchor

SUPPORTED = False
try:
    import torchaudio
    from tortoise.api import TextToSpeech
    from tortoise.utils.audio import load_voice
    SUPPORTED = True
except ImportError:
    pass


class TortoiseVoicer:
    __slots__ = ('engine', 'cache_dir', '_update_voice_anchor', '_nul_file', '_current_voice', '_preset', '_voice_samples', '_conditioning_latents')

    def __init__(self, cache_dir: str = None, anchor: str = '!:', preset: str = 'fast'):
        if not SUPPORTED:
            raise ImportError("tortoise-tts is not installed. Please install it using: pip install \"FastDub[tortoise]\"")
        
        if anchor:
            def _update_voice_anchor(line: str) -> bool:
                if line.startswith(anchor):
                    self.set_voice(line.removeprefix(anchor))
                    return True
                return False
        else:
            _update_voice_anchor = _no_update_voice_anchor
        self._update_voice_anchor = _update_voice_anchor

        cache_dir = Path(__file__).parent / '_cached_texts' if cache_dir is None else Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        nul_file = cache_dir / 'nul.wav'
        if not nul_file.is_file():
            AudioSegment.silent(0).export(nul_file, 'wav')
        self.cache_dir = cache_dir
        self._nul_file = str(nul_file)

        logging.info("Initializing Tortoise-TTS engine... This may take a while and will load models into memory.")
        self.engine = TextToSpeech()
        self._preset = preset
        
        # Default voice state
        self._current_voice = 'random'
        self._voice_samples, self._conditioning_latents = load_voice('random')

    def cleanup(self):
        rmtree(self.cache_dir, ignore_errors=True)

    def set_voice(self, voice: str):
        voice_name = voice.strip()
        try:
            self._voice_samples, self._conditioning_latents = load_voice(voice_name)
            self._current_voice = voice_name
        except Exception as e:
            raise UnknownVoice(f"Could not load Tortoise voice '{voice_name}': {e}")

    def voice(self, text: str) -> str:
        text = text.strip()
        if not text:
            return self._nul_file

        if self._update_voice_anchor((lines := text.splitlines())[0]):
            text = '\n'.join(lines[1:])

        # MD5 cache incorporating tortoise specific parameters
        cached_file_str = f'''{self.cache_dir / md5(f"{text}_tortoise_{self._current_voice}_{self._preset}".encode()).hexdigest()}.wav'''
        if not os.path.isfile(cached_file_str):
            logging.info(f"Tortoise-TTS generating audio for: {text[:50]}...")
            gen = self.engine.tts_with_preset(
                text, 
                voice_samples=self._voice_samples, 
                conditioning_latents=self._conditioning_latents, 
                preset=self._preset
            )
            # gen is shape (1, channels, frames), save to 24000 sample rate
            torchaudio.save(cached_file_str, gen.squeeze(0).cpu(), 24000)
            
        return cached_file_str
