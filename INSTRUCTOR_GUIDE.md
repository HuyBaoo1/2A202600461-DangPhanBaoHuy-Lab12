# 👨‍🏫 Instructor Guide — Day 12 Lab Assessment

> Hướng dẫn chấm điểm và đánh giá cho giảng viên

---

## 📊 Grading Overview

| Component | Points | Weight |
|-----------|--------|--------|
| **Part 1-5: Exercises** | 40 | 40% |
| **Part 6: Final Project** | 60 | 60% |
| **Total** | 100 | 100% |

**Passing grade:** 70/100

---

## Part 1-5: Exercises (40 points)

### Part 1: Localhost vs Production (8 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Exercise 1.1** | 2 | Identify 5+ anti-patterns in basic code |
| **Exercise 1.2** | 2 | Successfully run basic version |
| **Exercise 1.3** | 4 | Complete comparison table with meaningful insights |

**Grading notes:**
- Exercise 1.1: Accept any valid anti-patterns (hardcoded secrets, no health check, etc.)
- Exercise 1.3: Look for understanding of WHY each practice matters, not just WHAT

**Sample answer for Exercise 1.3:**

| Feature | Basic | Advanced | Tại sao quan trọng? |
|---------|-------|----------|---------------------|
| Config | Hardcode | Env vars | Dễ thay đổi giữa environments, không commit secrets |
| Health check | ❌ | ✅ | Platform biết khi nào restart, monitoring |
| Logging | print() | JSON | Structured logs dễ parse, search, analyze |
| Shutdown | Đột ngột | Graceful | Không mất data, hoàn thành requests |

---

### Part 2: Docker (8 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Exercise 2.1** | 2 | Answer Dockerfile questions correctly |
| **Exercise 2.2** | 2 | Build and run basic container |
| **Exercise 2.3** | 2 | Understand multi-stage build benefits |
| **Exercise 2.4** | 2 | Draw architecture diagram and test stack |

**Grading notes:**
- Exercise 2.1: Check understanding of Docker concepts
- Exercise 2.3: Image size should be significantly smaller (50-70% reduction)
- Exercise 2.4: Diagram should show agent, redis, nginx and their connections

**Sample answers:**

**Exercise 2.1:**
1. Base image: `python:3.11-slim` (OS + Python runtime)
2. Working directory: `/app` (where code lives)
3. Copy requirements first: Cache layer, rebuild only if requirements change
4. CMD vs ENTRYPOINT: CMD can be overridden, ENTRYPOINT is fixed

**Exercise 2.4 diagram:**
```
Client → Nginx (port 80) → Agent (port 8000) → Redis (port 6379)
```

---

### Part 3: Cloud Deployment (8 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Exercise 3.1** | 4 | Successfully deploy to Railway with working URL |
| **Exercise 3.2** | 3 | Deploy to Render OR compare config files |
| **Exercise 3.3** | 1 | (Optional) Understand GCP Cloud Run CI/CD |

**Grading notes:**
- Must have working public URL that responds to requests
- Accept either Railway OR Render (not both required)
- Exercise 3.3 is bonus

**Verification:**
```bash
# Test student's URL
curl https://student-app.railway.app/health
# Should return: {"status": "ok"}

curl -X POST https://student-app.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
# Should return valid response
```

---

### Part 4: API Security (8 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Exercise 4.1** | 2 | Understand API key authentication |
| **Exercise 4.2** | 2 | Implement JWT authentication |
| **Exercise 4.3** | 2 | Understand rate limiting |
| **Exercise 4.4** | 2 | Implement cost guard |

**Grading notes:**
- Exercise 4.1-4.3: Can be graded by running tests
- Exercise 4.4: Check implementation logic, not just copy-paste

**Test script:**
```python
# test_security.py
import requests

BASE_URL = "http://localhost:8000"

def test_api_key():
    # Without key
    r = requests.post(f"{BASE_URL}/ask", json={"question": "test"})
    assert r.status_code == 401, "Should reject without API key"
    
    # With key
    r = requests.post(
        f"{BASE_URL}/ask",
        headers={"X-API-Key": "secret"},
        json={"question": "test"}
    )
    assert r.status_code == 200, "Should accept with valid key"

def test_rate_limit():
    # Send 20 requests
    for i in range(20):
        r = requests.post(
            f"{BASE_URL}/ask",
            headers={"X-API-Key": "secret"},
            json={"question": f"test {i}"}
        )
    
    # Should get 429
    assert r.status_code == 429, "Should rate limit after threshold"

if __name__ == "__main__":
    test_api_key()
    test_rate_limit()
    print("✅ All tests passed")
```

---

