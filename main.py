# -*- coding: utf-8 -*-

import sys,os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher

def toDec(dec, padding):
    return ("{dec:0{padding}d}".format(dec=dec, padding=padding), "Dec")


def toHex(dec, padding):
    return ("0x{dec:0{padding}x}".format(dec=dec, padding=padding), "Hex")


def toOct(dec, padding):
    return ("0{dec:0{padding}o}".format(dec=dec, padding=padding), "Oct")


def toBin(dec, padding):
    return ("0b{dec:0{padding}b}".format(dec=dec, padding=padding), "Bin")


def getDec(arg):
    if arg.startswith("0x") or arg.startswith("0X"):
        return (int(arg, 16), "Hex")
    elif arg.startswith("0b") or arg.startswith("0B"):
        return (int(arg, 2), "Bin")
    elif arg.startswith("0"):
        return (int(arg, 8), "Oct")
    else:
        return (int(arg, 10), "Dec")


class NumberConverter(FlowLauncher):
    converters = [toDec, toHex, toBin, toOct]

    def query(self, query):
        results = []
        if len(query) == 0:
            return results
        try:
            decResult = getDec(query)
            for func in self.converters:
                result = func(decResult[0], 1)
                if result[1] != decResult[1]:
                    results.append({
                        "Title": result[0],
                        "SubTitle": "{t}".format(t=result[1]),
                        "IcoPath": "Images/app.png",
                        'JsonRPCAction': {
                            'method': 'copyToClipboard',
                            'parameters': [result[0]],
                            'dontHideAfterAction': False
                        }
                    })
                pass
        except Exception as e:
            results = []
            results.append({
                "Title": "Invalid parameters",
                "SubTitle": "Please try again",
                "IcoPath": 'Images/app.png'
            })
            return results
        return results

    def copyToClipboard(self, value):
        command = 'echo|set /p={v}|clip'.format(v=value.strip())
        os.system(command)


if __name__ == "__main__":
    NumberConverter()
