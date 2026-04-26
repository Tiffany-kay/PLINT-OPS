# Plint Store Monitor Skill

## Overview
This skill monitors your Plint store 24/7 and alerts you about important events.

## Triggers
- Every 5 minutes (cron job)
- On webhook from Firebase (instant alerts)

## Capabilities
1. **New Order Detection**: Alert immediately when order comes in
2. **Payment Status**: Track M-Pesa/crypto payment confirmations
3. **Low Stock Warnings**: Alert when products fall below threshold
4. **Daily Summary**: Revenue, orders, top products

## Setup Instructions

### 1. Firebase Service Account
```bash
# Export your Firebase service account key
# Save to: ~/.openclaw/credentials/firebase-key.json
```

### 2. Environment Variables
```bash
FIREBASE_PROJECT_ID=your-plint-project
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
PLINT_STORE_URL=https://your-store.netlify.app
LOW_STOCK_THRESHOLD=5
```

### 3. Skill Configuration
```yaml
# ~/.openclaw/skills/plint-monitor.yaml
name: plint-store-monitor
version: 1.0.0
description: Monitor Plint store for orders, stock, and payments

memory:
  - last_order_check: timestamp
  - daily_revenue: number
  - pending_alerts: array

triggers:
  - type: cron
    schedule: "*/5 * * * *"
    action: check_new_orders
    
  - type: cron
    schedule: "0 8 * * *"
    action: send_daily_report
    
  - type: webhook
    path: /plint/order-created
    action: instant_order_alert

actions:
  check_new_orders:
    steps:
      - fetch_orders_since: "{{ memory.last_order_check }}"
      - for_each_order:
          - check_payment_status
          - update_stock_levels
          - send_notification_if_needed
      - update_memory: last_order_check
      
  send_daily_report:
    steps:
      - aggregate_yesterday_data
      - calculate_metrics:
          - total_revenue
          - order_count
          - top_products (limit: 5)
          - low_stock_items
      - format_report
      - send_via: telegram
      
  instant_order_alert:
    steps:
      - parse_order_data
      - format_quick_alert
      - send_via: telegram
      - update_memory
```

## Sample Prompts for OpenClaw

### Check Store Status
```
"Check my Plint store right now"
"Any new orders in the last hour?"
"What's my revenue today?"
```

### Stock Management
```
"What products are running low?"
"Show me stock levels for all products"
"Alert me when Blue T-Shirts drop below 10"
```

### Order Management
```
"Show me pending orders"
"Mark order #123 as shipped"
"What's the status of the last 5 orders?"
```

## Firebase Queries Used

```javascript
// New orders since last check
const ordersRef = collection(db, 'orders');
const q = query(
  ordersRef,
  where('createdAt', '>', lastCheckTimestamp),
  where('businessOwnerId', '==', userId),
  orderBy('createdAt', 'desc')
);

// Low stock products
const productsRef = collection(db, 'products');
const lowStockQuery = query(
  productsRef,
  where('userId', '==', userId),
  where('stockQuantity', '<', LOW_STOCK_THRESHOLD),
  where('trackStock', '==', true)
);
```

## Notification Templates

### New Order Alert
```
🛒 NEW ORDER #{{ order.id }}

Customer: {{ order.customerName }}
Phone: {{ order.customerPhone }}
Product: {{ order.productName }}
Amount: {{ currency }}{{ order.total }}
Payment: {{ order.paymentMethod }} - {{ order.paymentStatus }}

Reply with:
• "confirm" to mark as processing
• "call" to dial customer
• "details" for full info
```

### Low Stock Warning
```
⚠️ LOW STOCK ALERT

{{ product.name }}
Current: {{ product.stockQuantity }} units
Min Level: {{ product.minStockLevel }} units
Last Sale: {{ product.lastSaleDate }}

Estimated stockout: {{ estimatedDays }} days

Reply "restock {{ quantity }}" to add stock
```

### Daily Report
```
📊 PLINT DAILY REPORT - {{ date }}

💰 Revenue: {{ currency }}{{ totalRevenue }}
📦 Orders: {{ orderCount }} ({{ changePercent }}% vs last week)
🏆 Top Seller: {{ topProduct.name }} ({{ topProduct.quantity }} sold)

⚠️ Needs Attention:
{{ lowStockItems }}

💡 Insight: {{ aiGeneratedInsight }}

Full analytics: {{ analyticsUrl }}
```

## Integration Points

### With Copilot/Cursor (for development)
```
"OpenClaw: Tell Copilot to fix the bug in Orders.tsx line 234"
"OpenClaw: Have Cursor add pagination to the products page"
"OpenClaw: Run tests and report any failures"
```

### With WhatsApp Business
```
"OpenClaw: Send order update to customer +254..."
"OpenClaw: Broadcast low stock notice to all staff"
```

## Error Handling

```yaml
on_error:
  firebase_connection:
    retry: 3
    fallback: notify_owner
    
  api_rate_limit:
    wait: exponential_backoff
    max_wait: 300
    
  payment_check_failed:
    log: error
    alert: owner
    retry: manual
```

## Metrics Tracked

- Orders per hour/day/week
- Revenue trends
- Stock velocity (how fast items sell)
- Payment success rate
- Average order value
- Customer response time
