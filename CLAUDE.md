# CLAUDE.md - Glory Traders Telegram Bot

You're an expert in developing Telegram bots with 20+ years of experience in Python development. You possess deep knowledge of high-quality code practices, web scraping, automation, and financial calculation systems. You have extensive experience with the following technologies and frameworks used in this project:

## Technology Stack & Expertise

### Core Technologies
- **Python 3.x** - Primary development language
- **pyTelegramBotAPI (4.25.0)** - Telegram Bot API wrapper
- **telebot (0.0.5)** - Additional Telegram bot utilities

### Web Scraping & Automation
- **Selenium (4.25.0)** - Web browser automation
- **selenium-wire (5.1.0)** - Enhanced Selenium with request/response interception
- **undetected-chromedriver (3.5.5)** - Anti-detection ChromeDriver
- **chromedriver-autoinstaller (0.6.4)** - Automatic ChromeDriver management
- **chromedriver-binary (133.0.6855.0.0)** - ChromeDriver binary
- **BeautifulSoup4 (4.12.3)** - HTML/XML parsing
- **requests (2.32.3)** - HTTP library
- **PyVirtualDisplay (3.0)** - Virtual display for headless environments

### Data Processing & Storage
- **psycopg2 (2.9.10)** - PostgreSQL adapter
- **python-dotenv (1.0.1)** - Environment variable management

### Networking & Security
- **httpx (0.25.1)** - Modern HTTP client
- **aiohttp (3.10.10)** - Asynchronous HTTP client/server
- **cryptography (43.0.3)** - Cryptographic recipes
- **PySocks (1.7.1)** - SOCKS proxy support

### CAPTCHA Solving
- **2captcha-python (1.5.0)** - 2captcha service integration
- **TwoCaptcha (0.0.1)** - Alternative 2captcha wrapper

### Async Programming
- **playwright (1.48.0)** - Modern web automation
- **trio (0.27.0)** - Async I/O library
- **anyio (3.7.1)** - High-level async library

## Project Overview

The Glory Traders Telegram Bot is a specialized financial calculator that helps users estimate the total cost of importing vehicles from South Korea to CIS countries (Russia, Kazakhstan, Kyrgyzstan). The bot provides:

1. **Automated Cost Calculation** - Extracts car data from Encar.com links and calculates import costs
2. **Manual Input Support** - Allows users to manually enter vehicle specifications
3. **Multi-Country Support** - Handles different customs regulations for Russia, Kazakhstan, and Kyrgyzstan
4. **Real-time Currency Rates** - Fetches current exchange rates from multiple central banks
5. **Insurance History Analysis** - Retrieves vehicle accident history and insurance claims

## Architecture & File Structure

```
glory-traders-telegram-bot/
├── main.py                    # Main bot entry point and message handlers
├── calculator.py              # Core calculation logic and web scraping
├── config.py                  # Bot configuration and initialization
├── utils.py                   # Utility functions (customs, formatting, etc.)
├── get_car_info.py           # Car data extraction from Encar.com
├── get_insurance_total.py     # Insurance history data extraction
├── kgs_customs_table.py      # Kyrgyzstan customs duty table
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment configuration
├── runtime.txt               # Python runtime version
├── .env                      # Environment variables (not in repo)
└── notes.txt                 # Important calculation notes and references
```

## Key Components

### 1. Bot Handlers (`main.py`)
- **Command Handlers**: `/start`, `/cbr`, `/nbk`, `/nbkr`
- **Message Handlers**: Country selection, calculation options, manual input
- **Callback Handlers**: Inline keyboard interactions
- **State Management**: User session data and calculation flow

### 2. Calculation Engine (`calculator.py`)
- **Web Scraping**: Automated data extraction from Korean car sites
- **Currency Exchange**: Real-time rates from central banks (CBR, NBK, NBKR)
- **Cost Calculation**: Complex algorithms for customs duties, taxes, and fees
- **Database Integration**: PostgreSQL for caching car data

