from functools import wraps


def has_required_params(method):
    @wraps(method)
    def decorator(self, *method_args, **method_kwargs):
        for argument in method_args:
            for param in self.required_params:
                if param not in argument.keys():
                    raise Exception("The request does not have all required params")
        return method(self, *method_args, **method_kwargs)
    return decorator
