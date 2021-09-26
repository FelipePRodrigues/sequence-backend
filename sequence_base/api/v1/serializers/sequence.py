from rest_framework import serializers

from sequence_base.models import Sequence


class SequenceCreateSerializer(serializers.Serializer):
    letters = serializers.ListField(required=True)

    def validate(self, data):
        MINIMUM = 4
        AVAILABLE_LETTERS = ['B', 'U', 'D', 'H']

        letters = data['letters']

        if not letters:
            raise serializers.ValidationError({
                "letters": 'This field must not be an empty array.'
            })

        lines_count = len(letters)
        if lines_count < MINIMUM:
            raise serializers.ValidationError({
                "letters": 'This field must represent a square matrix, with at least 4 rows and columns.'
            })

        for word in letters:
            if not isinstance(word, str):
                raise serializers.ValidationError({
                    "letters": 'This field must be an array of strings.'
                })

            columns_count = len(word)
            if lines_count != columns_count or lines_count < MINIMUM:
                raise serializers.ValidationError({
                    "letters": 'This field must represent a square matrix, with at least 4 rows and columns.'
                })

            for letter in word:
                if letter not in AVAILABLE_LETTERS:
                    raise serializers.ValidationError({
                        "letters": 'This field contains invalid letters.'
                    })

        return data
