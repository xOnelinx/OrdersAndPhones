import re

from rest_framework import serializers

from orders.models import Orders, Phones


class OrderSerializer(serializers.ModelSerializer):
    """
    Этот сериалайзер не обладает полями как на repetitors.info, считаю их избыточными для тестовой задачи
    """
    phones = serializers.CharField(max_length=1024)

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        for phone in self.validated_data['phones']:
            obj, created = Phones.objects.get_or_create(phone=phone)
            instance.phones.add(obj)

        return instance

    def validate(self, attrs):
        phone_string = attrs.get('phones')
        phones = re.findall(r'[0-9]?\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})', phone_string)
        phone_string = re.sub(r'[0-9]?\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})', '', phone_string)
        home_phones = [('495',) + numbers for numbers in
                       re.findall(r'[^\d]([0-9]{3})([ .-]?)([0-9]{4})\b', phone_string)]
        phones.extend(home_phones)
        phones = [''.join(('8',) + number) for number in phones]
        phones = [re.sub(r'[ .-]', '', number) for number in phones]
        if phones:
            attrs['phones'] = phones
        else:
            raise serializers.ValidationError("No phone numbers are found, try '8KKKNNNNNNN, 8KKKNNNNNNN'")
        return super().validate(attrs)

    class Meta:
        model = Orders
        fields = ('phones',)
