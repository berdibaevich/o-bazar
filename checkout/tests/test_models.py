from checkout.models import Delivery
import pytest



# TEST MODEL
@pytest.mark.django_db
def test_delivery_model(client, get_deliveries):
    new_deliveries = get_deliveries
    deliveries = Delivery.objects.all()
    assert deliveries.count() == len(new_deliveries)
    assert deliveries.first().__str__() == new_deliveries[0].__str__()
# END TEST MODEL