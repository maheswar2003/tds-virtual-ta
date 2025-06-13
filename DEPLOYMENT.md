# TDS Virtual TA - Deployment Guide

This guide explains how to deploy the TDS Virtual TA application to various cloud platforms.

## Prerequisites

1. **GitHub Repository**: Ensure your code is pushed to a public GitHub repository with an MIT LICENSE file.
2. **API Keys**: Obtain an OpenAI API key for AI-powered responses.

## Quick Start (Local Development)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/tds-virtual-ta.git
   cd tds-virtual-ta
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   ```bash
   cp env.example .env
   # Edit .env file with your OpenAI API key
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Test the API**:
   ```bash
   python test_example.py
   ```

## Deployment Options

### Option 1: Railway (Recommended)

Railway provides free deployment with easy GitHub integration.

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub**: Link your GitHub account
3. **Create new project**: Select "Deploy from GitHub repo"
4. **Choose repository**: Select your TDS Virtual TA repo
5. **Add environment variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `FLASK_ENV`: `production`
6. **Deploy**: Railway will automatically build and deploy

Your API will be available at: `https://your-app-name.railway.app/api/`

### Option 2: Render

Render offers free tier deployment with automatic builds.

1. **Sign up** at [render.com](https://render.com)
2. **Connect GitHub**: Link your GitHub account
3. **Create web service**: Choose "Build and deploy from a Git repository"
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. **Add environment variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `FLASK_ENV`: `production`
6. **Deploy**: Click "Create Web Service"

### Option 3: Heroku

Heroku provides reliable deployment with easy scaling.

1. **Install Heroku CLI**: Download from [heroku.com](https://heroku.com)
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Set environment variables**:
   ```bash
   heroku config:set OPENAI_API_KEY=your_api_key_here
   heroku config:set FLASK_ENV=production
   ```
5. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 4: Vercel

Vercel is great for serverless deployment.

1. **Install Vercel CLI**: `npm i -g vercel`
2. **Login**: `vercel login`
3. **Deploy**: `vercel --prod`
4. **Set environment variables** in Vercel dashboard

### Option 5: Google Cloud Run

For more control and scalability.

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8080
   CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
   ```

2. **Build and deploy**:
   ```bash
   gcloud run deploy tds-virtual-ta --source .
   ```

## Environment Variables

All deployment platforms require these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `FLASK_ENV` | Set to `production` | Yes |
| `PORT` | Port number (auto-set by most platforms) | No |

## Post-Deployment

### 1. Test Your API

Replace `YOUR_API_URL` with your deployed URL:

```bash
curl "YOUR_API_URL/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I use gpt-4o-mini or gpt-3.5-turbo?"}'
```

### 2. Run Evaluation

Update `project-tds-virtual-ta-promptfoo.yaml` with your API URL:

```yaml
providers:
  - id: tds-virtual-ta
    config:
      url: "YOUR_API_URL/api/"
```

Run evaluation:
```bash
npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
```

### 3. Submit Your Solution

Submit at: https://exam.sanand.workers.dev/tds-project-virtual-ta

Required information:
- GitHub repository URL
- API endpoint URL

## Troubleshooting

### Common Issues

1. **API not responding**:
   - Check if the service is running: `curl YOUR_API_URL/health`
   - Verify environment variables are set correctly

2. **OpenAI API errors**:
   - Ensure `OPENAI_API_KEY` is valid
   - Check API quota and billing

3. **Memory/timeout issues**:
   - Reduce model sizes in `src/processor.py`
   - Increase timeout settings in deployment config

4. **Package installation failures**:
   - Check Python version compatibility
   - Review `requirements.txt` for conflicts

### Monitoring

Most platforms provide built-in monitoring:
- **Railway**: Check logs in dashboard
- **Render**: View logs and metrics
- **Heroku**: Use `heroku logs --tail`

## Performance Optimization

1. **Caching**: Implement response caching for common questions
2. **Model optimization**: Use lighter models for faster responses
3. **Database**: Consider using a database for large knowledge bases
4. **CDN**: Use CDN for static assets if any

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Rate limiting**: Implement rate limiting for production use
3. **Input validation**: Validate all user inputs
4. **CORS**: Configure CORS appropriately for your use case

## Scaling

For high traffic:
1. **Horizontal scaling**: Increase number of instances
2. **Load balancing**: Use platform-provided load balancing
3. **Database**: Move from JSON files to a proper database
4. **Caching**: Implement Redis or similar for caching

## Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Test locally first
- Ensure all environment variables are set correctly 