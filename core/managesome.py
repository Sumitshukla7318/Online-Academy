import os
import sys

# Make sure the Django project root is in sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineAcademy.settings')

import django
django.setup()

from django.core.files import File
from django.conf import settings
from courses.models import Course

# Define the path to your image folder
media_folder = os.path.join(settings.MEDIA_ROOT, 'course_thumbnails')

# Loop through each Course
for course in Course.objects.all():
    old_thumb = course.thumbnail.name  # e.g. course_thumbnails/cjhlrxmvn4mf5htg5mh2
    file_only = os.path.basename(old_thumb)

    # If no extension (looks like Cloudinary ID)
    if '.' not in file_only:
        # Convert course title into a possible filename
        base_filename = course.title.lower().replace(' ', '_')

        # Try to find matching file
        matched_file = None
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            filename = f"{base_filename}{ext}"
            full_path = os.path.join(media_folder, filename)
            if os.path.exists(full_path):
                matched_file = filename
                break

        if matched_file:
            with open(os.path.join(media_folder, matched_file), 'rb') as f:
                course.thumbnail.save(matched_file, File(f), save=True)
            print(f"✅ Updated: {course.title} -> {matched_file}")
        else:
            print(f"❌ Image not found for: {course.title}")
    else:
        print(f"⏭️ Already correct: {course.title}")