from base.managers import QuerySet


class {{model_name}}QuerySet(QuerySet):

    def search(self, query):
        """
        Search {{model_name}} objects by name
        """
        if query:
            # TODO implement this method, since this is an example
            return self.filter(
                name__unaccent__icontains=query
            )
