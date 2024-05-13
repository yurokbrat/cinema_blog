from wagtail.api.v2.serializers import StreamField


class StreamFieldSerializer(StreamField):
    def to_representation(self, value, context=None):
        blocks = []
        for block in value:
            api_representation = block.block.get_api_representation(block.value, self.context)
            if isinstance(api_representation, dict):
                blocks.append({
                    "type": block.block_type,
                    "value": api_representation,
                })
            else:
                blocks.append({
                    "type": block.block_type,
                    "id": block.id,
                    "value": api_representation,
                })
        return blocks
