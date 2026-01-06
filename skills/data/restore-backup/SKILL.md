---
name: restore-backup
description: Restores applications and data from Velero backups with proper configuration, validation, and verification.
---

# Restore from OADP/Velero Backup

This skill helps you restore applications and data from existing backups with proper configuration and validation.

## When to Use This Skill

- Recovering from accidental deletion
- Migrating applications to new clusters
- Cloning applications to different namespaces
- Disaster recovery scenarios
- Testing backup validity

## What This Skill Does

1. **Validates Backup**: Ensures backup exists and is complete
2. **Plans Restore**: Determines restore strategy
3. **Prepares Environment**: Checks for conflicts
4. **Executes Restore**: Creates restore resource
5. **Monitors Progress**: Watches restore completion
6. **Verifies**: Confirms application restored correctly

## How to Use

```
Restore backup myapp-backup-20240315
```

```
Restore backup myapp-backup to namespace myapp-dev
```

```
Restore only PVCs from backup myapp-backup
```

## Examples

### Example 1: Simple Restore

**User**: "Restore backup wordpress-backup-20240315"

**Actions**:
1. Verify backup exists and is complete
2. Check if namespace exists
3. Create restore
4. Monitor completion
5. Verify application

```bash
# Verify backup
velero backup get wordpress-backup-20240315

# Create restore
velero restore create wordpress-restore-20240315 \
  --from-backup wordpress-backup-20240315 \
  --wait

# Verify
oc get all -n wordpress
```

### Example 2: Cross-Namespace Restore

**User**: "Restore backup prod-app to namespace dev-app"

```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: prod-to-dev-restore
  namespace: openshift-adp
spec:
  backupName: prod-app-backup
  namespaceMapping:
    prod-app: dev-app
  restorePVs: true
```

### Example 3: Partial Restore

**User**: "Restore only deployments and services from backup myapp"

```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: partial-restore
  namespace: openshift-adp
spec:
  backupName: myapp-backup
  includedResources:
    - deployments
    - services
  excludedResources:
    - secrets
    - configmaps
```

### Example 4: Selective Restore

**User**: "Restore only resources with label app=frontend"

```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: frontend-restore
  namespace: openshift-adp
spec:
  backupName: full-backup
  labelSelector:
    matchLabels:
      app: frontend
```

### Example 5: Velero Built-in Data Mover Restore (Cross-Region)

**User**: "Restore backup with Velero's built-in Data Mover from different region"

**Note**: Data Mover is now built-in to Velero and handles volume data migration natively.

**Actions**:

1. Verify target BSL configured:
   ```bash
   oc get backupstoragelocations -n openshift-adp
   ```

2. Create restore with Data Mover:
   ```yaml
   apiVersion: velero.io/v1
   kind: Restore
   metadata:
     name: datamover-restore-20240315
     namespace: openshift-adp
     annotations:
       oadp.openshift.io/target-bsl: secondary-bsl  # BSL in target region
   spec:
     backupName: app-datamover-backup-20240315
     includedNamespaces:
       - myapp
     restorePVs: true
   ```

3. Monitor Data Mover restore:
   ```bash
   # Watch Velero Data Mover operations
   oc get datadownloads -A -w

   # Check PVCs being created
   oc get pvc -n myapp -w

   # Monitor Velero logs for data mover activity
   oc logs -n openshift-adp deployment/velero -f | grep -i datamover
   ```

**Expected Behavior:**
- Velero's built-in Data Mover creates DataDownload CRs for each PVC
- Empty PVCs created first
- Data transferred from Kopia backup repository to PVCs (or Restic for OADP 1.3)
- Application pods start after PVCs populated

### Example 6: Cross-BSL/Cross-Region Restore

**User**: "Restore from backup in different region/BSL"

**Actions**:

1. Sync backups from source BSL:
   ```bash
   # Velero automatically syncs backups from all BSLs
   velero backup get

   # Verify backup from secondary BSL is visible
   velero backup describe offsite-backup-20240315 | grep "Storage Location"
   ```

2. Create restore with BSL mapping:
   ```yaml
   apiVersion: velero.io/v1
   kind: Restore
   metadata:
     name: cross-region-restore
     namespace: openshift-adp
     annotations:
       oadp.openshift.io/source-bsl: secondary-bsl  # Backup from this BSL
       oadp.openshift.io/target-region: us-east-1  # Target region
       oadp.openshift.io/target-storage-class: gp3  # Storage class in target region
   spec:
     backupName: offsite-backup-20240315
     includedNamespaces:
       - critical-app
     restorePVs: true
     volumeSnapshotLocations:
       - aws-us-east-1-vsl  # VSL in target region
   ```

3. Handle cross-region volume snapshots:
   ```bash
   # For snapshot-based backups, Data Mover may be required
   # Or manually copy snapshots between regions using cloud provider tools

   # Check if snapshots need to be copied
   velero backup describe offsite-backup-20240315 --details | grep VolumeSnapshot
   ```

