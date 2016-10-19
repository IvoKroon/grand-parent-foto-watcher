from django.core.files.storage import FileSystemStorage
from base.functions import randomHash
from database.models import Photos, User
import PIL
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
# import os


class ImageUploader:

    def __init__(self):
        # standard stuff
        self.image_path = 'media'
        self.image_thumbnail_path = 'media/thumbnail'
        self.max_photo_size = 4 * 1024 * 1024  # 4MB
        self.mime_list = ['image/png', 'image/jpeg', 'image/gif']
        self.extension_list = ['png', 'PNG', 'jpeg', 'jpg', 'JPG', 'gif']
        self.dir_path = '/www/website/media/'
        self.dir_path_thumbnail = '/www/website/media/thumbnail/'
        self.upload_memberships = {1: 1 * 1024 * 1024 * 1024, 2: 2 * 1024 * 1024 * 1024, 3: 5 * 1024 * 1024 * 1024}
        self.size_thumbnail = 250

    def upload(self, image, desc, title, user_id):
        name_parts = image.name.split('.')
        extension = name_parts[len(name_parts) - 1]
        # Check if the image is a an images.
        # Check if the image approved to upload
        if self.check_image(extension, image, image.size, user_id):
            # Build the new name for the image
            # This is against over rinding.
            new_name = self.image_name_builder(extension)
            print 'Uploading...'
            self.image_uploader('media', new_name, image)
            self.make_thumbnail(new_name)
            self.save_to_database(new_name, title, desc, image.size, user_id)
            return True

    def check_image(self, extension, image, size, user_id):

        if self.check_extension(extension):
            print 'Checked extension!'
            if self.check_mime_image(image.content_type):
                if size < self.max_photo_size:
                    if self.check_user_can_upload(size, user_id):
                        return True
        return False

    def check_extension(self, extension):
        for ext in self.extension_list:
            if extension == ext:
                return True
        return False

    def check_mime_image(self, content_type):
        for mime in self.mime_list:
            if content_type == mime:
                return True
        return False

    def check_user_can_upload(self, size, user_id):
        uploaded_images = Photos.objects.filter(user=user_id)
        amount = 0
        for image in uploaded_images:
            amount += image.size

        if amount + size > self.get_amount_user_can_upload(user_id):
            return False
        else:
            return True

    def get_amount_user_can_upload(self, user_id):
        user = User.objects.get(id=user_id)
        member_id = user.member_id
        return self.upload_memberships[member_id]

    @classmethod
    def image_name_builder(cls, extension):
        title = randomHash.RandomHash.generate()
        new_name = title + '.' + extension
        return new_name

    @classmethod
    def image_uploader(cls, dirname, name, image):
        fs = FileSystemStorage(dirname)
        fs.save(name, image)

    def make_thumbnail(self, image_name):
        img = Image.open(self.dir_path + image_name)
        img = img.resize((self.size_thumbnail, self.size_thumbnail), PIL.Image.ANTIALIAS)
        img.save(self.dir_path_thumbnail + image_name)

    @classmethod
    def save_to_database(cls, new_name, title, desc, size, user_id):
        # TODO get description and title
        user = User.objects.get(id=user_id)
        photo = Photos()
        photo.title = title
        photo.desc = desc
        photo.src = new_name
        photo.size = size
        photo.user = user
        photo.save()

    @classmethod
    def remove(cls, photo_id, user_id):

        if cls.check_if_photo_exists(photo_id, user_id):
            photo = Photos.objects.filter(user=User.objects.get(id=user_id)).get(id=photo_id)
            src = photo.src
            fs = FileSystemStorage("media")
            fs_thumb = FileSystemStorage("media/thumbnail")
            if fs.exists(src):
                if fs_thumb.exists(src):
                    fs_thumb.delete(src)
                    fs.delete(src)
                    photo.delete()
                    return True

        return False

    @classmethod
    def check_if_photo_exists(cls, photo_id, user_id):
        try:
            Photos.objects.filter(user=User.objects.get(id=user_id)).get(id=photo_id)
            return True
        except ObjectDoesNotExist:
            return False
