#!/usr/bin/env python3
"""
STEWIE'S LEAD SCRAPER
=====================
Web scraping script to find potential Plint customers in Kenya.

Usage (from WSL):
  cd /mnt/c/Users/HP\ ELITEBOOK/Desktop/ForStewie/plint
  python3 scripts/scrape_leads.py

Requirements:
  pip install requests beautifulsoup4 pandas
"""

import os
import csv
import json
from datetime import datetime
from typing import List, Dict

# Output paths
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'marketing', 'leads')
LEADS_FILE = os.path.join(OUTPUT_DIR, 'leads.csv')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# LEAD SOURCES TO SCRAPE
# ============================================

INSTAGRAM_HASHTAGS = [
    'NairobiSmallBusiness',
    'KenyaBusiness', 
    'ShopLocalKenya',
    'MadeInKenya',
    'KenyanEntrepreneur',
    'NairobiFashion',
    'KenyaFood',
    'AfricanBusiness',
]

TWITTER_SEARCHES = [
    '"small business" Kenya',
    '"online store" Kenya',
    '"DM to order" Nairobi',
    '"WhatsApp to buy" Kenya',
    'selling Kenya -job',
]

FACEBOOK_GROUPS = [
    'Kenya Small Business Owners',
    'Nairobi Entrepreneurs',
    'Buy and Sell Kenya',
    'Made in Kenya Products',
]

GOOGLE_SEARCHES = [
    'site:instagram.com "nairobi" "shop" "dm to order"',
    'site:twitter.com "kenya" "small business" "whatsapp"',
    '"retail shop" nairobi contact',
]

# ============================================
# LEAD SCHEMA
# ============================================

def create_lead(
    business_name: str,
    contact: str,
    platform: str,
    products: str,
    location: str,
    notes: str,
    score: int
) -> Dict:
    """Create a lead entry"""
    return {
        'business_name': business_name,
        'contact': contact,
        'platform': platform,
        'products': products,
        'location': location,
        'notes': notes,
        'score': score,
        'status': 'new',
        'scraped_at': datetime.now().isoformat(),
    }

# ============================================
# SAMPLE LEADS (For testing)
# ============================================

SAMPLE_LEADS = [
    create_lead(
        "Mama Njeri's Kitchen",
        "@mamanjeri_eats",
        "Instagram",
        "Home-cooked meals, delivery",
        "Nairobi - Westlands",
        "Posts daily menus on stories, takes orders via DM",
        8
    ),
    create_lead(
        "Thrift Finds KE",
        "@thriftfinds_ke",
        "Instagram",
        "Second-hand clothes, vintage",
        "Nairobi - CBD",
        "Good engagement, no website, DM-only sales",
        9
    ),
    create_lead(
        "Fresh Produce 254",
        "+254712345678",
        "WhatsApp",
        "Fresh vegetables, fruits",
        "Nairobi - Ngong Road",
        "WhatsApp status selling, no catalog",
        7
    ),
    create_lead(
        "Tech Gadgets KE",
        "@techgadgets_ke",
        "Twitter",
        "Phone accessories, chargers",
        "Nairobi",
        "Tweets products, links to WhatsApp",
        8
    ),
    create_lead(
        "Handmade by Mary",
        "@handmade_by_mary",
        "Instagram",
        "Jewelry, crafts, gifts",
        "Mombasa",
        "Beautiful products, struggling with orders",
        9
    ),
]

# ============================================
# SCRAPING FUNCTIONS (Templates for Stewie)
# ============================================

def scrape_instagram_hashtag(hashtag: str) -> List[Dict]:
    """
    STEWIE: Use browser automation or API to scrape Instagram
    
    Look for accounts that:
    - Post products regularly
    - Have "DM to order" in bio
    - No link to external store
    - Good engagement (real followers)
    """
    # This is a template - Stewie should implement with actual scraping
    print(f"[Instagram] Searching #{hashtag}...")
    return []

def scrape_twitter_search(query: str) -> List[Dict]:
    """
    STEWIE: Use Twitter search or API
    
    Look for:
    - Accounts selling products
    - Complaints about manual order management
    - Kenya-based small businesses
    """
    print(f"[Twitter] Searching: {query}...")
    return []