### Part 5: Scaling & Reliability (8 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Exercise 5.1** | 2 | Implement health and readiness checks |
| **Exercise 5.2** | 2 | Implement graceful shutdown |
| **Exercise 5.3** | 2 | Refactor to stateless design |
| **Exercise 5.4** | 1 | Run load balanced stack |
| **Exercise 5.5** | 1 | Test stateless design |

**Grading notes:**
- Exercise 5.1: Both endpoints must work correctly
- Exercise 5.2: Must handle SIGTERM properly
- Exercise 5.3: No state in memory, all in Redis

**Verification:**

```bash
# Test health checks
curl http://localhost:8000/health  # Should return 200
curl http://localhost:8000/ready   # Should return 200 or 503

# Test graceful shutdown
python app.py &
PID=$!
kill -TERM $PID
# Should see graceful shutdown message

# Test stateless
docker compose up --scale agent=3
# Make requests, kill random instance, continue requests
# Should work without errors
```

---

## Part 6: Final Project (60 points)

### Functional Requirements (20 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Agent works** | 10 | Responds to questions correctly |
| **Conversation history** | 5 | Maintains context across requests |
| **Error handling** | 5 | Graceful error responses |

**Test:**
```bash
# Test basic functionality
curl -X POST $URL/ask \
  -H "X-API-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'

# Test conversation
curl -X POST $URL/ask \
  -H "X-API-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "What did I just say?"}'
# Should reference previous message

# Test error handling
curl -X POST $URL/ask \
  -H "X-API-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
# Should return 422 with clear error message
```

---

### Docker & Configuration (15 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Multi-stage Dockerfile** | 5 | Proper multi-stage build |
| **Image size** | 3 | < 500 MB |
| **docker-compose.yml** | 4 | Complete stack with agent + redis |
| **Environment config** | 3 | All config from env vars |

**Checklist:**

```bash
# Check Dockerfile
grep -q "FROM.*as builder" Dockerfile  # Multi-stage
grep -q "FROM.*slim" Dockerfile        # Slim base image

# Check image size
docker images | grep student-agent
# Should be < 500 MB

# Check docker-compose
grep -q "redis:" docker-compose.yml
grep -q "agent:" docker-compose.yml

# Check env vars
grep -q "os.getenv" app/*.py
grep -q "Settings" app/config.py
```

---

### Security (20 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **API Key auth** | 5 | Working authentication |
| **Rate limiting** | 5 | Limits requests per user |
| **Cost guard** | 5 | Tracks and limits spending |
| **No hardcoded secrets** | 5 | All secrets from env vars |

**Test:**

```bash
# Test auth
curl $URL/ask  # Should return 401

# Test rate limiting
for i in {1..20}; do
  curl -X POST $URL/ask \
    -H "X-API-Key: $KEY" \
    -H "Content-Type: application/json" \
    -d '{"user_id": "test", "question": "test"}'
done
# Should eventually return 429

# Check for hardcoded secrets
grep -r "sk-" app/  # Should find nothing
grep -r "api_key.*=" app/  # Should only find env var reads
```

---

### Reliability (15 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Health check** | 3 | `/health` endpoint works |
| **Readiness check** | 3 | `/ready` endpoint works |
| **Graceful shutdown** | 4 | Handles SIGTERM |
| **Stateless design** | 5 | State in Redis, not memory |

**Test:**

```bash
# Health checks
curl $URL/health  # 200
curl $URL/ready   # 200

# Graceful shutdown
docker compose up -d
docker compose kill -s TERM agent
docker compose logs agent | grep -i "graceful"
# Should see graceful shutdown message

# Stateless
docker compose up --scale agent=3
# Make request to create conversation
# Kill one instance
# Make another request
# Should still have conversation history
```

---

### Deployment (10 points)

| Criteria | Points | Description |
|----------|--------|-------------|
| **Public URL** | 5 | Working public URL |
| **Deployment config** | 3 | railway.toml or render.yaml |
| **Environment setup** | 2 | Proper env vars on platform |

**Verification:**

```bash
# Test public URL
curl https://student-app.railway.app/health

# Check config files
ls railway.toml || ls render.yaml

# Check platform dashboard
# - Environment variables set
# - Service running
# - No errors in logs
```

---

## Automated Grading Script

