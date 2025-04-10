from rest_framework import serializers

from ads.models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_name = serializers.StringRelatedField(source='user', read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ('status',)


class ProposalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ('comment', 'ad_sender', 'ad_receiver')
