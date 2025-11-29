from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample data for listings, bookings, and reviews'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create sample users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f'host{i+1}',
                email=f'host{i+1}@example.com',
                password='password123',
                first_name=f'Host{i+1}',
                last_name='User'
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')
        
        # Create sample guest user
        guest_user = User.objects.create_user(
            username='guest1',
            email='guest1@example.com',
            password='password123',
            first_name='Guest',
            last_name='User'
        )
        users.append(guest_user)
        
        # Sample listing data
        listings_data = [
            {
                'title': 'Cozy Apartment in Downtown',
                'description': 'A beautiful cozy apartment located in the heart of downtown. Perfect for couples or solo travelers.',
                'address': '123 Main Street',
                'city': 'New York',
                'country': 'USA',
                'price_per_night': 120.00,
                'max_guests': 2,
                'bedrooms': 1,
                'bathrooms': 1,
                'property_type': 'apartment',
                'amenities': 'WiFi,Kitchen,Air Conditioning,TV',
            },
            {
                'title': 'Luxury Villa with Ocean View',
                'description': 'Stunning luxury villa with breathtaking ocean views. Private pool and modern amenities.',
                'address': '456 Ocean Drive',
                'city': 'Miami',
                'country': 'USA',
                'price_per_night': 350.00,
                'max_guests': 6,
                'bedrooms': 3,
                'bathrooms': 2,
                'property_type': 'villa',
                'amenities': 'Pool,WiFi,Kitchen,Air Conditioning,TV,Garden',
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Escape to this peaceful mountain cabin surrounded by nature. Perfect for hiking and relaxation.',
                'address': '789 Mountain Road',
                'city': 'Aspen',
                'country': 'USA',
                'price_per_night': 180.00,
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 1,
                'property_type': 'cabin',
                'amenities': 'Fireplace,WiFi,Kitchen,Garden',
            },
            {
                'title': 'Modern City Condo',
                'description': 'Sleek modern condo with amazing city views. Close to all attractions and public transport.',
                'address': '321 Urban Avenue',
                'city': 'San Francisco',
                'country': 'USA',
                'price_per_night': 200.00,
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 2,
                'property_type': 'condo',
                'amenities': 'WiFi,Kitchen,Air Conditioning,TV,Gym',
            },
            {
                'title': 'Family-Friendly House',
                'description': 'Spacious house perfect for families. Large backyard and close to parks and schools.',
                'address': '654 Family Lane',
                'city': 'Chicago',
                'country': 'USA',
                'price_per_night': 220.00,
                'max_guests': 8,
                'bedrooms': 4,
                'bathrooms': 3,
                'property_type': 'house',
                'amenities': 'WiFi,Kitchen,Air Conditioning,TV,Garden,Playground',
            },
        ]
        
        # Create listings
        listings = []
        for i, data in enumerate(listings_data):
            listing = Listing.objects.create(
                **data,
                host=users[i % len(users)]
            )
            listings.append(listing)
            self.stdout.write(f'Created listing: {listing.title}')
        
        # Create sample bookings
        statuses = ['pending', 'confirmed', 'completed']
        for i in range(10):
            listing = random.choice(listings)
            guest = random.choice(users)
            check_in = datetime.now().date() + timedelta(days=random.randint(1, 30))
            check_out = check_in + timedelta(days=random.randint(1, 7))
            
            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in=check_in,
                check_out=check_out,
                total_price=listing.price_per_night * (check_out - check_in).days,
                guests_count=random.randint(1, min(3, listing.max_guests)),
                status=random.choice(statuses),
                special_requests='Sample special request' if random.choice([True, False]) else ''
            )
            self.stdout.write(f'Created booking: {booking}')
        
        # Create sample reviews
        for listing in listings:
            for i in range(random.randint(1, 3)):
                guest = random.choice(users)
                review = Review.objects.create(
                    listing=listing,
                    guest=guest,
                    rating=random.randint(3, 5),
                    comment=f'Great stay at {listing.title}! Would definitely recommend.'
                )
                self.stdout.write(f'Created review: {review}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with:')
        )
        self.stdout.write(f'  - {User.objects.count()} users')
        self.stdout.write(f'  - {Listing.objects.count()} listings')
        self.stdout.write(f'  - {Booking.objects.count()} bookings')
        self.stdout.write(f'  - {Review.objects.count()} reviews')