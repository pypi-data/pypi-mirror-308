# import importlib as _importlib

# submodules = [
#     'formats',
#     'plotting',
# ]


# def __dir__():
#     return submodules


# def __getattr__(name):
#     if name in submodules:
#         return _importlib.import_module(f'scipy.{name}')
#     else:
#         try:
#             return globals()[name]
#         except KeyError:
#             raise AttributeError(
#                 f"Module 'scipy' has no attribute '{name}'"
#             )