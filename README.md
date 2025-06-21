# 📚 Echobook AI

**Turn any book into expressive speech with your voice or a cloned one**

Echobook AI is a open-source audio book generator powered by Resemble AI's Chatterbox TTS. It lets you convert text files into naturally sounding audio using voice cloning or expressive synthetic voices.

---

## ✨ Features

- 🎙️ **Voice Cloning**: Create a digital replica of your voice from just a short reference clip
- 😄 **Emotion Control**: Adjust speech parameters to convey different emotions and expressions
- 🎧 **Expressive Speech**: Generate natural-sounding audio with your cloned voice and chosen emotions
- 🖥️ **Web Interface**: User-friendly browser-based application for easy access
- 📚 **Multiple Format Support**: Convert books from various text formats (TXT, EPUB, PDF)
- 💾 **Export Options**: Save audio in multiple formats (MP3, WAV) for different devices

---

## 🗃️ Speech Generation via Resemble AI API

This project uses the [Resemble AI Web API](https://docs.resemble.ai/docs) for real-time text-to-speech (TTS) and voice cloning.

Resemble provides high-quality, expressive, and customizable synthetic voices with emotion control and voice cloning features.

You’ll need to:

1. **Sign up** at [https://www.resemble.ai](https://www.resemble.ai)
2. **Create an API token** under your account settings
3. **Create a project** and at least one voice in the Resemble dashboard
4. **Create a `.env` file in your project root** and store the following values:
    ```env
    RESEMBLE_API_KEY=your_resemble_api_key_here
    RESEMBLE_PROJECT_ID=your_project_id_here
   ```