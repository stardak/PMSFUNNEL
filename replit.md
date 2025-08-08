# Portugal Made Simple - Landing Page

## Overview

This project has been transformed from a YouTube title generator into a clean landing page for "Portugal Made Simple" - a service helping people relocate to Portugal. The landing page features:

1. Portugal Made Simple branding with logo
2. Compelling headline about Portugal relocation opportunity  
3. Embedded Wistia video player for explanatory content
4. Calendly booking widget for scheduling consultation calls
5. Clean, minimal design focused on conversion

The application is built with Flask and uses a single-page layout optimized for lead generation and booking conversions.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (August 2025)

**Application Cleanup & A/B Testing Implementation (August 8, 2025)**
- Removed all YouTube-related functionality and dependencies (youtube_utils, openai_utils, transcript extractors)
- Cleaned up unused routes (/generate, /auth, /oauth/callback, /dashboard)
- Removed unnecessary dependencies (OpenAI, Google APIs, YouTube libraries, Stripe, etc.)
- Simplified to core dependencies: Flask, SQLAlchemy, PostgreSQL, Gunicorn
- Implemented complete A/B testing system with PostgreSQL database for visitor and conversion tracking
- Set up two video variants: A (jz42mm3kzf) and B (ncb9bu8s4y) for split testing
- Created analytics dashboard at /ab-test-results for monitoring test performance
- Replaced Calendly with Typeform embed (01K24WCFJ08WGQB06K1Q0PVFFY)
- Added conversion tracking system that monitors clicks on Typeform widget to measure booking intent
- 50/50 visitor split between variants with consistent experience per visitor
- Database stores visitor data, variant assignments, and conversion events with timestamps
- Removed unused templates (dashboard.html, landing.html, login.html, signup.html)

**Complete Transformation to Portugal Landing Page (August 6, 2025)**
- Converted entire application from YouTube title generator to Portugal relocation landing page
- Replaced all content with "Portugal Made Simple" branding and messaging
- Updated main headline to "Thousands are relocating to Portugal. Watch this to see how you can too—without the overwhelm."
- Integrated Wistia video player for explanatory content (media-id: jz42mm3kzf)
- Added Calendly booking widget for 15-minute consultation calls
- Removed navigation bar, Google sign-in, and all YouTube-related functionality
- Simplified layout to focus on lead generation and conversion
- Updated logo to Portugal Made Simple branding (pms-black_1754498993209.png)
- Clean, minimal single-page design optimized for the Portugal relocation service

## System Architecture

### Backend Architecture

The application follows a simple Flask-based architecture:

- **Framework**: Flask serves as the web framework
- **API Endpoints**: RESTful endpoints handle YouTube URL processing
- **Processing Flow**: Audio extraction → Transcription → Title generation
- **Error Handling**: Robust fallback mechanisms when primary methods fail
- **Temporary Storage**: Uses Python's tempfile for managing downloaded audio

This approach provides a lightweight, maintainable backend that can be easily deployed on Replit's infrastructure.

### Frontend Architecture

The frontend is built with:

- **HTML/CSS/JavaScript**: Standard web technologies for UI
- **Bootstrap**: Provides responsive layouts and theming
- **AJAX**: Asynchronous requests for a smooth user experience
- **CSS Animations**: Visual feedback during processing

The UI is designed to be clean, intuitive, and provide clear feedback during the multistep processing flow.

### Authentication

- **API Keys**: Uses environment variables for secure storage of OpenAI and YouTube API keys
- **No User Authentication**: Public access application with no user accounts

## Key Components

### 1. Main Application (`app.py`, `main.py`)

- Initializes Flask application
- Sets up routes and request handling
- Configures middleware and session security
- Orchestrates the processing flow

### 2. YouTube Utilities (`youtube_utils.py`)

- Extracts video IDs from YouTube URLs
- Downloads audio from YouTube videos using pytube
- Falls back to YouTube Data API for captions when audio extraction fails
- Handles various YouTube URL formats

### 3. OpenAI Utilities (`openai_utils.py`)

- Transcribes audio using Whisper API
- Generates title suggestions using GPT-4o
- Manages API rate limits and errors
- Optimizes prompt engineering for title generation

### 4. Frontend Components

- **HTML Templates**: Define the UI structure (`templates/index.html`)
- **CSS**: Styling and animations (`static/css/style.css`)
- **JavaScript**: Client-side logic and AJAX requests (`static/js/script.js`)

## Data Flow

1. **Input**: User submits YouTube URL via web form
2. **Processing**:
   - Backend extracts video ID and attempts to download audio
   - If successful, audio is transcribed with Whisper API
   - If audio extraction fails, falls back to YouTube captions API
   - Transcript is processed by GPT-4o to generate title ideas
3. **Output**: 
   - Title suggestions are returned to frontend
   - Transcript and processing source are displayed
   - Any errors are presented with helpful messages

## External Dependencies

### API Services
- **OpenAI API**: Used for audio transcription (Whisper) and title generation (GPT-4o)
- **YouTube Data API**: Used as a fallback for retrieving video captions

### Python Libraries
- `flask`: Web framework
- `pytube`: YouTube video/audio extraction
- `openai`: OpenAI API client
- `google-api-python-client`: YouTube Data API client
- Additional support libraries listed in `pyproject.toml`

### System Dependencies
- `ffmpeg`: Required for audio processing
- `openssl`: Security and cryptography
- `postgresql`: Potentially used for future database integration

## Deployment Strategy

The application is configured for deployment on Replit's infrastructure:

- **Target**: Autoscale deployment
- **Run Command**: `gunicorn --bind 0.0.0.0:5000 main:app`
- **Environment**: Python 3.11 with Nix package manager
- **System Dependencies**: Installed via Nix (ffmpeg, openssl, postgresql)
- **Environment Variables**: Required for API keys (OPENAI_API_KEY, YOUTUBE_API_KEY)

For local development, the application can be run using `python main.py` which will start Flask in debug mode.

## Future Considerations

1. **Database Integration**: The project structure suggests future integration with a database, possibly PostgreSQL, for storing results or user preferences.

2. **Authentication System**: Adding user accounts could enable saving favorite titles and history.

3. **Additional Language Models**: The architecture supports easy integration of additional AI models for different creative tasks.

4. **Enhanced Analytics**: Adding metrics on title effectiveness could provide additional value.