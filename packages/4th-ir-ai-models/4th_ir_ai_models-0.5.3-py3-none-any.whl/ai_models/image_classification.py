from enum import Enum


class ImageClassificationModel(str, Enum):
    """Defines AI Models that can be used"""

    clip_vit = "https://image-class-openai-clip-vit.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    document_finetuned_rvlcdip = "https://image-c-document-finetuned.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    efficientnet_b1 = "https://image-class-efficientnet.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"
    facebook_diet_small_distelled = "https://image-class-fb-diet-small-dist.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
    facebook_levit = "https://image-class-facebook-levit.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"
    microsoft_swin_base = "https://image-class-microsoft-swin-base.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"
    clip_vit_base_patch32 = "https://image-classification-clip-vit.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"
    resnet50_1 = "https://image-class-resnet.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"


class AgeClassificationModel(str, Enum):
    google_vit_base = "https://image-vit-age-classifier.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