### 3. Utilities (`utils.py`)
- **Customs Calculations**: Russia-specific customs duty calculations
- **Age Calculations**: Vehicle age determination for tax purposes
- **Number Formatting**: Locale-aware currency formatting
- **Memory Management**: Garbage collection utilities

### 4. Data Sources
- **Encar.com**: Primary source for Korean car listings
- **Central Bank APIs**: Currency exchange rates
- **Customs APIs**: Real-time duty calculations
- **Insurance Reports**: Vehicle history verification

## Development Guidelines

### Code Style
- Follow PEP 8 standards
- Use meaningful variable names in English with Russian comments where needed
- Implement proper error handling with try-except blocks
- Use type hints where applicable
- Maintain consistent indentation (4 spaces)

### Error Handling
- Always wrap web scraping in try-catch blocks
- Provide user-friendly error messages in Russian
- Log detailed errors for debugging
- Implement fallback mechanisms for API failures

### Security Practices
- Store sensitive data in environment variables
- Use SSL connections for database access
- Implement rate limiting for API calls
- Sanitize all user inputs
- Use secure proxy configurations

### Database Operations
- Use connection pooling for PostgreSQL
- Implement proper transaction handling
- Cache frequently accessed data
- Use prepared statements to prevent SQL injection

## Environment Variables

Required environment variables in `.env`:
```
BOT_TOKEN=your_telegram_bot_token
CHROMEDRIVER_PATH_LOCAL=path_to_chromedriver
DATABASE_URL=postgresql_connection_string
```

## Key Functions

### Currency Rates
- `get_currency_rates()` - Russian Central Bank rates (CBR)
- `get_nbk_currency_rates()` - Kazakhstan National Bank rates
- `get_nbkr_currency_rates()` - Kyrgyzstan National Bank rates
- `get_usdt_krw_rate()`, `get_usdt_rub_rate()` - Cryptocurrency rates

### Cost Calculations
- `calculate_cost(country, message)` - Main calculation from Encar link
- `calculate_cost_manual()` - Manual input calculation
- `get_customs_fees_russia()` - Russian customs duty API integration
- `calculate_customs_fee_kg()` - Kyrgyzstan customs table lookup

### Data Extraction
- `get_car_info(url)` - Extract car details from Encar.com
- `get_insurance_total()` - Fetch insurance/accident history

## Testing & Deployment

### Testing Approach
- Test with real Encar.com URLs
- Validate calculations against official customs calculators
- Test all supported countries and car types
- Verify currency rate accuracy

### Deployment
- **Platform**: Heroku (configured via Procfile)
- **Runtime**: Python 3.x (specified in runtime.txt)
- **Process**: Worker process running main.py
- **Database**: PostgreSQL with SSL

## Important Considerations

### Web Scraping Challenges
- Websites use anti-bot measures (CAPTCHA, rate limiting)
- DOM structure changes require code updates
- Proxy rotation may be necessary
- Headless browser detection countermeasures

### Multi-Country Complexity
- Different tax structures per country
- Various customs duty calculation methods
- Currency conversion requirements
- Regulatory compliance variations

### Performance Optimization
- Use threading for concurrent operations
- Implement caching for repeated requests
- Optimize database queries
- Memory management for long-running processes

### User Experience
- Provide progress indicators for long operations
- Support both automated and manual input methods
- Multi-language support (Russian interface)
- Clear error messages and guidance

## Recent Updates & Notes

The bot currently supports:
- Russia: Full customs calculation via calcus.ru API
- Kazakhstan: Custom calculation logic
- Kyrgyzstan: Table-based customs duty lookup with car type differentiation

Critical reference: Kazakhstan calculation verification available at https://findauto.kz/calc

## Development Workflow

When working on this project:
1. Test changes with real Encar URLs
2. Verify calculations against official sources
3. Update customs tables when regulations change
4. Monitor for website structure changes
5. Implement proper logging for production debugging
6. Follow security best practices for credentials and API keys

This bot handles significant financial calculations, so accuracy and reliability are paramount. Always validate changes thoroughly before deployment.