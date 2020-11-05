class ListAttr(list):
    """List with attributes support"""

    attrs = {}

    def __getattr__(self, name):
        if name in self.attrs:
            return self.attrs[name]
        else:
            return super().__getattr__(name)

    def __setattr__(self, name, value):
        self.attrs[name] = value


def main():
    l = ListAttr()
    l.append(100)
    l.a = 4
    print(l)
    print(l.a)
    l.order = 'reversed'
    print(l.order)


if __name__ == "__main__":
    main()
