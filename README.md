# YouTube Title Generator

A web application that generates creative title ideas for YouTube videos by analyzing the video's audio content or captions.

## Features

- Extract audio from YouTube videos using pytube
- Transcribe audio using OpenAI's Whisper API
- Fall back to YouTube Data API for captions when audio extraction fails
- Generate creative title ideas using OpenAI's GPT-4o
- Clean, responsive UI with error handling and loading states

## Setup Instructions

### Prerequisites

- Python 3.7+
- A Replit account
- OpenAI API key
- YouTube Data API key

### Environment Variables

Set up the following environment variables in your Replit:

1. `OPENAI_API_KEY` - Your OpenAI API key
2. `YOUTUBE_API_KEY` - Your YouTube Data API key
3. `SESSION_SECRET` - A random string for Flask session security (optional)

To set up environment variables in Replit:
1. Click on the lock icon in the sidebar
2. Add each key-value pair
3. Click "Save"

### Installing Dependencies

The project requires the following packages:
- Flask
- pytube
- openai
- google-api-python-client

These will be installed automatically via the `requirements.txt` file. Replit will handle this for you.

### Installing ffmpeg

The application requires ffmpeg for audio processing. To install it in Replit:

1. Open the Replit shell
2. Run: `nix-env -i ffmpeg-full`
3. Wait for the installation to complete

## Running the Application

1. Click the "Run" button in Replit
2. The application will start and be available at the provided URL

## Troubleshooting

### Common Issues

#### pytube Errors
- **RegexMatchError**: YouTube may have changed their page structure. Try updating pytube with: `pip install --upgrade pytube`
- **HTTP Errors**: Temporary YouTube connection issues. Try again later.

#### YouTube API Issues
- **Quota Exceeded**: The YouTube Data API has daily quota limits. If exceeded, you'll need to wait until it resets.
- **Missing Captions**: Some videos may not have captions available, and the app will try to fall back to title/description.

#### OpenAI API Issues
- **Authentication Errors**: Check that your API key is correct and has enough credits.
- **Rate Limits**: OpenAI may rate-limit requests. The application will display appropriate error messages.

## How It Works

1. User inputs a YouTube URL
2. Application attempts to download the audio using pytube
3. Audio is transcribed using OpenAI's Whisper API
4. If audio download fails, falls back to retrieving captions via YouTube Data API
5. The transcript/captions are sent to OpenAI's GPT-4o to generate creative title ideas
6. Results are displayed to the user

## License

This project is meant for educational purposes and personal use only.
