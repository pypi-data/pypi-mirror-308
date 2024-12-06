# pyDuckChat

An unofficial library to send messages and receive responses asynchronously with DuckDuckGo chat API. You can use GPT-4o mini, Claude 3 Haiku, Llama 3.1 70B, Mixtral 8x7B for free.

## Installation

You can install the library using pip:

```bash
pip install git+https://github.com/tolgakurtuluss/pyduckchat.git
```

### Model

Available AI models:

- `GPT_4O_MINI`
- `CLAUDE_3_HAIKU`
- `META_LLAMA`
- `MISTRALAI`

## Usage

```python
# Run the main function in an async context
from pyduckchat.chat import init_chat, Model

async def main():
    chat_instance = await init_chat(Model.GPT_4O_MINI)
    response = await chat_instance.fetch_full("Hello, how are you?")
    print(response)
```

## Credits and Terms of Service

[DuckDuckGo Help Pages](https://duckduckgo.com/duckduckgo-help-pages/aichat/)

[DuckDuckGo AI Chat Privacy Policy and Terms of Use](https://duckduckgo.com/aichat/privacy-terms)