**Use Cases:**
- Disaster recovery to different region
- Migration between clusters in different regions
- Testing restore in alternate location

### Example 7: OpenShift Virtualization VM Restore

**User**: "Restore VirtualMachine from backup"

**Actions**:

1. Verify VM backup:
   ```bash
   velero backup describe vm-backup-20240315 --details
   ```

2. Create VM restore:
   ```yaml
   apiVersion: velero.io/v1
   kind: Restore
   metadata:
     name: vm-restore-20240315
     namespace: openshift-adp
     annotations:
       oadp.openshift.io/target-storage-class: ocs-storagecluster-ceph-rbd  # Target storage class
   spec:
     backupName: vm-backup-20240315
     includedNamespaces:
       - vm-namespace
     includedResources:
       - virtualmachines.kubevirt.io
       - virtualmachineinstances.kubevirt.io
       - datavolumes.cdi.kubevirt.io
       - persistentvolumeclaims
       - volumesnapshots.snapshot.storage.k8s.io
     restorePVs: true
   ```

3. Verify VM restore:
   ```bash
   # Check VM restored
   oc get vms -n vm-namespace

   # Check DataVolumes
   oc get datavolumes -n vm-namespace

   # Check PVCs bound
   oc get pvc -n vm-namespace

   # Check VM status
   virtctl status vm-name -n vm-namespace
   ```

4. Start VM if needed:
   ```bash
   # VMs are restored in stopped state by default
   virtctl start vm-name -n vm-namespace
   ```

**Success Indicators:**
- VirtualMachine CR restored
- DataVolumes recreated
- PVCs bound and populated
- VM can be started successfully

**Post-Restore Actions:**
- Verify VM disk integrity
- Check VM network configuration
- Test VM functionality
- Update any cluster-specific settings

### Example 8: etcd Restore Reference

**Note**: etcd restore is a cluster-level disaster recovery operation performed separately from OADP application restores.

**etcd Restore (Manual Process)**:

```bash
# On each master node - restore etcd from snapshot
oc debug node/master-0
chroot /host

# Stop static pods
sudo mv /etc/kubernetes/manifests /etc/kubernetes/manifests.backup

# Restore etcd snapshot
sudo -E /usr/local/bin/cluster-restore.sh /path/to/etcd-snapshot

# Restart services
sudo systemctl restart kubelet.service
sudo systemctl restart crio.service

# Restore static pods
sudo mv /etc/kubernetes/manifests.backup /etc/kubernetes/manifests

exit
```

**Force etcd Redeployment**:
```bash
# After restoring on all masters
oc patch etcd cluster -p='{"spec": {"forceRedeploymentReason": "recovery-'"$(date --rfc-3339=ns)"'"}}' --type=merge
```

**Restore OADP Backup of etcd Resources** (Optional):

After etcd data is restored, restore etcd-related resources:

```bash
# Restore etcd namespace resources
velero restore create etcd-resources-restore \
  --from-backup etcd-resources-backup \
  --include-namespaces openshift-etcd
```

**Important Notes:**
- etcd restore is destructive - only use as last resort
- Follow official OpenShift disaster recovery documentation
- Test etcd restore procedure in non-production first
- Ensure all master nodes are processed
- Cluster may be unavailable during etcd restore

**Integration with OADP:**
1. Use OADP for application-level backups
2. Use etcd snapshots for control plane disaster recovery
3. Combine both for complete cluster recovery capability

## Restore Strategies

### 1. In-Place Restore
Restore to original namespace (requires deletion first)

```bash
# Delete namespace
oc delete namespace myapp

# Restore
velero restore create myapp-restore \
  --from-backup myapp-backup \
  --wait
```

### 2. Cross-Namespace Restore
Restore to different namespace

```bash
# Create target namespace
oc create namespace myapp-dev

# Restore with mapping
velero restore create myapp-clone \
  --from-backup myapp-backup \
  --namespace-mappings myapp:myapp-dev \
  --wait
```

### 3. Cross-Cluster Restore
Restore to different cluster

```bash
# On target cluster with same BSL configured
velero restore create cross-cluster-restore \
  --from-backup myapp-backup \
  --wait
```

### 4. Partial Restore
Restore specific resources

```bash
# Restore only PVCs
velero restore create pvc-only-restore \
  --from-backup myapp-backup \
  --include-resources persistentvolumeclaims \
  --wait
```

## Handling Conflicts

### Existing Resources

**Strategy 1: Delete first**
```bash
oc delete namespace myapp
velero restore create --from-backup myapp-backup
```

**Strategy 2: Update existing**
```bash
velero restore create myapp-restore \
  --from-backup myapp-backup \
  --existing-resource-policy=update
```

**Strategy 3: Skip existing**
```bash
# Default behavior - skip existing resources
velero restore create --from-backup myapp-backup
```

### PVC Binding Issues

