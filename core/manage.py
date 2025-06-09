import os
import cloudinary
from django.conf import settings
from cloudinary.uploader import upload
from courses.models import Course  # change if needed

# Set Cloudinary credentials manually
cloudinary.config( 
  cloud_name = "dmqsvbyfz",  
  api_key = "516322764339631",  
  api_secret = "u53P24XJ63Tu9wtwNa14-y9zem0"  
)

# Upload local thumbnails
for course in Course.objects.all():
    thumbnail = course.thumbnail
    if thumbnail and not str(thumbnail).startswith("http"):
        local_path = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
        if os.path.exists(local_path):
            print(f"📤 Uploading {local_path}...")
            result = upload(local_path)
            course.thumbnail = result['secure_url']
            course.save()
            print(f"✅ Uploaded: {result['secure_url']}")
        else:
            print(f"❌ Not found: {local_path}")
