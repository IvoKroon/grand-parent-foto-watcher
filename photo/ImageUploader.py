from django.core.files.storage import FileSystemStorage
from base.functions import randomHash
from database.models import Photos


class ImageUploader():

    def __init__(self, image):
        self.image = image
        self.name = image.name
        self.size = image.size
        self.content_type = image.content_type

        self.image_path = 'media'
        self.image_thumbnail_path = 'media/thumbnail'
        self.max_size = 4 * 1024 * 1024  # 4MB
        self.mime_list = ['image/png', 'image/jpeg', 'image/gif']
        self.extension_list = ['png', 'jpeg', 'jpg', 'gif']

    def check_mime_image(self):
        for mime in self.mime_list:
            if self.content_type == mime:
                return True

        return False

    def check_extension(self):
        string_array = self.name.split('.')
        amount = len(string_array)
        extension = string_array[amount - 1]
        for ext in self.extension_list:
            if extension == ext:
                return True

        return False

    def image_name_builder(self):
        string_array = self.name.split('.')
        amount = len(string_array)
        extension = string_array[amount - 1]

        title = randomHash.RandomHash.generate()
        new_name = title + '.' + extension
        return new_name

    def image_uploader(self, dirname, name):
        fs = FileSystemStorage(dirname)
        fs.save(name, self.image)

    def save_to_database(self, new_name):
        photo = Photos()
        photo.title = self.name
        photo.desc = "bla bla"
        photo.src = new_name
        photo.size = self.size
        photo.save()

    def upload(self):
        print 'uploading...'

        if self.check_extension():
            print 'Checked extension!'
            if self.check_mime_image():
                if self.size < self.max_size:
                    # TODO check if user is able to upload more.
                    # TODO put user id with uploaded photo.
                    # TODO make photo pages.
                    # TODO crop thumbnail image for faster loading.
                    new_name = self.image_name_builder()
                    self.image_uploader('media/thumbnail', new_name)
                    self.image_uploader('media', new_name)
                    self.save_to_database(new_name)






