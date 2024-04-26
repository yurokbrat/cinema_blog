from wagtail.api.v2.serializers import StreamField


class StreamFieldSerializer(StreamField):
    def to_representation(self, value, context=None):
        # blocks = []
        # for block in value:
        #     block_type = block.block_type
        #     block_value = block.value
        #     api_representation = block.block.get_api_representation(block_value, self.context)
        #     blocks.append({"type": block_type, "value": api_representation})
        # return blocks
        blocks = []
        for block in value:
            block_type = block.block_type
            block_value = block.value
            if hasattr(block.block, "get_api_representation"):
                api_representation = block.block.get_api_representation(block_value, self.context)
                blocks.append({"type": block_type, "value": api_representation})
            blocks.append({"type": block_type, "id": block.id, "value": block.value})
        return blocks
