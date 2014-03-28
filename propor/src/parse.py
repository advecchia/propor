import argparse

class Parse:
    """ A class for manipulating the program input.
    """
    def __init__(self):
        #sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), 'src'))
        pass

    def parse(self):
        parser = argparse.ArgumentParser(description="", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # group 1
#        group1 = parser.add_argument_group("group name","infos")
#        group1.add_argument(MIN_PORT, PORT, dest=PORT, nargs=1, metavar="number", default=DEFAULT_PORT, help="infos")
        # group 2
#        group2 = parser.add_argument_group("group name","infos")
#        group2.add_argument(MIN_PORT, PORT, dest=PORT, nargs=1, metavar="number", default=DEFAULT_PORT, help="infos")

#        args = parser.parse_args()
#        params = vars(args)
# 
#         #"""
#         # Removes the parameter not inserted in the input
#         for key,value in params.items():
#             if value is None:
#                 del params[key]
#             elif not isinstance(value, list):
#                 params[key] = []
#                 params[key].append(value)
#         #"""
#         return params