# ⚡ Quick Start — Get Started in 5 Minutes

> Jump right into the lab without reading everything first

---

## 🎯 Goal

Deploy your first AI agent to the cloud in under 30 minutes.

---

## ✅ Prerequisites Check

Run these commands to verify you're ready:

```bash
# Check Python
python --version
# Should be 3.11 or higher

# Check Docker
docker --version
docker compose version

# Check Git
git --version
```

If any command fails, install the missing tool first.

---

## 🚀 Fast Track (30 minutes)

### Step 1: Clone & Setup (2 minutes)

```bash
# Navigate to the project
cd day12_ha-tang-cloud_va_deployment

# Check structure
ls
# Should see: 01-localhost-vs-production, 02-docker, etc.
```

### Step 2: Run Basic Example (3 minutes)

```bash
cd 01-localhost-vs-production/develop
pip install -r requirements.txt
python app.py
```

In another terminal:
```bash
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

**Expected:** You get a response! 🎉

**Stop the server:** Press `Ctrl+C`

### Step 3: Docker Basics (5 minutes)

```bash
cd ../../02-docker/develop

# Build image
docker build -t my-agent .

# Run container
docker run -p 8000:8000 my-agent
```

Test again:
```bash
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```

**Expected:** Same response, but now in a container! 🐳

**Stop:** `Ctrl+C` or `docker stop <container-id>`

### Step 4: Deploy to Cloud (10 minutes)

```bash
cd ../../03-cloud-deployment/railway

# Install Railway CLI
npm i -g @railway/cli

# Login (opens browser)
railway login

# Initialize project
railway init

# Deploy!
railway up

# Get your URL
railway domain
```

**Expected:** You get a public URL like `https://your-agent.railway.app`

Test it:
```bash
curl https://your-agent.railway.app/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Am I on the cloud?"}'
```

**Expected:** Response from the cloud! 🌐

### Step 5: Add Security (10 minutes)

```bash
cd ../../04-api-gateway/develop

# Set API key
export AGENT_API_KEY="my-secret-key"

# Run
python app.py
```

Test without key (should fail):
```bash
curl "http://localhost:8000/ask?question=Hello" -X POST \
  -H "Content-Type: application/json" \
  -d ""
# Expected: 401 Unauthorized
```

Test with key (should work):
```bash
curl "http://localhost:8000/ask?question=Hello" -X POST \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d ""
# Expected: 200 OK
```

---

## 🎓 What You Just Did

1. ✅ Ran an AI agent locally
2. ✅ Containerized it with Docker
3. ✅ Deployed it to the cloud
4. ✅ Added API key authentication

**Congratulations!** You've completed the basics. 🎉

---

## 📚 Next Steps

Now that you've seen it work, go deeper:

### Option A: Follow Full Lab (Recommended)

Read [CODE_LAB.md](CODE_LAB.md) for detailed explanations and exercises.

**Time:** 3-4 hours  
**Outcome:** Deep understanding + production-ready skills

### Option B: Jump to Final Project

Go straight to Part 6 and build from scratch.

```bash
cd 06-lab-complete
cat README.md
```

**Time:** 1-2 hours  
**Outcome:** Working production agent

### Option C: Explore Examples

Browse through each section's `develop/` and `production/` folders.

**Time:** 1 hour  
**Outcome:** See different patterns and approaches

---

## 🆘 Stuck?

### Common Issues

**"Port already in use"**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**"Docker daemon not running"**
```bash
# macOS: Open Docker Desktop app
# Linux: sudo systemctl start docker
```

**"railway: command not found"**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Or with Homebrew (macOS)
brew install railway
```

**"Module not found"**
```bash
# Install dependencies
pip install -r requirements.txt
```

### Get Help

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Search error message on Google
3. Ask instructor or classmates
4. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands

---

## 📖 Documentation Map

```
START HERE
    ↓
