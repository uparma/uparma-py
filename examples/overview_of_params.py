#!/usr/bin/env python3
import uparma

def main():
    up = uparma.UParma()
    print('Universal parameter mapper contains {0} styles'.format(
        len(up.available_styles)
    ))

if __name__ == '__main__':
    main()
