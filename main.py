import os
import asyncio
import speech_recognition as sr
from dotenv import load_dotenv
from openai import AsyncOpenAI
from playsound import playsound

load_dotenv()

client = AsyncOpenAI()

recognizer = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("🎤 Speak...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except:
        return None

async def speak(text):
    response = await client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
        response_format="mp3",
    )

    with open("output.mp3", "wb") as f:
        f.write(response.content)

    playsound("output.mp3")

    os.remove("output.mp3")
        

async def main():
    while True:
        user_text = listen()
        if not user_text:
            continue

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}],
        )

        reply = response.choices[0].message.content
        print("🤖:", reply)

        await speak(reply)


if __name__ == "__main__":
    asyncio.run(main())