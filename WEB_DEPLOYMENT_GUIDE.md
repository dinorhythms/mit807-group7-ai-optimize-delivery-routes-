# MetroSwift Web Application Deployment Guide

## Overview

This guide explains how to deploy the MetroSwift web application on Render.com and access it through your browser.

## What's New

The web version includes:

- **Modern Web Interface**: Responsive, professional UI accessible from any browser
- **Same Algorithms**: BFS, DFS, and A\* route optimization
- **Dynamic Parameters**: Real-time adjustable traffic, peak, weather, and reroute factors
- **API Backend**: Flask-based REST API for route computation
- **Cloud Ready**: Optimized for Render.com deployment

## Files Created

### Backend

- `web_app.py` - Flask application with API endpoints

### Frontend

- `templates/index.html` - Main web interface
- `static/css/style.css` - Professional, responsive styling
- `static/js/script.js` - Frontend logic and API interactions

### Deployment Configuration

- `Procfile` - Process file for Render.com
- `render.yaml` - Render.com configuration
- `requirements.txt` - Updated with Flask and gunicorn dependencies

## Local Testing

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Application Locally

```bash
python web_app.py
```

The app will be available at `http://localhost:5000`

### 3. Test the Web Interface

- Open your browser and navigate to `http://localhost:5000`
- Use the control panel to select source/destination
- Adjust dynamic parameters (Traffic, Peak, Weather, Reroute)
- Click "Run BFS", "Run DFS", or "Run A\*" to analyze routes
- View instant results in the Results section

## Deployment to Render.com

### Prerequisites

1. GitHub account (to host your code)
2. Render.com account (free tier available)

### Step 1: Push Code to GitHub

```bash
# Initialize git if needed
git init

# Add all files
git add .

# Commit
git commit -m "Add MetroSwift web application"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render.com

1. **Create Account**: Sign up at [render.com](https://render.com)
2. **Connect GitHub**: Link your GitHub account in Render dashboard
3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Select your GitHub repository
   - Choose branch: `main`
4. **Configure Service**:
   - **Name**: `metroswift` (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
   - **Instance Type**: Free (or select your preferred tier)
5. **Deploy**: Click "Deploy"

Render will automatically:

- Build your application
- Install dependencies
- Start the web service
- Provide a public URL (e.g., `https://metroswift.onrender.com`)

### Step 3: Access Your Application

Once deployment is complete, visit your application at the Render-provided URL. The web interface will load immediately.

## API Endpoints

### 1. Health Check

- **Endpoint**: `GET /health`
- **Purpose**: Verify application is running
- **Response**: `{"status": "healthy"}`

### 2. Get Available Nodes

- **Endpoint**: `GET /api/nodes`
- **Response**: `{"nodes": ["Lekki", "Victoria Island", ...]}`

### 3. Run BFS Algorithm

- **Endpoint**: `POST /api/run-bfs`
- **Body**:

```json
{
  "source": "Depot",
  "destination": "Ajah"
}
```

- **Response**: Path, traversal order, and distance

### 4. Run DFS Algorithm

- **Endpoint**: `POST /api/run-dfs`
- **Body**: Same as BFS

### 5. Run A\* Algorithm

- **Endpoint**: `POST /api/run-astar`
- **Body**:

```json
{
  "source": "Depot",
  "destination": "Ajah",
  "traffic_level": 0.55,
  "peak_factor": 0.35,
  "weather_factor": 0.1,
  "reroute_factor": 0.08
}
```

- **Response**: Path, traversal order, and predicted travel time

## Feature Highlights

### Control Panel

- **Source Location**: Select starting point
- **Destination**: Select delivery endpoint
- **Traffic Level** (0.1 - 1.0): Current road congestion
- **Peak Factor** (0 - 1.0): Rush hour intensity
- **Weather Impact** (0 - 0.6): Weather-related delays
- **Reroute Impact** (0 - 0.5): Unexpected disruption factor

### Algorithm Selection

- **BFS Search**: Explores all neighbors at current depth
- **DFS Search**: Explores deeply along each branch
- **A\* Optimizer**: AI-powered optimal route with dynamic parameters

### Results Display

- **Traversal Order**: Nodes visited during search
- **Optimal Path**: Best route from source to destination
- **Metrics**: Distance (km) or Predicted Travel Time (minutes)
- **Scenario Parameters**: (A\* only) Shows applied dynamic factors

## Troubleshooting

### Application Won't Start

- Check `requirements.txt` includes Flask and gunicorn
- Verify all app files are in the correct directories
- Review Render deployment logs

### Web Page Won't Load

- Ensure health check passes: `GET /health` should return `{"status": "healthy"}`
- Wait 5-10 minutes after initial deployment for cold start
- Check Render dashboard for error logs

### Algorithm Returns No Results

- Verify source and destination are different
- Confirm both locations exist in the node list
- Check console (browser F12) for API error messages

### Port Issues

- Render automatically assigns a PORT environment variable
- `web_app.py` reads this: `port = int(os.environ.get('PORT', 5000))`
- No manual port configuration needed

## Performance Notes

- **Free Tier**: Auto-spins down after 15 minutes of inactivity (cold start ~30s on next request)
- **Paid Tier**: Dedicated resources with instant response
- **Data**: Network graph loads into memory on startup
- **API Response**: ~100-500ms depending on route complexity

## Future Enhancements

- Route visualization on map
- Multiple route comparison
- Historical analytics
- Real-time traffic integration
- Mobile app version

## Support & Documentation

- MetroSwift Technical Report: See `MetroSwift_Technical_Report.md`
- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com/

---

**Now your MetroSwift application is accessible globally through a web browser!** 🚀
