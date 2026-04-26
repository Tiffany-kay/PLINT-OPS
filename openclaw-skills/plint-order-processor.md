# Plint Order Processor Skill

## Overview
Automatically process orders from receipt to fulfillment.

## Triggers
- Firebase webhook on new order
- Manual command: "process order #123"
- Scheduled: Check pending orders every hour

## Workflow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ New Order   │────▶│ Verify       │────▶│ Update      │
│ Received    │     │ Payment      │     │ Stock       │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌──────────────┐     ┌─────────────┐
                    │ Payment      │     │ Notify      │
                    │ Pending?     │     │ Customer    │
                    └──────────────┘     └─────────────┘
                           │                    │
              ┌────────────┼────────────┐      │
              ▼            ▼            ▼      ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐ │
       │ Send     │ │ Wait &   │ │ Mark     │ │
       │ Reminder │ │ Check    │ │ Failed   │ │
       └──────────┘ └──────────┘ └──────────┘ │
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ Order        │
                                       │ Complete     │
                                       └──────────────┘
```

## Skill Configuration

```yaml
name: plint-order-processor
version: 1.0.0
description: Automated order processing pipeline

triggers:
  # Real-time webhook
  - type: webhook
    path: /plint/new-order
    action: process_new_order
    
  # Scheduled check for stuck orders
  - type: cron
    schedule: "0 * * * *"  # Every hour
    action: check_pending_orders
    
  # Manual command
  - type: command
    patterns:
      - "process order"
      - "check order"
      - "ship order"

memory:
  - pending_orders: array
  - processed_today: number
  - average_processing_time: number

actions:
  process_new_order:
    timeout: 120  # seconds
    steps:
      - validate_order_data
      - check_payment_status
      - verify_stock_available
      - deduct_stock
      - send_customer_confirmation
      - notify_owner
      - log_transaction
      
  check_pending_orders:
    steps:
      - fetch_pending_orders
      - for_each:
          - check_payment_status
          - decide_action
          - execute_action
      - summarize_results
```

## Payment Verification

### M-Pesa Check
```javascript
async function verifyMpesaPayment(order) {
  const result = await mpesaService.checkStatus(order.paymentReference);
  
  if (result.status === 'completed') {
    return { verified: true, method: 'mpesa', reference: result.transactionId };
  } else if (result.status === 'pending') {
    return { verified: false, reason: 'awaiting_confirmation' };
  } else {
    return { verified: false, reason: result.error };
  }
}
```

### Crypto Check (Base)
```javascript
async function verifyCryptoPayment(order) {
  const receipt = await publicClient.getTransactionReceipt({
    hash: order.transactionHash
  });
  
  if (receipt && receipt.status === 'success') {
    return { verified: true, method: 'crypto', hash: order.transactionHash };
  }
  return { verified: false, reason: 'transaction_not_found' };
}
```

## Stock Management

```javascript
async function processStockDeduction(order) {
  const productRef = doc(db, 'products', order.productId);
  const product = await getDoc(productRef);
  
  if (!product.exists()) {
    throw new Error('Product not found');
  }
  
  const currentStock = product.data().stockQuantity || 0;
  const orderQuantity = order.quantity || 1;
  
  if (currentStock < orderQuantity && !product.data().allowBackorders) {
    return { success: false, reason: 'insufficient_stock' };
  }
  
  const newStock = currentStock - orderQuantity;
  
  await updateDoc(productRef, {
    stockQuantity: newStock,
    stockStatus: newStock === 0 ? 'out_of_stock' : 
                 newStock <= product.data().minStockLevel ? 'low_stock' : 'in_stock',
    updatedAt: new Date()
  });
  
  // Log transaction
  await addDoc(collection(db, 'stockTransactions'), {
    productId: order.productId,
    orderId: order.id,
    type: 'sold',
    quantity: orderQuantity,
    previousStock: currentStock,
    newStock: newStock,
    timestamp: new Date(),
    userId: order.businessOwnerId
  });
  
  return { success: true, newStock };
}
```

## Customer Notifications

### Order Confirmation (WhatsApp)
```
🎉 Order Confirmed!

Hi {{ customerName }},

Your order #{{ orderId }} has been confirmed!

📦 {{ productName }}
💰 {{ currency }}{{ total }}
✅ Payment: Received

We'll notify you when it ships.

Questions? Reply to this message.

