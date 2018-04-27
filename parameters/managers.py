from base.managers import QuerySet


class ParameterQuerySet(QuerySet):

    def search(self, query):
        """
        Search Parameter objects by name
        """
        if query:
            # TODO implement this method, since this is an example
            return self.filter(
                name__unaccent__icontains=query
            )
