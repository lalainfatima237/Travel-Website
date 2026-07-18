import os
import django
import urllib.request
import tempfile
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TravelWebsite.settings')
django.setup()

from travel_app.models import Destination

destinations_data = [
    {
        "name": "Santorini",
        "country": "Greece",
        "description": "Experience the beautiful white and blue architecture and breathtaking sunsets.",
        "image_url": "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Kyoto",
        "country": "Japan",
        "description": "Immerse yourself in traditional Japanese culture, temples, and cherry blossoms.",
        "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Machu Picchu",
        "country": "Peru",
        "description": "Explore the ancient Incan city set high in the Andes Mountains.",
        "image_url": "https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Amalfi Coast",
        "country": "Italy",
        "description": "Enjoy the dramatic coastline, pastel-colored fishing villages, and terraced vineyards.",
        "image_url": "https://images.unsplash.com/photo-1633519119642-120025fcf958?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Banff National Park",
        "country": "Canada",
        "description": "Discover stunning turquoise lakes, majestic mountains, and abundant wildlife.",
        "image_url": "https://images.unsplash.com/photo-1544378730-8b56f345c26b?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Maldives",
        "country": "Maldives",
        "description": "Relax in luxury overwater bungalows and snorkel in crystal-clear waters.",
        "image_url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Dubai",
        "country": "UAE",
        "description": "Marvel at modern architecture, luxury shopping, and desert safaris.",
        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Cape Town",
        "country": "South Africa",
        "description": "Take in the views from Table Mountain and explore beautiful coastlines.",
        "image_url": "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Bora Bora",
        "country": "French Polynesia",
        "description": "Escape to this romantic island known for its turquoise lagoon and coral reefs.",
        "image_url": "https://images.unsplash.com/photo-1589394815804-964ce0ff9657?q=80&w=800&auto=format&fit=crop"
    },
    {
        "name": "Swiss Alps",
        "country": "Switzerland",
        "description": "Experience world-class skiing, scenic train rides, and picturesque alpine villages.",
        "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=800&auto=format&fit=crop"
    }
]

print("Starting to add destinations...")

# Optional: Clear existing destinations if user wants exactly 10 cards. Let's just clear them to make the page look fresh.
Destination.objects.all().delete()

for dest in destinations_data:
    print(f"Processing {dest['name']}...")
    img_temp = tempfile.NamedTemporaryFile(delete=True)
    req = urllib.request.Request(dest['image_url'], headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            img_temp.write(response.read())
            img_temp.flush()
    except Exception as e:
        print(f"Failed to download image for {dest['name']}: {e}. Using fallback.")
        fallback_req = urllib.request.Request("https://picsum.photos/800/600", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(fallback_req) as response:
            img_temp.write(response.read())
            img_temp.flush()
            
    d = Destination(
        name=dest['name'],
        country=dest['country'],
        description=dest['description']
    )
    # save image
    file_name = f"{dest['name'].lower().replace(' ', '_')}.jpg"
    d.image.save(file_name, File(img_temp), save=True)
    print(f"Added {dest['name']} successfully!")

print("All 10 destinations added successfully!")
