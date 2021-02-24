#!/usr/bin/env python3
import uparma


def main():
    up = uparma.UParma()
    print("Universal parameter mapper contains:")
    print(f"\t{len(up.available_styles)} styles")
    print(f"\t{len(up.parameters)} parameters")


if __name__ == '__main__':
    main()
