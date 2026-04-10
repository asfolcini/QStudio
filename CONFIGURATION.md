# Configuration Setup

The `qstudio-configuration.json` file contains sensitive API credentials and should never be committed to version control.

## Setup Instructions

1. Create a copy of this file:
```bash
cp config/qstudio-configuration.json.example config/qstudio-configuration.json
```

2. Fill in your actual API credentials:
```json
{
    "LLM_API_URL": "https://your-actual-api-url.com",
    "LLM_API_KEY": "your-real-api-key-here",
    "LLM_MODEL": "qwen"
}
```

3. Make sure the configuration file is properly ignored by adding it to `.gitignore`