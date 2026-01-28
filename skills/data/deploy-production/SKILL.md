---
name: deploy-production
description: "Deploy to production. Use when: Releasing code to production environments with safety checks. Not for: Staging deploys or local builds (unless specifically requested)."
disable-model-invocation: true
user-invocable: true
context: fork
agent: Plan
allowed-tools: Read, Bash(docker:*), Bash(kubectl:*)
---

# Deploy to Production

Deploy application to production with comprehensive safety checks.

⚠️ **DANGER ZONE** - Production Deployment

## Pre-Deployment Checklist

**CRITICAL SAFETY CHECK**: Verify ALL requirements BEFORE proceeding:

- [ ] All tests pass locally (`npm test`)
- [ ] Recent commits are reviewed and approved
- [ ] Database migrations are tested
- [ ] Backups are current and tested
- [ ] Deployment plan documented
- [ ] Rollback plan prepared
- [ ] Monitoring configured
- [ ] Team notified of deployment window

**DO NOT PROCEED** unless ALL items are verified.

## Deployment Process

<logic_flow>
digraph Deployment {
    rankdir=TD;
    node [shape=box];
    Verify [label="1. Verify Checklist"];
    Build [label="2. Build & Test"];
    Docker [label="3. Build Docker"];
    Push [label="4. Push Registry"];
    Deploy [label="5. Apply K8s"];
    Check [label="6. Verify Health"];
    Success [label="Deployment Success" style=filled fillcolor=lightgreen];
    Rollback [label="Rollback Procedure" style=filled fillcolor=lightpink];

    Verify -> Build;
    Build -> Docker;
    Docker -> Push;
    Push -> Deploy;
    Deploy -> Check;
    Check -> Success [label="Health OK"];
    Check -> Rollback [label="Errors"];
    Rollback -> Verify [label="Fix & Retry"];
}
</logic_flow>

### 1. Pre-Deployment Verification
Complete the checklist above and verify all systems are ready.

### 2. Build Application
```bash
npm run build
npm test
```

### 3. Build Docker Image
```bash
docker build -t myapp:$VERSION .
docker tag myapp:$VERSION myapp:latest
```

### 4. Push to Registry
```bash
docker push myapp:$VERSION
docker push myapp:latest
```

### 5. Deploy to Kubernetes
```bash
kubectl apply -f manifests/production/
kubectl rollout status deployment/myapp
```

### 6. Verify Deployment
- [ ] Health checks passing
- [ ] Logs show no errors
- [ ] Metrics within normal range
- [ ] Smoke tests pass

### 7. Post-Deployment
- [ ] Update documentation
- [ ] Notify team of successful deployment
- [ ] Monitor for 30 minutes
- [ ] Update deployment tracker

## Safety Features

This skill includes:
- **Manual-only invocation** - Cannot be auto-triggered
- **Pre-deployment checklist** - Must verify all safety items
- **Rollback capability** - Can revert if issues detected
- **Verification steps** - Ensures deployment success

## Rollback Procedure

If deployment fails:

1. **Revert to previous version**:
   ```bash
   kubectl rollout undo deployment/myapp
   ```

2. **Verify rollback**:
   ```bash
   kubectl rollout status deployment/myapp
   ```

3. **Investigate issues**:
   - Check logs
   - Review metrics
   - Identify root cause

4. **Fix and re-deploy** after resolution

## Integration

This skill integrates with:
- `ci-pipeline-manager` - CI/CD pipeline integration
- `backend-patterns` - Deployment best practices
