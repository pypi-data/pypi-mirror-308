import sys
from .browser import Browser

if len(sys.argv) > 1:
    browser = Browser(sys.argv[1], slowly=False, headless=False)
    browser.open('/')
    browser.breakpoint()
    browser.close()
else:
    print('Inform the base URL')
