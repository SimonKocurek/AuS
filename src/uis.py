# coding=utf-8

from src import webapp

port = 5431
domain = 'localhost'


def main():
    """ Starting method """
    webapp.app.run(port=port, debug=False)


if __name__ == "__main__":
    main()
