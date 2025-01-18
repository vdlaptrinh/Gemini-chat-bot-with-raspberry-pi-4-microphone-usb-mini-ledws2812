import queue
import re
import sys
import os
import asyncio

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech as cloud_speech_types

import pyaudio

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
CHANNELS = 1
project_id = "beaming-benefit-445802-g5"
recognizer_id = "vb2024"

# Thiết lập thông tin xác thực Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'google_stt.json'

class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
        """The audio -- and generator -- is guaranteed to be on the main thread."""
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self: object) -> object:
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            #input_device_index=0,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(
        self: object,
        type: object,
        value: object,
        traceback: object,
    ) -> None:
        """Closes the stream, regardless of whether the connection was lost or not."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self: object,
        in_data: object,
        frame_count: int,
        time_info: object,
        status_flags: object,
    ) -> object:
        """Continuously collect data from the audio stream, into the buffer.

        Args:
            in_data: The audio data as a bytes object
            frame_count: The number of frames captured
            time_info: The time information
            status_flags: The status flags

        Returns:
            The audio data as a bytes object
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self: object) -> object:
        """Generates audio chunks from the stream of audio data in chunks.

        Args:
            self: The MicrophoneStream object

        Returns:
            A generator that outputs audio chunks.
        """
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses: object) -> None:
    data1 = ''
    for response in responses:
        if response.results:
            result = response.results[0]
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                # if not result.is_final:
                    # libs.logging('right','(HUMAN-STT-GG-CLOUD)' + transcript + '\r', 'dark_grey')
                if result.is_final:
                    data1 = transcript
                    break
    return data1

client = SpeechClient()

recognition_config = cloud_speech_types.RecognitionConfig(
    explicit_decoding_config=cloud_speech_types.ExplicitDecodingConfig(
        sample_rate_hertz=RATE,
        encoding=cloud_speech_types.ExplicitDecodingConfig.AudioEncoding.LINEAR16,
        audio_channel_count=CHANNELS
    ),
    language_codes=["vi-VN"],
    model="short",
)
streaming_config = cloud_speech_types.StreamingRecognitionConfig(
    config=recognition_config,
    streaming_features=cloud_speech_types.StreamingRecognitionFeatures(
        interim_results=True
    )
)
config_request = cloud_speech_types.StreamingRecognizeRequest(
    #recognizer = 'projects/'+global_constants.project_id+'/locations/global/recognizers/'+global_constants.recognizer_id, 
    recognizer = 'projects/'+project_id+'/locations/global/recognizers/'+recognizer_id, 
    streaming_config=streaming_config,
)

def requests(config: cloud_speech_types.RecognitionConfig, audio: list) -> list:
    """Helper function to generate the requests list for the streaming API.

    Args:
        config: The speech recognition configuration.
        audio: The audio data.
    Returns:
        The list of requests for the streaming API.
    """
    yield config
    for chunk in audio:
        yield cloud_speech_types.StreamingRecognizeRequest(audio=chunk)

def stt_process() -> None:
    """start bidirectional streaming from microphone input to speech API"""
    # print_out('left','Bắt đầu chạy','white')
    with MicrophoneStream() as stream:
        print("Listening ...")
        stream.audio_input = []
        
        audio_generator = stream.generator()
        # Transcribes the audio into text
        responses_iterator = client.streaming_recognize(
            requests=requests(config_request, audio_generator))
        data = listen_print_loop(responses_iterator)
        print(f"You said: {data}")
    return data

async def main():
    print('Bắt đầu thu âm')
    #data = await stt_process()
    data = stt_process()
    print(data)

if __name__ == '__main__': 

    asyncio.run(main())
    #run(main())