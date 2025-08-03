# Railway Deployment Testing Guide

## 🚀 **Railway Deployment Testing**

### **1. Pre-Deployment Local Testing**

#### **Test Railway Startup Script**

```bash
# Start the Railway startup script locally
python3 railway_start.py &

# Test health endpoint
curl -s http://localhost:8000/health

# Test text checking
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjouwr, comment allez-tu?"}'

# Stop the server
pkill -f "python3 railway_start.py"
```

#### **Test Package Installation**

```bash
# Test local package installation
pip3 install -e . --force-reinstall

# Verify Grammalecte import
python3 -c "import grammalecte; print('Success')"
```

### **2. Railway Deployment Testing**

#### **Deploy to Railway**

1. **Push to GitHub** (if not already done)
2. **Connect to Railway**: Go to [railway.app](https://railway.app)
3. **Deploy**: Railway will automatically detect the Python project

#### **Test Deployed API**

Once deployed, you'll get a Railway URL like: `https://your-app-name.railway.app`

```bash
# Test health endpoint
curl -s https://your-app-name.railway.app/health

# Test text checking
curl -X POST "https://your-app-name.railway.app/check" \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjouwr, comment allez-tu?"}'

# Test spelling suggestions
curl -X GET "https://your-app-name.railway.app/suggest/bonjour"

# Test options
curl -X GET "https://your-app-name.railway.app/options"
```

### **3. Automated Testing Script**

Create a test script to verify all endpoints:

```python
#!/usr/bin/env python3
import requests
import json

# Replace with your Railway URL
RAILWAY_URL = "https://your-app-name.railway.app"

def test_health():
    response = requests.get(f"{RAILWAY_URL}/health")
    print(f"Health: {response.status_code}")
    return response.status_code == 200

def test_check_text():
    response = requests.post(
        f"{RAILWAY_URL}/check",
        json={"text": "Bonjouwr, comment allez-tu?"}
    )
    print(f"Check text: {response.status_code}")
    return response.status_code == 200

def test_suggestions():
    response = requests.get(f"{RAILWAY_URL}/suggest/bonjour")
    print(f"Suggestions: {response.status_code}")
    return response.status_code == 200

def test_options():
    response = requests.get(f"{RAILWAY_URL}/options")
    print(f"Options: {response.status_code}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing Railway deployment...")
    tests = [test_health, test_check_text, test_suggestions, test_options]

    for test in tests:
        if not test():
            print("❌ Test failed!")
            exit(1)

    print("✅ All tests passed!")
```

### **4. Common Issues & Solutions**

#### **Issue: Package Installation Fails**

- **Cause**: Missing files referenced in `setup.py`
- **Solution**: ✅ Fixed - Removed script references

#### **Issue: Port Binding**

- **Cause**: Railway uses `PORT` environment variable
- **Solution**: ✅ Fixed - `railway_start.py` uses `os.environ.get("PORT", 8000)`

#### **Issue: Dependencies Missing**

- **Cause**: `requirements.txt` incomplete
- **Solution**: ✅ Fixed - Added `-e .` for local package

### **5. Monitoring Railway Deployment**

#### **Railway Dashboard**

- Check deployment logs in Railway dashboard
- Monitor resource usage
- View environment variables

#### **Health Checks**

```bash
# Test from any machine
curl -s https://your-app-name.railway.app/health
```

### **6. Production Testing Checklist**

- ✅ **Health endpoint**: `/health` returns 200
- ✅ **Text checking**: `/check` processes French text
- ✅ **Spelling suggestions**: `/suggest/{token}` works
- ✅ **Options**: `/options` returns grammar options
- ✅ **Documentation**: `/docs` and `/redoc` accessible
- ✅ **Error handling**: Graceful error responses
- ✅ **Performance**: Response times under 2 seconds

### **7. Troubleshooting**

#### **If Deployment Fails**

1. Check Railway logs for error messages
2. Verify all files are committed to GitHub
3. Ensure `requirements.txt` is correct
4. Test locally with `python3 railway_start.py`

#### **If API Doesn't Work**

1. Check Railway URL is correct
2. Verify environment variables are set
3. Test with simple curl commands
4. Check Railway logs for errors

## 🎉 **Ready for Production!**

Once all tests pass, your Grammalecte API is ready for production use!
