from rest_framework.response import Response


def send_emails(func):
    def inner(self, request, *args, **kwargs):
        print(args)
        print(kwargs)

        result: Response = func(self, request, *args, **kwargs)
        return result

    return inner
