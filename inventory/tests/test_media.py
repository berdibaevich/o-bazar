from inventory.models import Media


# TEST MEDIA TABLE


# TEST CREATE MEDIA
def test_create_media(get_media):
    new_media = get_media
    media = Media.objects.first()
    assert media.is_feature == new_media.is_feature
    assert media.image == new_media.image
# END TEST CREATE MEDIA



# END TEST MEDIA TABLE 