from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from orders.models import Orders
from orders.seriolizers import OrderSerializer


class OrderSerializerTestCase(TestCase):

    def test_serializer_not_valid(self):
        """ If no phone numbers are found should raise ValidationError """
        data = {'phones': 'личный+797882'}
        serializer = OrderSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(serializer.errors,
                         {'non_field_errors':
                              [ErrorDetail(string="No phone numbers are found, try '8KKKNNNNNNN, 8KKKNNNNNNN'",
                                           code='invalid')]},
                         msg=serializer.errors)

    def test_serializer(self):
        """ Serializer should validate and parse all phone numbers """
        data = {'phones': 'личный+79788222521 рабочий(123) 456 7899, ljvfiybq:4567899 рабочий2:356-9877, 765-123-1234'}
        serializer = OrderSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(serializer.validated_data['phones'],
                         ['89788222521', '81234567899', '87651231234', '84954567899', '84953569877'],
                         msg=serializer.validated_data)

    def test_model_saved(self):
        """ Order model should have right phones """
        data = {
            'phones': 'типичный 89031110022 личный +7 978 822 2521 рабочий(123)'
                      ' 456 7899, рабочий2:356-9877, 765-123-1234'}
        serializer = OrderSerializer(data=data)
        serializer.is_valid()
        order = serializer.save()
        self.assertEqual([obj.phone for obj in order.phones.all()],
                         ['89031110022', '89788222521', '81234567899', '87651231234', '84953569877'])

    def test_find_another_order(self):
        """ Test can we find order with same phone numbers """
        data1 = {
            'phones': 'типичный 89031110022 личный +7 978 822 2521 рабочий(123)'
                      ' 456 7899, рабочий2:356-9877, 765-123-1234'}
        serializer = OrderSerializer(data=data1)
        serializer.is_valid()
        order1 = serializer.save()

        data2 = {
            'phones': 'типичный 89031110022'}
        serializer = OrderSerializer(data=data2)
        serializer.is_valid()
        order2 = serializer.save()

        self.assertEqual(Orders.objects.count(), 2)
        self.assertTrue(Orders.objects.filter(phones__in=order1.phones.all()).exclude(id=order1.id).exists())
