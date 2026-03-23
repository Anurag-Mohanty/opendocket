# Deploy OpenDocket Backend to Railway

1. Go to railway.app and sign up (free tier available)
2. New Project > Deploy from GitHub repo
3. Select your opendocket repo
4. Set root directory: `/` (root)
5. Set start command: `python scanner/api.py`
6. Add environment variables:
   - `ANTHROPIC_API_KEY=your_key`
   - `GEMINI_API_KEY=your_key`
   - `PORT=8080`
   - `DAILY_SCAN_LIMIT=200`
   - `MONTHLY_SCAN_LIMIT=2000`
7. Railway will give you a URL like:
   `https://opendocket-production.up.railway.app`
8. Update `API_BASE_URL` in `web/index.html` to this URL
