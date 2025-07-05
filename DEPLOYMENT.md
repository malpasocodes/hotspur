# Deployment Guide for Hotspur

## Render Deployment

### Prerequisites
1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Data Files**: Ensure Shakespeare data is available

### Quick Deploy to Render

#### Option 1: Deploy Button (Recommended)
Add this to your GitHub README for one-click deployment:

```markdown
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/hotspur)
```

#### Option 2: Manual Deployment

1. **Connect Repository**:
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**:
   - **Name**: `hotspur-shakespeare-search`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `streamlit run hotspur_search/streamlit_app/app.py --server.port $PORT --server.address 0.0.0.0`

3. **Environment Variables**:
   ```
   STREAMLIT_SERVER_PORT=$PORT
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
   ```

4. **Deploy**: Click "Create Web Service"

### Expected Build Process

1. **Dependencies Installation** (~2-3 minutes)
   - Installs Python packages from requirements.txt
   - Sets up Whoosh, Streamlit, pandas

2. **Data Processing** (~3-5 minutes)
   - Parses Shakespeare texts into searchable segments
   - Creates search index (~93k documents)

3. **Verification** (~30 seconds)
   - Tests search functionality
   - Confirms all components working

**Total Build Time**: ~5-8 minutes

### Troubleshooting Deployment

#### Build Fails - Missing Data
**Error**: `Shakespeare data not found`
**Solution**: Ensure `data/processed/shakespeare_only.txt` is in your repository or available for download

#### Build Timeout
**Error**: Build takes too long
**Solution**: Consider pre-building the search index and including it in the repository

#### Memory Issues
**Error**: Out of memory during build
**Solution**: Use a higher Render plan or optimize the build process

#### Start Command Fails
**Error**: Streamlit won't start
**Solution**: Check that the start command matches your file structure

### Performance Considerations

#### Free Tier Limitations
- **Memory**: 512 MB RAM
- **CPU**: Shared
- **Sleep**: Service sleeps after 15 minutes of inactivity
- **Build Time**: 15 minute limit

#### Optimization for Free Tier
```bash
# In build.sh, add memory optimization
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50
export STREAMLIT_SERVER_MAX_MESSAGE_SIZE=50
```

#### Recommended Upgrades
- **Starter Plan** ($7/month): 1GB RAM, no sleep
- **Pro Plan** ($25/month): 4GB RAM, faster builds

### Post-Deployment

#### Health Check
Once deployed, verify:
1. App loads at your Render URL
2. Search interface is responsive
3. All 31 works appear in dropdown
4. Search results return correctly
5. Export functionality works

#### Monitoring
- **Render Dashboard**: Monitor uptime and performance
- **Logs**: Check application logs for errors
- **User Feedback**: Monitor for search issues

### Custom Domain (Optional)

1. **Add Domain in Render**:
   - Go to your service settings
   - Add custom domain
   - Follow DNS configuration instructions

2. **SSL Certificate**:
   - Automatically provided by Render
   - No additional configuration needed

### Alternative Deployment Options

#### Streamlit Cloud
```bash
# Requirements for Streamlit Cloud
pip freeze > requirements.txt
# Push to GitHub, deploy via share.streamlit.io
```

#### Heroku
```bash
# Additional files needed for Heroku
echo "web: streamlit run hotspur_search/streamlit_app/app.py --server.port \$PORT" > Procfile
echo "python-3.9.*" > runtime.txt
```

#### Docker (Self-hosted)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN ./build.sh

EXPOSE 8501
CMD ["streamlit", "run", "hotspur_search/streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Environment Variables Reference

| Variable | Purpose | Default |
|----------|---------|---------|
| `STREAMLIT_SERVER_PORT` | Port for Streamlit | `$PORT` (Render) |
| `STREAMLIT_SERVER_ADDRESS` | Bind address | `0.0.0.0` |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | Disable analytics | `false` |
| `STREAMLIT_THEME_BASE` | UI theme | `light` |

### Security Considerations

#### Production Settings
- Disable debug mode
- Use HTTPS (automatic with Render)
- Limit file upload sizes
- Monitor for abuse

#### Data Privacy
- No user data stored
- Search queries not logged
- Shakespeare texts are public domain

### Support

#### Common Issues
1. **Slow initial load**: First search builds index
2. **Memory warnings**: Expected on free tier
3. **Search timeouts**: Restart service if needed

#### Getting Help
- **Render Support**: For deployment issues
- **GitHub Issues**: For application bugs
- **Documentation**: Check all .md files in repository