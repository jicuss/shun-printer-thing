# Testing Guide

## Test Overview

Comprehensive testing strategy covering unit tests, integration tests, end-to-end tests, and user acceptance testing.

## Test Phases

### Phase 1: Unit Testing

#### Odoo Module Tests

**Test: Lot Number Generation**

> **Code Example**: See [appendix/code-examples/tests/test_lot_number_generation.py](../../../appendix/code-examples/tests/test_lot_number_generation.py)

Unit tests verifying lot number uniqueness and sequential numbering.

**Test: GS1 Barcode Generation**

> **Code Example**: See [appendix/code-examples/tests/test_gs1_barcode.py](../../../appendix/code-examples/tests/test_gs1_barcode.py)

Unit tests for GS1 weight encoding and GTIN check digit validation.

#### Flask Server Tests

**Test: Print Job Submission**

> **Code Example**: See [appendix/code-examples/tests/test_flask_api.py](../../../appendix/code-examples/tests/test_flask_api.py)

Flask API tests for print job submission and error handling.

---

### Phase 2: Integration Testing

#### Test: MO Split to Print

**Scenario**: Split MO triggers automatic printing

> **Code Example**: See [appendix/code-examples/tests/test_integration_mo_split.py](../../../appendix/code-examples/tests/test_integration_mo_split.py)

Integration test for complete MO split to print job creation flow.

#### Test: Odoo to Flask Communication

> **Code Example**: See [appendix/code-examples/tests/test_integration_flask_api.py](../../../appendix/code-examples/tests/test_integration_flask_api.py)

Integration test with mocked Flask API responses to verify Odoo-Flask communication.

---

### Phase 3: End-to-End Testing

#### Test Scenario 1: Complete Print Workflow (200 Labels)

**Steps**:
1. Create MO for 200 units of catch weight product
2. Assign catch weights to each unit
3. Split MO into 200 units
4. Wait for automatic print
5. Verify all 200 labels printed
6. Scan random labels to verify barcodes

**Expected Results**:
- All 200 lot numbers unique
- All 200 labels print successfully
- Print time < 10 minutes
- All barcodes scannable
- Job logged in history

**Test Script**:

> **Code Example**: See [appendix/code-examples/tests/test_e2e_batch_print.py](../../../appendix/code-examples/tests/test_e2e_batch_print.py)

End-to-end test for complete 200 label batch print workflow with timing and verification.

#### Test Scenario 2: Manual Reprint

**Steps**:
1. Complete MO with 10 units
2. Navigate to MO form
3. Click "Reprint Labels"
4. Select boxes 5-7
5. Submit reprint
6. Verify only 3 labels print

**Expected Results**:
- Reprint dialog opens
- Only selected boxes print (5, 6, 7)
- Labels match original data
- New job logged as "manual_reprint"

---

### Phase 4: Performance Testing

#### Metrics to Measure

| Metric | Target | Test Method |
|--------|--------|-------------|
| Lot generation (200 units) | < 2 sec | Time function execution |
| Label data prep (200 units) | < 3 sec | Time ZPL generation |
| Print throughput | > 20 labels/min | Time batch print |
| API response time | < 500 ms | Apache Bench |
| Job queue capacity | 100 concurrent jobs | Load test |

#### Load Testing

```bash
# Test Flask API performance
ab -n 1000 -c 10 \
  -H "Authorization: Bearer test-key" \
  -p test_payload.json \
  -T application/json \
  https://print-server.local:5000/api/print
```

---

### Phase 5: User Acceptance Testing (UAT)

#### Test Participants
- 3-5 commissary staff members
- 1 production supervisor
- 1 QC manager

#### UAT Scenarios

**Scenario 1: Normal Production Day**
- Process 10 MOs with various quantities
- Use automatic printing
- Verify labels applied correctly to products

**Scenario 2: Error Recovery**
- Simulate printer offline during print
- Verify error message displayed
- Verify retry successfully prints

**Scenario 3: Reprint Damaged Labels**
- Simulate damaged labels (boxes 15, 23, 47)
- Use manual reprint for specific boxes
- Verify correct labels print

#### UAT Feedback Form

- Ease of use (1-5 scale)
- Speed of operation (1-5 scale)
- Label quality (1-5 scale)
- Error message clarity (1-5 scale)
- Overall satisfaction (1-5 scale)
- Open feedback

---

## Test Data

### Sample Products & Catch Weights

> **Code Example**: See [appendix/code-examples/tests/test_data.py](../../../appendix/code-examples/tests/test_data.py)

Test data fixtures including sample products and catch weights for testing.

## Test Results Documentation

### Template

```markdown
## Test Run: [Date]

### Test Phase: [Unit/Integration/E2E/UAT]

**Tester**: [Name]
**Environment**: [Test/Staging/Production]

### Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| Test 1 | ✅ Pass | |
| Test 2 | ❌ Fail | Error message X |
| Test 3 | ⚠️ Warning | Performance below target |

### Issues Found
1. [Issue description]
2. [Issue description]

### Recommendations
- [Action item 1]
- [Action item 2]
```

## Related Documents
- [Deployment Guide](deployment.md)
- [Maintenance Guide](maintenance.md)