# Finance Plugins Development Plan

Based on first-principles analysis.

## Step 1: Question - What Problem Are We Solving?

**Core Problem**: Manual data entry between Mercury (banking) and QuickBooks (accounting) is time-consuming and error-prone.

**Validated Need**:
- Real business need: Accountants waste hours copying transactions manually
- Current workaround: Manual CSV export/import or third-party services ($$$)

**Success Criteria**:
- [ ] New Mercury transactions automatically appear in QuickBooks
- [ ] No manual data entry required
- [ ] Duplicate prevention works reliably

## Step 2: Delete - What Can We Remove?

### Current Scope Analysis

| Plugin | Status | Needed for Core Problem? |
|--------|--------|--------------------------|
| mercury_tools_plugin | 100% done | **YES** - Query transactions |
| quickbooks_plugin | 100% done | **YES** - Create entries |
| quickbooks_payments_plugin | 100% done | **NO** - Payments is separate concern |
| mercury_trigger_plugin | 40% done | **MAYBE** - Is webhook trigger necessary? |

### Critical Question: Do We Need the Trigger Plugin?

**Alternative approaches**:

| Approach | Complexity | Reliability | User Value |
|----------|------------|-------------|------------|
| A: Webhook Trigger | High (OAuth, webhook setup) | Medium (delivery issues) | Auto-sync |
| B: Scheduled Workflow | Low (just use existing tools) | High | Manual trigger |
| C: Manual Tool Chain | Lowest | Highest | On-demand |

**First-principles decision**:
- **Option B (Scheduled Workflow)** delivers 80% of value with 20% of complexity
- Mercury Tools + QuickBooks Tools already exist and work
- A Dify workflow can: get_transactions → filter new → create_purchase/deposit
- No trigger plugin needed for MVP!

### Deleted from Scope

```
DELETED:
├── mercury_trigger_plugin completion (defer to v2)
├── quickbooks_payments_plugin (separate concern)
├── Real-time webhook sync (scheduled polling is sufficient)
└── Complex event filtering (handle in workflow)
```

## Step 3: Simplify - What's the Minimal Solution?

### MVP Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Dify Workflow                       │
│  (Scheduled or manual trigger)                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  1. get_transactions (Mercury)                       │
│         ↓                                            │
│  2. Filter: new transactions only                    │
│         ↓                                            │
│  3. For each transaction:                            │
│     - Debit → create_purchase (QuickBooks)           │
│     - Credit → create_deposit (QuickBooks)           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### What's Already Done

| Component | Status | Action Needed |
|-----------|--------|---------------|
| Mercury get_transactions | ✅ Working | None |
| Mercury get_accounts | ✅ Working | None |
| QuickBooks create_purchase | ✅ Working | None |
| QuickBooks create_deposit | ✅ Working | None |
| QuickBooks vendor_management | ✅ Working | None |

### What's Missing (Minimal)

| Gap | Priority | Solution |
|-----|----------|----------|
| Duplicate prevention | P0 | Add transaction ID to QuickBooks PrivateNote field |
| Workflow template | P0 | Create example Dify workflow |
| Documentation | P1 | Usage guide for the workflow |

## Step 4: Accelerate - Implementation Plan

### Week 1: Core Integration

**Day 1-2**: Duplicate Prevention
```
Task: Ensure create_purchase and create_deposit use Mercury transaction_id
Files:
  - quickbooks_plugin/tools/create_purchase.py
  - quickbooks_plugin/tools/create_deposit.py
Change: Add PrivateNote with Mercury transaction ID
```

**Day 3-4**: Workflow Template
```
Task: Create example Dify workflow for Mercury→QuickBooks sync
Output: workflow_templates/mercury_quickbooks_sync.json
Steps:
  1. Trigger (schedule or manual)
  2. Get Mercury transactions (last 24h)
  3. Loop through transactions
  4. Check if exists in QuickBooks (query by PrivateNote)
  5. If new: create_purchase or create_deposit
```

**Day 5**: Testing & Documentation
```
Task: End-to-end testing with sandbox environments
Output: README updates, troubleshooting guide
```

### Week 2: Polish (If Needed)

- User feedback collection
- Edge case handling
- Performance optimization

## Step 5: Automate - Future Considerations

**Only after MVP is validated**:

| Automation | Trigger | Priority |
|------------|---------|----------|
| Webhook trigger plugin | Users need real-time | v2.0 |
| Auto-categorization | Users request it | v2.0 |
| Multi-account support | Users have multiple | v2.0 |

## Summary: What We're Actually Building

```
┌─────────────────────────────────────────────────────┐
│  MVP: Mercury → QuickBooks Sync                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  KEEP (Already Done):                                │
│  ✅ mercury_tools_plugin                             │
│  ✅ quickbooks_plugin                                │
│                                                      │
│  ADD (Minimal):                                      │
│  📝 Duplicate prevention (PrivateNote field)        │
│  📝 Example workflow template                        │
│  📝 Usage documentation                              │
│                                                      │
│  DELETE (Not for v1):                                │
│  ❌ mercury_trigger_plugin (defer)                   │
│  ❌ quickbooks_payments_plugin (separate concern)    │
│  ❌ Real-time sync (polling is enough)               │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Next Actions

1. [ ] Verify duplicate prevention in QuickBooks tools
2. [ ] Create workflow template
3. [ ] Test end-to-end with sandbox
4. [ ] Document usage