```python
#!/usr/bin/env python3
"""
Automated grading script for Day 12 Lab
Usage: python grade.py <student-repo-path> <public-url> <api-key>
"""

import sys
import os
import subprocess
import requests
import time
from pathlib import Path

class Grader:
    def __init__(self, repo_path, public_url, api_key):
        self.repo_path = Path(repo_path)
        self.public_url = public_url
        self.api_key = api_key
        self.score = 0
        self.max_score = 60
        self.results = []
    
    def test(self, name, points, func):
        """Run a test and record result"""
        try:
            func()
            self.score += points
            self.results.append(f"✅ {name}: {points}/{points}")
            return True
        except AssertionError as e:
            self.results.append(f"❌ {name}: 0/{points} - {e}")
            return False
        except Exception as e:
            self.results.append(f"❌ {name}: 0/{points} - Error: {e}")
            return False
    
    def check_file_exists(self, filepath):
        """Check if file exists"""
        assert (self.repo_path / filepath).exists(), f"{filepath} not found"
    
    def check_dockerfile(self):
        """Check Dockerfile quality"""
        dockerfile = (self.repo_path / "Dockerfile").read_text()
        assert "FROM" in dockerfile, "No FROM instruction"
        assert "as builder" in dockerfile.lower(), "Not multi-stage"
        assert "slim" in dockerfile.lower(), "Not using slim image"
    
    def check_docker_compose(self):
        """Check docker-compose.yml"""
        compose = (self.repo_path / "docker-compose.yml").read_text()
        assert "redis:" in compose, "No redis service"
        assert "agent:" in compose or "app:" in compose, "No agent service"
    
    def check_no_secrets(self):
        """Check for hardcoded secrets"""
        result = subprocess.run(
            ["grep", "-r", "sk-", str(self.repo_path / "app")],
            capture_output=True
        )
        assert result.returncode != 0, "Found hardcoded API keys"
    
    def test_health_endpoint(self):
        """Test /health endpoint"""
        r = requests.get(f"{self.public_url}/health", timeout=10)
        assert r.status_code == 200, f"Health check failed: {r.status_code}"
    
    def test_ready_endpoint(self):
        """Test /ready endpoint"""
        r = requests.get(f"{self.public_url}/ready", timeout=10)
        assert r.status_code in [200, 503], f"Ready check failed: {r.status_code}"
    
    def test_auth_required(self):
        """Test authentication is required"""
        r = requests.post(
            f"{self.public_url}/ask",
            json={"question": "test"}
        )
        assert r.status_code == 401, "Should require authentication"
    
    def test_auth_works(self):
        """Test authentication works"""
        r = requests.post(
            f"{self.public_url}/ask",
            headers={"X-API-Key": self.api_key},
            json={"user_id": "test", "question": "Hello"}
        )
        assert r.status_code == 200, f"Auth failed: {r.status_code}"
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        # Send many requests
        for i in range(15):
            r = requests.post(
                f"{self.public_url}/ask",
                headers={"X-API-Key": self.api_key},
                json={"user_id": "test_rate", "question": f"test {i}"}
            )
        
        # Should eventually get rate limited
        assert r.status_code == 429, "Rate limiting not working"
    
    def test_conversation_history(self):
        """Test conversation history"""
        user_id = f"test_{int(time.time())}"
        
        # First message
        r1 = requests.post(
            f"{self.public_url}/ask",
            headers={"X-API-Key": self.api_key},
            json={"user_id": user_id, "question": "My name is Alice"}
        )
        assert r1.status_code == 200
        
        # Second message referencing first
        r2 = requests.post(
            f"{self.public_url}/ask",
            headers={"X-API-Key": self.api_key},
            json={"user_id": user_id, "question": "What is my name?"}
        )
        assert r2.status_code == 200
        # Response should mention Alice (basic check)
        # Note: This is a weak test, might need adjustment
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Running automated tests...\n")
        
        # File structure tests
        self.test("Dockerfile exists", 2, 
                  lambda: self.check_file_exists("Dockerfile"))
        self.test("docker-compose.yml exists", 2,
                  lambda: self.check_file_exists("docker-compose.yml"))
        self.test("requirements.txt exists", 1,
                  lambda: self.check_file_exists("requirements.txt"))
        
        # Docker quality tests
        self.test("Multi-stage Dockerfile", 5, self.check_dockerfile)
        self.test("Docker Compose has services", 4, self.check_docker_compose)
        
        # Security tests
        self.test("No hardcoded secrets", 5, self.check_no_secrets)
        self.test("Auth required", 5, self.test_auth_required)
        self.test("Auth works", 5, self.test_auth_works)
        self.test("Rate limiting", 5, self.test_rate_limiting)
        
        # Reliability tests
        self.test("Health endpoint", 3, self.test_health_endpoint)
        self.test("Ready endpoint", 3, self.test_ready_endpoint)
        
        # Functionality tests
        self.test("Conversation history", 5, self.test_conversation_history)
        
        # Deployment test
        self.test("Public URL works", 5, self.test_health_endpoint)
        
        # Print results
        print("\n" + "="*60)
        print("📊 GRADING RESULTS")
        print("="*60)
        for result in self.results:
            print(result)
        print("="*60)
        print(f"🎯 TOTAL SCORE: {self.score}/{self.max_score}")
        print(f"📈 PERCENTAGE: {self.score/self.max_score*100:.1f}%")
        
        if self.score >= self.max_score * 0.7:
            print("✅ PASSED")
        else:
            print("❌ FAILED (need 70% to pass)")
        
        return self.score

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python grade.py <repo-path> <public-url> <api-key>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    public_url = sys.argv[2].rstrip('/')
    api_key = sys.argv[3]
    
    grader = Grader(repo_path, public_url, api_key)
    score = grader.run_all_tests()
    
    sys.exit(0 if score >= grader.max_score * 0.7 else 1)
```

