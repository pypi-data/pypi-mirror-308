# Usage

This page contains a few examples of how to use the `pyflowery` package. This page does not cover installation, for that see the [installation](installation.md) page.

## Creating an API client

To create an API client, you need to first import the `pyflowery.pyflowery.FloweryAPI` class. Then, you can create an instance of the class by passing in a `pyflowery.models.FloweryAPIConfig` class.

```python
from pyflowery import FloweryAPI, FloweryAPIConfig
config = FloweryAPIConfig(user_agent="PyFlowery Documentation Example/example@foobar.com")
api = FloweryAPI(config)
```

Okay, now we have a `FloweryAPI` class. Let's move on to the next example.

## Retrieving a voice

So, whenever a `FloweryAPI` class is instantiated, it will automatically fetch a list of voices from the Flowery API, and cache it in the class. You can access this cache by calling the `get_voices` method with either a voice's ID or the name of a voice. If you want to get a list of all voices, you can call the `get_voices` method without any arguments.

```python
# Set up the API client
from pyflowery import FloweryAPI, FloweryAPIConfig
config = FloweryAPIConfig(user_agent="PyFlowery Documentation Example/example@foobar.com")
api = FloweryAPI(config) # This will fetch all of the voices from the API and cache them automatically, you don't need to do that manually

voices = api.get_voices(name="Alexander")
print(voices) # (Voice(id='fa3ea565-121f-5efd-b4e9-59895c77df23', name='Alexander', gender='Male', source='TikTok', language=Language(name='English (United States)', code='en-US')),)
print(voices[0].id) # 'fa3ea565-121f-5efd-b4e9-59895c77df23'
```

## Updating the API client's voice cache

In most use cases, it is not necessary to manually update the voice cache. But, for applications that run for an extended period of time, it may be necessary to manually update the voice cache. To do this, you can call the `_populate_voices_cache()` async method.

```python
import asyncio # This is required to run asynchronous code outside of async functions
from pyflowery import FloweryAPI, FloweryAPIConfig
config = FloweryAPIConfig(user_agent="PyFlowery Documentation Example/example@foobar.com")
api = FloweryAPI(config) # This will fetch all of the voices from the API and cache them automatically, you don't need to do that manually

asyncio.run(api._populate_voices_cache()) # This will update the voice cache. This is what `FloweryAPI` calls automatically when it is instantiated
```

## Retrieving a list of voices from the API directly

If necessary, you can call the `fetch_voices()` or `fetch_voice()` methods. These methods will fetch the voices from the API directly, skipping the cache. This isn't recommended, though, as it puts more strain on the Flowery API.  

<!-- markdownlint-disable code-block-style -->

=== "`fetch_voices()`"
    `fetch_voices()` returns an `AsyncContextManager`, so you need to iterate through it when you call it.

    ```python
    import asyncio
    from pyflowery import FloweryAPI, FloweryAPIConfig
    config = FloweryAPIConfig(user_agent="PyFlowery Documentation Example/example@foobar.com")
    api = FloweryAPI(config)

    async def fetch_voices():
        voices_list = []
        async for voice in api.fetch_voices():
            voices_list.append(voice)
        return voices_list

    voices = asyncio.run(fetch_voices())
    ```

=== "`fetch_voice()`"

    ```python
    import asyncio
    from pyflowery import FloweryAPI, FloweryAPIConfig
    config = FloweryAPIConfig(user_agent="PyFlowery Documentation Example/example@foobar.com")
    api = FloweryAPI(config)

    voice_id = "38f45366-68e8-5d39-b1ef-3fd4eeb61cdb"

    voice = asyncio.run(api.fetch_voice(voice_id))
    print(voice) # Voice(id='38f45366-68e8-5d39-b1ef-3fd4eeb61cdb', name='Jacob', gender='Male', source='Microsoft Azure', language=Language(name='English (United States)', code='en-US'))
    ```

<!-- markdownlint-enable code-block-style -->

## Converting text to audio

Finally, let's convert some text into audio. To do this, you can call the `fetch_tts()` method. This will return the bytes of the audio file.

```python
import asyncio
from pyflowery import FloweryAPI, FloweryAPIConfig
config = FloweryAPIConfig(user_agent="PyFlowery Documentation Example/example@foobar.com")
api = FloweryAPI(config)

voice = api.get_voices(name="Alexander")[0]

tts = asyncio.run(api.fetch_tts("Hello, world!", voice))
with open("hello_world.mp3", "wb") as f:
    f.write(tts)
```