```bash
# Map storage classes
velero restore create myapp-restore \
  --from-backup myapp-backup \
  --storage-class-mappings old-sc:new-sc
```

## Restore with Hooks

### Post-Restore Hooks

```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: db-restore-with-hooks
  namespace: openshift-adp
spec:
  backupName: database-backup
  hooks:
    resources:
      - name: db-post-restore
        includedNamespaces:
          - database
        labelSelector:
          matchLabels:
            app: postgres
        postHooks:
          - exec:
              container: postgres
              command:
                - /bin/bash
                - -c
                - |
                  # Wait for DB ready
                  until pg_isready; do sleep 1; done
                  # Run migrations
                  psql -U postgres -d mydb -f /migrations/latest.sql
              execTimeout: 5m
              waitTimeout: 10m
```

## Monitoring Restore

### Real-time Monitoring

```bash
# Watch restore status
watch "oc get restore myapp-restore -n openshift-adp"

# Stream logs
velero restore logs myapp-restore -f

# Detailed status
velero restore describe myapp-restore --details
```

### Checking Progress

```bash
# Get restore status
velero restore get

# Check resource creation
oc get all -n myapp --watch

# Check PVC binding
oc get pvc -n myapp --watch

# Check pod status
oc get pods -n myapp --watch
```

## Verification

### Post-Restore Checklist

```bash
# 1. Check restore completed
velero restore describe myapp-restore | grep "Phase:"

# 2. Verify all pods running
oc get pods -n myapp

# 3. Verify PVCs bound
oc get pvc -n myapp

# 4. Check services
oc get svc -n myapp

# 5. Test application
curl http://myapp-route.example.com

# 6. Verify data integrity
oc exec -n myapp deployment/myapp -- /check-data.sh
```

### Comparing Backup vs Restore

```bash
# Resources in backup
velero backup describe myapp-backup --details | \
  grep "Resource List" -A 100

# Resources after restore
oc api-resources --verbs=list --namespaced -o name | \
  xargs -n 1 oc get --show-kind --ignore-not-found -n myapp
```

## Troubleshooting

### Restore Stuck

```bash
# Check restore logs
velero restore logs myapp-restore

# Check for errors
velero restore describe myapp-restore | grep -i error

# Check Velero logs
oc logs -n openshift-adp deployment/velero
```

### PVCs Not Binding

```bash
# Check VolumeSnapshots
oc get volumesnapshots -n myapp

# Check storage class
oc get storageclass

# Describe PVC
oc describe pvc <pvc-name> -n myapp

# Check for events
oc get events -n myapp --sort-by='.lastTimestamp'
```

### Partial Restore

```bash
# Check what was restored
velero restore describe myapp-restore --details

# Check for warnings
velero restore logs myapp-restore | grep -i warning

# Check skipped resources
velero restore describe myapp-restore | grep -A 20 "Warnings:"
```

## Best Practices

1. **Verify backup first**: Ensure backup completed successfully
2. **Plan for conflicts**: Know how to handle existing resources
3. **Test in non-prod**: Verify restore works before DR scenario
4. **Monitor closely**: Watch restore progress in real-time
5. **Verify thoroughly**: Check all aspects of restored app
6. **Document process**: Keep runbooks for DR scenarios
7. **Time estimates**: Know how long restores take
8. **Storage class mapping**: Plan for cross-cluster restores
9. **Network policies**: May need updating after restore
10. **Secrets rotation**: Consider rotating secrets after restore

## Common Scenarios

### Disaster Recovery

```bash
#!/bin/bash
# DR restore script

BACKUP_NAME=$1
TARGET_NAMESPACE=$2

echo "Starting DR restore from $BACKUP_NAME to $TARGET_NAMESPACE"

# 1. Verify backup
velero backup get $BACKUP_NAME || exit 1

# 2. Create namespace if needed
oc get namespace $TARGET_NAMESPACE || \
  oc create namespace $TARGET_NAMESPACE

# 3. Create restore
velero restore create dr-restore-$(date +%s) \
  --from-backup $BACKUP_NAME \
  --namespace-mappings source-ns:$TARGET_NAMESPACE \
  --wait || exit 1

# 4. Verify
echo "Verifying restore..."
oc wait --for=condition=ready pod \
  -l app=$APP_LABEL \
  -n $TARGET_NAMESPACE \
  --timeout=10m

echo "DR restore completed successfully"
```

### Application Migration

```bash
# Migrate app to new cluster

# On source cluster - create backup
velero backup create app-migration \
  --include-namespaces myapp \
  --wait

# On target cluster - configure same BSL
# Then restore
velero restore create app-migration-restore \
  --from-backup app-migration \
  --wait

# Update DNS/routes to point to new cluster
```

## Next Steps

- Verify application functionality
- Update configurations for new environment
- Test application thoroughly
- Document any manual steps required
- Plan for cleanup of source resources (if migration)
- Schedule regular restore testing
