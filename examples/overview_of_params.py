#!/usr/bin/env python3
from uparma.uparma import UParma as UP


def main():
    up = UP()
    print('Universal parameter mapper contains {0} styles'.format(
        len(up.available_styles)
    ))

if __name__ == '__main__':
    main()
