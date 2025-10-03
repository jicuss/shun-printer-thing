# Testing Guide

## Test Overview

Comprehensive testing strategy covering unit tests, integration tests, end-to-end tests, and user acceptance testing.

## Test Phases

### Phase 1: Unit Testing

#### Odoo Module Tests

**Test: Lot Number Generation**
```python
class TestLotNumberGeneration(TransactionCase):
    
    def test_unique_lot_numbers(self):
        """Verify lot numbers are unique"""
        mo = self.env.ref('mrp.test_mo')
        generator = self.env['lot.number.generator']
        
        lots = generator.generate_for_mo_split(mo, quantity=10)
        lot_numbers = [lot.lot_number for lot in lots]
        
        # All unique
        self.assertEqual(len(lot_numbers), len(set(lot_numbers)))
    
    def test_sequential_numbering(self):
        """Verify lot numbers are sequential"""
        mo = self.env.ref('mrp.test_mo')
        generator = self.env['lot.number.generator']
        
        lots = generator.generate_for_mo_split(mo, quantity=5)
        
        # Extract sequence numbers
        sequences = [int(lot.lot_number.split('-')[-1]) for lot in lots]
        
        # Check sequential
        for i in range(1, len(sequences)):
            self.assertEqual(sequences[i], sequences[i-1] + 1)
```

**Test: GS1 Barcode Generation**
```python
class TestGS1Barcode(TransactionCase):
    
    def test_weight_encoding(self):
        """Test catch weight encoding"""
        generator = self.env['gs1.barcode.generator']
        
        # Test 1.250 kg
        encoded = generator._encode_weight(1.250, decimal_places=3)
        self.assertEqual(encoded, '001250')
        
        # Test edge cases
        encoded = generator._encode_weight(0.001, decimal_places=3)
        self.assertEqual(encoded, '000001')
        
        encoded = generator._encode_weight(999.999, decimal_places=3)
        self.assertEqual(encoded, '999999')
    
    def test_gtin_validation(self):
        """Test GTIN check digit validation"""
        generator = self.env['gs1.barcode.generator']
        
        # Valid GTIN
        self.assertTrue(generator._validate_gtin_check_digit('00012345678905'))
        
        # Invalid GTIN
        self.assertFalse(generator._validate_gtin_check_digit('00012345678904'))
```

#### Flask Server Tests

**Test: Print Job Submission**
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_print_job_submission(client):
    """Test POST /api/print endpoint"""
    response = client.post('/api/print', json={
        'printer': 'zebra_z230_line1',
        'quantity': 1,
        'labels': [{'zpl_code': '^XA^FO50,50^A0N,50,50^FDTest^FS^XZ'}]
    }, headers={'Authorization': 'Bearer test-key'})
    
    assert response.status_code == 201
    assert 'job_id' in response.json

def test_invalid_printer(client):
    """Test submission to non-existent printer"""
    response = client.post('/api/print', json={
        'printer': 'invalid_printer',
        'quantity': 1,
        'labels': [{'zpl_code': '^XA^XZ'}]
    }, headers={'Authorization': 'Bearer test-key'})
    
    assert response.status_code == 404
```

---

### Phase 2: Integration Testing

#### Test: MO Split to Print

**Scenario**: Split MO triggers automatic printing

```python
def test_mo_split_triggers_print(self):
    """Test complete flow from MO split to print job creation"""
    # Create MO
    mo = self.env['mrp.production'].create({
        'product_id': self.product.id,
        'product_qty': 10
    })
    
    # Split MO
    mo.action_split_production()
    
    # Verify lot numbers generated
    lots = self.env['lot.number.generator'].search([('mo_id', '=', mo.id)])
    self.assertEqual(len(lots), 10)
    
    # Verify print job created
    print_job = self.env['label.print.job'].search([('mo_id', '=', mo.id)])
    self.assertTrue(print_job)
    self.assertEqual(print_job.quantity, 10)
    self.assertEqual(print_job.status, 'sent')
```

#### Test: Odoo to Flask Communication

```python
import responses

@responses.activate
def test_flask_api_communication(self):
    """Test Odoo successfully calls Flask API"""
    # Mock Flask API response
    responses.add(
        responses.POST,
        'https://print-server.local:5000/api/print',
        json={'job_id': 'test-uuid', 'status': 'queued'},
        status=201
    )
    
    job = self.env['label.print.job'].create({...})
    job._submit_to_print_server()
    
    # Verify job updated with Flask job ID
    self.assertEqual(job.flask_job_id, 'test-uuid')
    self.assertEqual(job.status, 'sent')
```

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
```python
def test_200_label_batch_print(self):
    mo = self.create_mo_with_catch_weights(quantity=200)
    
    start_time = time.time()
    mo.action_split_production()
    
    # Wait for completion (poll job status)
    job = self.env['label.print.job'].search([('mo_id', '=', mo.id)])
    self.wait_for_job_completion(job, timeout=600)  # 10 min timeout
    
    elapsed_time = time.time() - start_time
    
    # Assertions
    self.assertEqual(job.status, 'completed')
    self.assertLess(elapsed_time, 600)
    
    lots = self.env['lot.number.generator'].search([('mo_id', '=', mo.id)])
    self.assertEqual(len(lots), 200)
    self.assertTrue(all(lot.label_printed for lot in lots))
```

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

### Sample Products

```python
products = [
    {'name': 'Wild Caught Salmon', 'sku': 'SALM-001', 'gtin': '00012345678905'},
    {'name': 'Atlantic Cod', 'sku': 'COD-001', 'gtin': '00012345678912'},
    {'name': 'King Crab Legs', 'sku': 'CRAB-001', 'gtin': '00012345678929'},
]
```

### Sample Catch Weights

```python
weights = [1.150, 1.250, 1.350, 1.420, 1.180, 1.290, 1.310, 1.400, 1.220, 1.260]
```

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