QUICK_START.md (you are here)
    ↓
    ├─→ Want full tutorial? → CODE_LAB.md
    ├─→ Need commands? → QUICK_REFERENCE.md
    ├─→ Hit an error? → TROUBLESHOOTING.md
    └─→ Want motivation? → LEARNING_PATH.md
```

---

## 💡 Pro Tips

### Tip 1: Use Multiple Terminals

```
Terminal 1: Run server
Terminal 2: Test with curl
Terminal 3: View logs
```

### Tip 2: Keep Docker Desktop Open

Docker commands won't work if Docker Desktop is closed.

### Tip 3: Save Your Commands

Create a `commands.sh` file with your frequently used commands:

```bash
#!/bin/bash
# My useful commands

# Build and run
alias build="docker build -t my-agent ."
alias run="docker run -p 8000:8000 my-agent"

# Test
alias test="curl http://localhost:8000/health"
```

### Tip 4: Use .env Files

Instead of exporting variables:
```bash
export API_KEY=secret
export PORT=8000
```

Create `.env` file:
```
API_KEY=secret
PORT=8000
```

Then load it:
```bash
source .env
# or
export $(cat .env | xargs)
```

---

## 🎯 Success Checklist

After Quick Start, you should be able to:

- [ ] Run Python app locally
- [ ] Build Docker image
- [ ] Run Docker container
- [ ] Deploy to Railway
- [ ] Access public URL
- [ ] Add API authentication
- [ ] Test with curl

If you checked all boxes, you're ready for the full lab! 🚀

---

## 🏃 Speed Run Challenge

Think you're fast? Try this:

**Challenge:** Deploy a secured agent to the cloud in 15 minutes.

**Rules:**
1. Start from scratch
2. Must have Docker
3. Must have authentication
4. Must have public URL
5. Must work when tested

**Leaderboard:**
- 🥇 < 10 minutes: Deployment Master
- 🥈 10-15 minutes: Speed Demon
- 🥉 15-20 minutes: Quick Learner
- 📚 > 20 minutes: Keep practicing!

---

## 🎓 Learning Modes

Choose your style:

### 🐢 Turtle Mode (Recommended for beginners)
- Read everything carefully
- Do all exercises
- Understand before moving on
- **Time:** 4 hours
- **Retention:** High

### 🐇 Rabbit Mode (For experienced developers)
- Skim documentation
- Run examples
- Jump to final project
- **Time:** 1.5 hours
- **Retention:** Medium

### 🚀 Rocket Mode (For experts)
- Read requirements only
- Build from scratch
- Reference docs when stuck
- **Time:** 1 hour
- **Retention:** High (if you succeed)

---

## 📊 Progress Tracking

Mark your progress:

```
Day 12 Lab Progress
═══════════════════

Quick Start
├─ [✓] Run local agent
├─ [✓] Docker basics
├─ [✓] Deploy to cloud
└─ [✓] Add security

Full Lab
├─ [ ] Part 1: Localhost vs Production
├─ [ ] Part 2: Docker
├─ [ ] Part 3: Cloud Deployment
├─ [ ] Part 4: API Security
├─ [ ] Part 5: Scaling & Reliability
└─ [ ] Part 6: Final Project

Status: 4/10 complete (40%)
```

---

## 🎉 Celebrate Small Wins

- ✅ First successful curl? → You're a tester!
- ✅ First Docker build? → You're a containerizer!
- ✅ First deployment? → You're a cloud engineer!
- ✅ First secured API? → You're a security expert!

Every step counts. Keep going! 💪

---

## 🔗 Quick Links

- **Full Lab:** [CODE_LAB.md](CODE_LAB.md)
- **Commands:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Errors:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Motivation:** [LEARNING_PATH.md](LEARNING_PATH.md)
- **Grading:** [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md) (for instructors)

---

**Ready for more? Open [CODE_LAB.md](CODE_LAB.md) and dive deep! 🏊**
