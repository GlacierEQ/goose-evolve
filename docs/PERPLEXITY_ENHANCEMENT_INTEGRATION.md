# Perplexity Enhancement MCP Integration

## Overview

Goose-Evolve now includes comprehensive monitoring and tracking for the **Perplexity Enhancement MCP Server**.

## Features

### 🧠 Evolution Tracking
- **Intelligence Score Calculation** - Composite metric (0-100)
- **Learning Progress Monitoring** - 30-day timeline
- **Pattern Learning Tracking** - Count and analyze learned patterns
- **Success Rate Trending** - Track improvement over time

### 📊 Performance Monitoring
- **Tool Execution Analytics** - Per-tool and aggregate metrics
- **Response Time Tracking** - Optimize execution speed
- **Token Usage Monitoring** - Track input/output tokens
- **Resource Utilization** - Memory and compute metrics

### ⚖️ Legal Automation Metrics
- **Motion Generation Quality** - Track document compliance
- **Evidence Citation Accuracy** - Monitor citation rates
- **Court Profile Usage** - Analytics per jurisdiction
- **Template Performance** - Identify best templates

## Installation

### 1. Install Goose-Evolve with MCP Support

```bash
git clone https://github.com/GlacierEQ/goose-evolve.git
cd goose-evolve
git checkout feature/perplexity-enhancement-mcp
pip install -r requirements.txt
pip install -e .
```

### 2. Install Perplexity Enhancement MCP

```bash
cd ~/
git clone https://github.com/GlacierEQ/perplexity-enhancement-mcp.git
cd perplexity-enhancement-mcp
npm install && npm run build
```

### 3. Configure Monitoring

```python
from evolution.mcp_enhancement_tracker import MCPEnhancementTracker
from monitoring.mcp_health_monitor import MCPHealthMonitor

# Initialize tracker
tracker = MCPEnhancementTracker()

# Initialize health monitor
monitor = MCPHealthMonitor()
```

## Usage

### Track Tool Executions

```python
from evolution.mcp_enhancement_tracker import MCPEnhancementTracker, MCPToolExecution
from datetime import datetime

tracker = MCPEnhancementTracker()

# Record tool execution
execution = MCPToolExecution(
    timestamp=datetime.now().isoformat(),
    tool_name="generate_legal_motion",
    success=True,
    execution_time_ms=450.0,
    input_tokens=250,
    output_tokens=1500,
    error=None
)

tracker.record_tool_execution(execution)
```

### Generate Evolution Report

```python
tracker = MCPEnhancementTracker()
report = tracker.generate_report()
print(report)
```

**Sample Output:**
```
============================================================
PERPLEXITY ENHANCEMENT MCP EVOLUTION REPORT
============================================================

Generated: 2025-12-03 18:30:00

CURRENT STATE:
  Intelligence Score: 75.5/100
  Success Rate: 96.5%
  Learned Patterns: 12
  Total Tool Calls: 143
  Avg Execution Time: 380ms
  Memory Size: 2.45MB

LEARNING PROGRESS (30 days):
  Intelligence Growth: 15.3 points (25.4%)
  Success Rate Improvement: 8.5%
  Execution Speed Improvement: 120ms faster

============================================================
```

### Monitor Health

```python
from monitoring.mcp_health_monitor import MCPHealthMonitor

monitor = MCPHealthMonitor()
report = monitor.generate_health_report()
print(report)
```

### Get Analytics

```python
tracker = MCPEnhancementTracker()

# Overall analytics
stats = tracker.get_tool_analytics()
print(f"Total Calls: {stats['total_calls']}")
print(f"Success Rate: {stats['success_rate']*100:.1f}%")

# Per-tool analytics
motion_stats = tracker.get_tool_analytics("generate_legal_motion")
print(f"Legal Motions Generated: {motion_stats['total_calls']}")
```

### Track Learning Progress

```python
tracker = MCPEnhancementTracker()
progress = tracker.get_learning_progress()

if progress['status'] == 'learning':
    growth = progress['intelligence_growth']
    print(f"Intelligence improved by {growth['improvement']:.1f} points")
    print(f"Growth rate: {growth['growth_rate']:.1f}%")
```

## Intelligence Score Calculation

The intelligence score (0-100) is calculated from:

### Success Rate (40 points)
- 100% success = 40 points
- 50% success = 20 points

### Patterns Learned (30 points)
- 0 patterns = 0 points
- 10+ patterns = 30 points
- Linear scaling between

### Execution Speed (30 points)
- Faster execution = higher score
- Baseline: 1000ms
- Optimizes over time

**Example:**
- Success Rate: 95% → 38 points
- Patterns: 12 → 30 points (capped)
- Speed: 400ms → 24 points
- **Total: 92/100**

## Evolution Timeline

```python
tracker = MCPEnhancementTracker()
timeline = tracker.get_evolution_timeline(days=30)

for snapshot in timeline:
    print(f"{snapshot.timestamp}: Intelligence={snapshot.intelligence_score:.1f}")
```

## Integration with Goose

When Goose uses MCP tools, automatically track:

```python
# In your Goose workflow
from evolution.mcp_enhancement_tracker import MCPEnhancementTracker, MCPToolExecution

tracker = MCPEnhancementTracker()

def track_mcp_call(tool_name, success, execution_time, tokens_in, tokens_out):
    execution = MCPToolExecution(
        timestamp=datetime.now().isoformat(),
        tool_name=tool_name,
        success=success,
        execution_time_ms=execution_time,
        input_tokens=tokens_in,
        output_tokens=tokens_out
    )
    tracker.record_tool_execution(execution)
```

## Continuous Monitoring

Set up continuous monitoring:

```python
import time
from monitoring.mcp_health_monitor import MCPHealthMonitor

monitor = MCPHealthMonitor()

while True:
    health = monitor.check_health()
    if health.status != 'healthy':
        print(f"⚠️  MCP Server Status: {health.status}")
        # Send alert
    
    time.sleep(60)  # Check every minute
```

## Database Schema

Goose-Evolve stores evolution data in SQLite:

### tool_executions
- timestamp
- tool_name
- success
- execution_time_ms
- input_tokens
- output_tokens
- error

### learning_metrics
- timestamp
- metric_type
- success_rate
- avg_execution_time
- total_executions
- patterns_learned

### evolution_snapshots
- timestamp
- total_tool_calls
- success_rate
- learned_patterns
- avg_execution_time
- memory_size_mb
- intelligence_score

## API Reference

### MCPEnhancementTracker

**Methods:**
- `record_tool_execution(execution)` - Record MCP tool call
- `record_learning_metric(metric)` - Record learning metric
- `create_evolution_snapshot()` - Create state snapshot
- `get_evolution_timeline(days)` - Get timeline
- `get_tool_analytics(tool_name)` - Get analytics
- `get_learning_progress()` - Get progress summary
- `generate_report()` - Generate full report

### MCPHealthMonitor

**Methods:**
- `check_health()` - Perform health check
- `generate_health_report()` - Generate report

## Future Enhancements

- [ ] Real-time dashboard
- [ ] Slack/Email alerts
- [ ] Grafana integration
- [ ] A/B testing framework
- [ ] Automated optimization recommendations

## Learn More

- [Perplexity Enhancement MCP](https://github.com/GlacierEQ/perplexity-enhancement-mcp)
- [Goose Documentation](https://block.github.io/goose)
- [MCP Protocol](https://modelcontextprotocol.io)

---

**Track, monitor, and optimize your AI enhancement capabilities with Goose-Evolve.**