def scrape_google_business(query: str) -> List[Dict]:
    """
    STEWIE: Use Google search
    
    Find:
    - Local businesses without websites
    - Businesses with only social media presence
    - Contact info (phone, email, WhatsApp)
    """
    print(f"[Google] Searching: {query}...")
    return []

# ============================================
# LEAD SCORING
# ============================================

def score_lead(lead: Dict) -> int:
    """
    Score a lead from 1-10 based on likelihood to convert
    
    Factors:
    - No existing online store (+3)
    - Active social media (+2)
    - Already taking orders via DM/WhatsApp (+2)
    - Good product photos (+1)
    - Nairobi location (+1)
    - Mentions payment struggles (+1)
    """
    score = 5  # Base score
    
    notes = lead.get('notes', '').lower()
    
    if 'no website' in notes or 'dm only' in notes:
        score += 3
    if 'good engagement' in notes or 'active' in notes:
        score += 2
    if 'dm to order' in notes or 'whatsapp' in notes:
        score += 2
    if 'nairobi' in lead.get('location', '').lower():
        score += 1
    if 'struggling' in notes or 'overwhelmed' in notes:
        score += 1
    
    return min(score, 10)

# ============================================
# FILE OPERATIONS
# ============================================

def save_leads(leads: List[Dict]):
    """Save leads to CSV file"""
    if not leads:
        print("No leads to save")
        return
    
    fieldnames = ['business_name', 'contact', 'platform', 'products', 
                  'location', 'notes', 'score', 'status', 'scraped_at']
    
    file_exists = os.path.exists(LEADS_FILE)
    
    with open(LEADS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(leads)
    
    print(f"Saved {len(leads)} leads to {LEADS_FILE}")

def load_leads() -> List[Dict]:
    """Load existing leads from CSV"""
    if not os.path.exists(LEADS_FILE):
        return []
    
    with open(LEADS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def deduplicate_leads(leads: List[Dict]) -> List[Dict]:
    """Remove duplicate leads based on contact"""
    seen = set()
    unique = []
    for lead in leads:
        contact = lead['contact'].lower()
        if contact not in seen:
            seen.add(contact)
            unique.append(lead)
    return unique

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    print("=" * 50)
    print("STEWIE'S LEAD SCRAPER")
    print("=" * 50)
    print()
    
    # Load existing leads
    existing_leads = load_leads()
    print(f"Existing leads: {len(existing_leads)}")
    
    # Collect new leads
    new_leads = []
    
    # Add sample leads (for testing)
    new_leads.extend(SAMPLE_LEADS)
    
    # TODO: Stewie - implement actual scraping
    # for hashtag in INSTAGRAM_HASHTAGS:
    #     new_leads.extend(scrape_instagram_hashtag(hashtag))
    
    # for query in TWITTER_SEARCHES:
    #     new_leads.extend(scrape_twitter_search(query))
    
    # for query in GOOGLE_SEARCHES:
    #     new_leads.extend(scrape_google_business(query))
    
    # Score leads
    for lead in new_leads:
        if 'score' not in lead or not lead['score']:
            lead['score'] = score_lead(lead)
    
    # Deduplicate
    all_leads = existing_leads + new_leads
    unique_leads = deduplicate_leads(all_leads)
    new_unique = len(unique_leads) - len(existing_leads)
    
    # Save new leads only
    if new_unique > 0:
        # Clear and rewrite with deduplicated
        with open(LEADS_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['business_name', 'contact', 'platform', 'products', 
                          'location', 'notes', 'score', 'status', 'scraped_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_leads)
        print(f"Added {new_unique} new leads")
    
    print()
    print(f"Total leads in database: {len(unique_leads)}")
    print()
    
    # Show top leads
    top_leads = sorted(unique_leads, key=lambda x: int(x.get('score', 0)), reverse=True)[:5]
    print("TOP 5 LEADS:")
    print("-" * 40)
    for lead in top_leads:
        print(f"  [{lead['score']}/10] {lead['business_name']}")
        print(f"         {lead['platform']}: {lead['contact']}")
        print(f"         {lead['products']}")
        print()

if __name__ == '__main__':
    main()
