# AI Product Generator Skill

## Overview
Generate complete product listings from photos using vision AI.

## How It Works
1. Send photo via Telegram/WhatsApp to OpenClaw
2. Vision model analyzes the image
3. AI generates name, description, category, tags
4. Suggests competitive pricing
5. Creates product in Firebase
6. Optionally shares to social media

## Skill Configuration

```yaml
# ~/.openclaw/skills/plint-product-gen.yaml
name: plint-product-generator
version: 1.0.0
description: Generate product listings from photos

capabilities:
  - vision_analysis
  - market_research
  - content_generation
  - firebase_write

inputs:
  image:
    type: image
    required: true
    sources: [telegram, whatsapp, file_upload]
  
  base_price:
    type: number
    required: false
    description: Optional starting price point
    
  category_hint:
    type: string
    required: false
    description: Optional category suggestion

outputs:
  product:
    name: string
    description: string (SEO optimized, 150-300 chars)
    category: enum [from Plint categories]
    tags: array[string]
    suggested_price: number
    market_comparison: object
    firebase_id: string
    share_links: object
```

## Vision Prompts

### Product Analysis
```
Analyze this product image and extract:

1. **Product Type**: What is this item?
2. **Material**: What is it made of?
3. **Color**: Primary and accent colors
4. **Condition**: New, used, vintage?
5. **Target Audience**: Who would buy this?
6. **Key Features**: List 3-5 selling points
7. **Estimated Quality**: Budget, mid-range, premium?

Format as JSON for processing.
```

### Description Generation
```
Create a compelling product description for e-commerce:

Product: {{ product_type }}
Features: {{ features }}
Target: {{ audience }}

Requirements:
- Under 300 characters
- Include 2-3 keywords naturally
- Create urgency without being pushy
- Highlight unique value proposition
- Sound professional but friendly
```

### Category Mapping
```javascript
// Map AI analysis to Plint categories
const categoryMapping = {
  'clothing': 'Clothing & Fashion',
  'electronics': 'Electronics & Technology',
  'jewelry': 'Jewelry & Accessories',
  'food': 'Food & Beverages',
  'beauty': 'Beauty & Personal Care',
  'home': 'Home & Garden',
  // ... etc
};
```

## Price Intelligence

### Market Research
```yaml
pricing_strategy:
  sources:
    - competitor_analysis
    - market_averages
    - demand_indicators
    
  factors:
    - product_quality
    - brand_positioning
    - target_margin
    - local_market_adjustment
    
  output:
    suggested_price: number
    price_range: { min: number, max: number }
    confidence: percent
    rationale: string
```

## Sample Conversation Flow

```
You: *sends photo of leather bag*

OpenClaw: 📸 Analyzing product image...

I see a premium leather messenger bag. Here's what I've prepared:

📦 **Product Details**
• Name: Vintage Brown Leather Messenger Bag
• Category: Jewelry & Accessories
• Tags: leather, bag, messenger, vintage, men, work

📝 **Description**
"Handcrafted genuine leather messenger bag with antique brass hardware. Features adjustable strap, multiple compartments, and laptop sleeve. Perfect for professionals who value timeless style."

💰 **Pricing Analysis**
• Suggested: KES 4,500
• Market Range: KES 3,800 - 5,500
• Your margin at this price: ~45%

Ready to publish?
• Type "yes" to create product
• Type "edit name: [new name]" to change
• Type "price: [amount]" to adjust
• Type "cancel" to discard
```

## Firebase Integration

```javascript
// Create product in Firestore
async function createProduct(productData, userId) {
  const product = {
    name: productData.name,
    description: productData.description,
    price: productData.suggestedPrice,
    category: productData.category,
    tags: productData.tags,
    imageUrl: await uploadImage(productData.image),
    userId: userId,
    isVisible: true,
    createdAt: new Date(),
    updatedAt: new Date(),
    stockQuantity: productData.initialStock || 10,
    trackStock: true,
    minStockLevel: 5,
    aiGenerated: true,
    aiConfidence: productData.confidence
  };
  
  return await addDoc(collection(db, 'products'), product);
}
```

## Social Sharing (Optional)

```yaml
share_options:
  whatsapp_status:
    template: "🆕 Just added: {{ name }} - {{ price }}! Shop now: {{ link }}"
    
  twitter:
    template: "New arrival! {{ name }} ✨ {{ price }} | Shop: {{ link }} #{{ tags[0] }}"
    
  instagram_caption:
    template: |
      {{ name }}
      
      {{ description }}
      
      💰 {{ price }}
      📦 Free shipping on orders over KES 2000
      
      Link in bio! 🔗
      
      {{ hashtags }}
```

## Batch Processing

```
You: "OpenClaw, I have 20 products to add"

OpenClaw: Great! Send me the photos one by one or as an album.
For each, I'll generate:
• Product name & description
• Category & tags  
• Suggested pricing

After processing all, I'll show you a summary to review
before publishing. Ready when you are! 📸
```

## Quality Checks

```yaml
validation:
  image_quality:
    min_resolution: 800x800
    blur_detection: true
    lighting_check: true
    
  description:
    min_length: 100
    max_length: 500
    keyword_density: 2-3%
    
  pricing:
    min_margin: 20%
    max_deviation: 30%  # from market avg
```

## Error Handling

```
# If image is unclear
OpenClaw: "I'm having trouble identifying this product clearly. 
Could you send another photo with better lighting or a different angle?"

# If category is ambiguous
OpenClaw: "This could be categorized as either 'Home & Garden' 
or 'Arts & Crafts'. Which fits better for your store?"

# If pricing data unavailable
OpenClaw: "I couldn't find market data for this exact product.
Based on similar items, I suggest KES 2,000-3,000.
What price would you like to set?"
```
