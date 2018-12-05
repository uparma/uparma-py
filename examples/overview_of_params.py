<<<<<<< HEAD
import uparma
=======
#!/usr/bin/env python3
from uparma.uparma import UParma as UP

>>>>>>> 4657e70e95eae7004fabf092875f35a4dda32cc7

def main():
    up = uparma.UParma()
    print('Universal parameter mapper contains {0} styles'.format(
        len(up.available_styles)
    ))

if __name__ == '__main__':
    main()
