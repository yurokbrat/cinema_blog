from kino.cards.tests.utils.base_api_card import BaseAPICard


class BaseCheckFields(BaseAPICard):
    def check_fields_in_detail(self, fields, response):
        for field in fields:
            self.assertIn(
                field,
                response.data,
                f"В ответе отсутствует поле '{field}'",
            )

    def check_fields_in_list(self, fields, response):
        for result in response.data["results"]:
            for field in fields:
                self.assertIn(
                    field,
                    result,
                    f"В ответе отсутствует поле '{field}'",
                )

    def check_list_fields_is_not_retrieve_fields(self, fields_detail, fields_list, response):
        for result in response.data["results"]:
            for field in fields_detail:
                if field not in fields_list:
                    self.assertNotIn(
                        field,
                        result,
                        f"В отображении списка присутствует "
                        f"поле для детального отображения: '{field}'",
                    )