Thank you for shopping with {{ storeName }}! 🛍️
```

### Shipping Update
```
📦 Your Order is on its Way!

Hi {{ customerName }},

Great news! Order #{{ orderId }} has shipped.

🚚 Carrier: {{ carrier }}
📍 Tracking: {{ trackingNumber }}
📅 Expected: {{ estimatedDelivery }}

Track: {{ trackingUrl }}

Questions? We're here to help!
```

### Payment Reminder
```
⏰ Payment Reminder

Hi {{ customerName }},

Your order #{{ orderId }} is awaiting payment.

📦 {{ productName }}
💰 {{ currency }}{{ total }}

To pay via M-Pesa:
1. Go to M-Pesa
2. Select Lipa na M-Pesa
3. Enter Paybill: {{ paybill }}
4. Account: {{ orderId }}
5. Amount: {{ total }}

Order expires in {{ hoursRemaining }} hours.

Need help? Reply here!
```

## Error Handling

```yaml
error_handling:
  payment_verification_failed:
    action: retry
    max_retries: 3
    interval: 300  # 5 minutes
    on_final_failure: mark_for_review
    
  stock_deduction_failed:
    action: rollback
    notify: owner
    
  notification_failed:
    action: queue
    retry_after: 60
    fallback: email
    
  unknown_error:
    action: log
    notify: owner
    escalate: true
```

## Owner Notifications

### New Order Alert
```
🛒 NEW ORDER!

#{{ orderId }}
Customer: {{ customerName }}
Phone: {{ customerPhone }}
Product: {{ productName }}
Amount: {{ currency }}{{ total }}
Payment: {{ paymentStatus }}

{{ if paymentStatus == 'confirmed' }}
✅ Ready to fulfill!
{{ else }}
⏳ Awaiting payment
{{ endif }}

Quick Actions:
• "ship {{ orderId }}" - Mark as shipped
• "call {{ orderId }}" - Call customer
• "cancel {{ orderId }}" - Cancel order
```

### Daily Processing Summary
```
📊 Order Processing Summary

Today's Activity:
✅ Processed: {{ processed }} orders
⏳ Pending: {{ pending }} orders
❌ Failed: {{ failed }} orders

Revenue Processed: {{ currency }}{{ totalRevenue }}
Average Processing Time: {{ avgTime }} minutes

{{ if pending > 0 }}
⚠️ Pending Orders:
{{ for order in pendingOrders }}
• #{{ order.id }} - {{ order.reason }}
{{ endfor }}
{{ endif }}

{{ if failed > 0 }}
🚨 Needs Attention:
{{ for order in failedOrders }}
• #{{ order.id }} - {{ order.error }}
{{ endfor }}
{{ endif }}
```

## Conversation Examples

### Check Order Status
```
You: "What's happening with order 456?"

OpenClaw: 📦 Order #456 Status

Customer: John Doe
Product: Wireless Earbuds
Amount: KES 2,500
Created: 2 hours ago

Timeline:
✅ 14:30 - Order received
✅ 14:31 - Payment confirmed (M-Pesa)
✅ 14:31 - Stock updated (15 → 14)
✅ 14:32 - Customer notified
⏳ Awaiting shipment

Next: "ship 456" to mark as shipped
```

### Bulk Processing
```
You: "Process all pending orders"

OpenClaw: 🔄 Processing 5 pending orders...

#451: ✅ Payment confirmed, stock updated, notified
#452: ⏳ Payment still pending (1hr old) - sent reminder
#453: ✅ Payment confirmed, stock updated, notified
#454: ❌ Insufficient stock - flagged for review
#455: ✅ Payment confirmed, stock updated, notified

Summary:
• Completed: 3
• Pending: 1
• Failed: 1

Order #454 needs attention - "Blue T-Shirt" is out of stock.
Shall I:
1. Cancel and refund?
2. Offer alternative product?
3. Wait for restock?
```

### Manual Override
```
You: "Force complete order 452 - customer paid cash"

OpenClaw: ⚠️ Manual override requested for Order #452

Current status: Payment pending
Action: Mark as paid (cash)

This will:
• Update payment status to "paid"
• Deduct stock
• Send confirmation to customer
• Log manual override reason

Confirm? Reply YES to proceed.

---

You: "yes"

OpenClaw: ✅ Order #452 manually completed

• Payment: Marked as CASH
• Stock: Deducted
• Customer: Notified
• Log: Manual override recorded

Order is ready for fulfillment!
```
