from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER

import os
from PIL import Image
import random, string

from .models import Picture, Farm
from processing.models import ProcessedData
from processing import script

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@receiver(post_save, sender=Farm)
def farm_save_handler(sender, instance, created, **kwargs):
    if created:
        instance.farm_lookup = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        subject = 'New Farm'
        message = f'{instance.farm_lookup}'
        recp = 'hunainahmed6@gmail.com'
        try: 
            send_mail(subject, message, EMAIL_HOST_USER, [recp], fail_silently=False)
        except:
            print("Mail not sent.")
        finally:
            instance.save()


@receiver(post_save, sender=Picture)
def data_process_handler(sender, instance, created, **kwargs):
    if created:

        path = "farm/media/arial_shots/"
        media_path = "arial_shots/"
        new_data = {}
        full_paths = {}

        for attr, value in instance.__dict__.items():
            if attr.startswith('resource'):
                if value:

                    splited_array = str(value).split("/")
                    further_splited = splited_array[2].split(".")

                    resource_type = splited_array[1]
                    file_name = further_splited[0]
                    file_ext = further_splited[1]
                    full_path = f"{path}{resource_type}/{file_name}.{file_ext}"
                    half_path = f"{media_path}{resource_type}/{file_name}.jpeg"

                    new_data[attr] = half_path
                    full_paths[attr] = full_path
                    
                    resource = Image.open(os.path.join(BASE_DIR, full_path))
                    # resource = Image.open('media/arial_shots/REG/IMG_160808_092611_0000_REG_5Hn30y3.TIF')
                    resource.mode = 'I'
                    resource.point(lambda i: i * (1. / 256)).convert('L').save(os.path.join(BASE_DIR, path)+resource_type+"/"+file_name+'.jpeg')

        # # ***********************************s

        instance.resource_GRE = new_data['resource_GRE']
        instance.resource_NIR = new_data['resource_NIR']
        instance.resource_RED = new_data['resource_RED']
        instance.resource_REG = new_data['resource_REG']
        instance.save()

        data = script.Data(
            full_paths['resource_GRE'],
            full_paths['resource_NIR'],
            full_paths['resource_RED'],
            full_paths['resource_REG']
        )

        processed_data = ProcessedData(
            farm=instance.farm_id,
            picture=instance,
            ndvi=data.calculate_ndvi(),
            ndre=data.calculate_ndre(),
            grvi=data.calculate_grvi(),
            gci=data.calculate_gci()
        )

        processed_data.save()







