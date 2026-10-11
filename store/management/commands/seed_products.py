from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Product

PRODUCTS = [
    ("Wireless Headphones", "wireless-headphones", "Comfortable over-ear headphones with rich sound and long battery life.", "2499.00", "Electronics", 20, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80"),
    ("Everyday Backpack", "everyday-backpack", "A durable, minimalist backpack for commuting, college, and weekend trips.", "1799.00", "Accessories", 15, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80"),
    ("Classic Wristwatch", "classic-wristwatch", "A clean everyday watch design that pairs with casual and formal outfits.", "3299.00", "Accessories", 12, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80"),
    ("Running Sneakers", "running-sneakers", "Lightweight sneakers designed for daily walks, gym sessions, and running.", "2899.00", "Footwear", 18, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80"),
    ("Ceramic Coffee Mug", "ceramic-coffee-mug", "A sturdy ceramic mug for your morning coffee, tea, or hot chocolate.", "399.00", "Home", 30, "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=900&q=80"),
    ("Desk Lamp", "desk-lamp", "A modern desk lamp that creates a comfortable workspace lighting setup.", "1299.00", "Home", 10, "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80"),
    ("Smartphone Stand", "smartphone-stand", "A compact adjustable stand for video calls, streaming, and desk use.", "499.00", "Electronics", 25, "https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=900&q=80"),
    ("Cotton T-Shirt", "cotton-t-shirt", "A soft cotton everyday T-shirt with a simple, versatile fit.", "699.00", "Clothing", 35, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80"),
    (
                "Naruto Shinobi Headband",
                "naruto-shinobi-headband",
                "A cosplay-inspired forehead protector for Naruto fans.",
                "599.00",
                "Naruto",
                24,
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?auto=format&fit=crop&w=900&q=80"
            ),
            (
                "Anime Ninja Collectible Figure",
                "anime-ninja-figure",
                "A collectible anime-inspired ninja figure for your desk or shelf.",
                "1499.00",
                "Naruto",
                12,
                "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=900&q=80"
            ),
            (
                "Pirate Crew Poster",
                "pirate-crew-poster",
                "An adventure-inspired poster for anime fans.",
                "349.00",
                "One Piece",
                30,
                "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=900&q=80"
            ),
            (
                "Anime Graphic Hoodie",
                "anime-graphic-hoodie",
                "A comfortable graphic hoodie for everyday fandom style.",
                "1899.00",
                "Demon Slayer",
                14,
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80"
            ),
            (
                "Saiyan Graphic T-Shirt",
                "saiyan-graphic-tshirt",
                "A graphic T-shirt inspired by high-energy anime battles.",
                "799.00",
                "Dragon Ball",
                22,
                "https://images.unsplash.com/photo-1503341504253-dff4815485f1?auto=format&fit=crop&w=900&q=80"
            ),
            (
                "Anime Sticker Pack",
                "anime-sticker-pack",
                "Anime-style stickers for laptops, notebooks, and bottles.",
                "199.00",
                "Accessories",
                50,
                "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80"
            ),
]

class Command(BaseCommand):
    help = "Create or update demo products."

    def handle(self, *args, **options):
        for name, slug, description, price, category, stock, image_url in PRODUCTS:
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name, "description": description, "price": price,
                    "category": category, "stock": stock, "image_url": image_url,
                    "is_active": True,
                },
            )
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(PRODUCTS)} demo products."))
        