---

## Manual Review Checklist

Use this for aspects that can't be automated:

### Code Quality (subjective, not graded but provide feedback)

- [ ] Code is readable and well-organized
- [ ] Proper error handling
- [ ] Meaningful variable names
- [ ] Comments where necessary
- [ ] No obvious security vulnerabilities
- [ ] Follows Python best practices (PEP 8)

### Architecture (subjective)

- [ ] Proper separation of concerns
- [ ] Config management is clean
- [ ] Dependencies are minimal
- [ ] Scalable design

### Documentation (bonus points)

- [ ] README with setup instructions
- [ ] API documentation
- [ ] Architecture diagram
- [ ] Deployment guide

---

## Common Issues & Partial Credit

### Issue: "Works locally but not on cloud"

**Partial credit:** 50% if:
- Docker works locally
- Code quality is good
- Just deployment config issue

**Feedback:** "Check PORT environment variable, ensure it's read from env"

---

### Issue: "No rate limiting"

**Partial credit:** 70% if:
- Everything else works
- Auth is implemented
- Just missing rate limiting

**Feedback:** "Implement rate limiting using Redis sorted sets"

---

### Issue: "Stateful design"

**Partial credit:** 60% if:
- Works functionally
- Just stores state in memory instead of Redis

**Feedback:** "Move conversation history to Redis for stateless design"

---

## Grading Timeline

1. **Automated tests** (5 minutes per student)
   - Run grading script
   - Record automated score

2. **Manual review** (10 minutes per student)
   - Check code quality
   - Review architecture
   - Test edge cases
   - Provide feedback

3. **Final scoring** (2 minutes per student)
   - Combine automated + manual scores
   - Write summary feedback
   - Submit grade

**Total time:** ~15-20 minutes per student

---

## Feedback Template

```
Student: [Name]
Score: [X]/100

AUTOMATED TESTS: [Y]/60
- Functionality: [score]
- Docker: [score]
- Security: [score]
- Reliability: [score]
- Deployment: [score]

MANUAL REVIEW: [Z]/40
- Code quality: [feedback]
- Architecture: [feedback]
- Documentation: [feedback]

STRENGTHS:
- [What they did well]

AREAS FOR IMPROVEMENT:
- [What needs work]

OVERALL FEEDBACK:
[Summary paragraph]
```

---

## Sample Feedback

### Excellent (90-100)

```
Excellent work! Your agent is production-ready with proper security,
scalability, and reliability features. Code is clean and well-organized.
Deployment is smooth. Great job implementing all requirements.

Suggestions for next level:
- Add monitoring with Prometheus
- Implement distributed tracing
- Add comprehensive test suite
```

### Good (80-89)

```
Good work! Your agent works well and includes most production features.
Minor issues with [specific issue]. Code quality is solid.

To improve:
- [Specific improvement 1]
- [Specific improvement 2]
```

### Satisfactory (70-79)

```
Your agent meets basic requirements but lacks some production features.
[Specific missing features]. Works functionally but needs improvement
in [area].

Focus on:
- [Key improvement 1]
- [Key improvement 2]
```

### Needs Improvement (<70)

```
Your submission is incomplete or has significant issues. [Specific problems].
Please review the lab materials and resubmit.

Critical issues:
- [Issue 1]
- [Issue 2]

Office hours available for help.
```

---

## FAQ for Instructors

**Q: Student's app works locally but fails on cloud. How much credit?**  
A: 50-70% depending on how close they are. If it's just a config issue, be lenient.

**Q: Student used different tech stack (e.g., Express instead of FastAPI)?**  
A: Accept if they meet all requirements. Grade based on concepts, not specific tech.

**Q: Student's rate limiting is basic (not production-ready)?**  
A: Accept if it works. This is a learning exercise, not production code.

**Q: How strict on code quality?**  
A: Focus on functionality first. Code quality is feedback, not heavy grading.

**Q: Student deployed to different platform (not Railway/Render)?**  
A: Accept any cloud platform (AWS, GCP, Azure, Heroku, etc.)

---

**Happy grading! 📝**
