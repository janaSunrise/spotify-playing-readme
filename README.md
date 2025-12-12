# Spotify Playing for README

Display your Spotify listening status on GH README and websites with a beautiful, customizable widget.

## Setup

### Prerequisites

- Python 3.11+
- `uv` package manager
- Spotify Developer Account
- Supabase Account

### Local Development

1. **Clone the repository**
   ```sh
   git clone https://github.com/janaSunrise/spotify-playing-readme
   cd spotify-playing-readme
   ```

2. **Install dependencies**
   ```sh
   uv sync --all-groups
   ```

3. **Configure Spotify API**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Add `http://localhost:8000/callback` to Redirect URIs
   - Note your Client ID and Client Secret

4. **Configure Supabase**
   - Create a new project on [Supabase](https://supabase.com)
   - Setup the database with the schema from `schema.sql`
   - Get your project URL and API key

5. **Configure environment variables**

   Create a `.env` file based on `.env.example` and fill in the required values. Don't include a trailing slash in `BASE_URL`.

6. **Generate a secure secret key**

   You need a secure secret key for session management. Generate one using Python:
   ```sh
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Or using OpenSSL:
   ```sh
   openssl rand -hex 32
   ```
   Copy the generated key and use it as your `SESSION_SECRET_KEY` in the `.env` file.

7. **Run the application**
   ```sh
   uv run poe dev
   ```

The app will be available at `http://localhost:8000`

## Self-Hosting

### Configuration

Update the `.env` file for production:

- Set `BASE_URL` to your domain
- Generate a secure `SESSION_SECRET_KEY` (see step 6 in Local Development)
- Update Spotify redirect URI to `https://yourdomain.com/callback`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

**Inspired by [Novatorem](https://github.com/novatorem)**
