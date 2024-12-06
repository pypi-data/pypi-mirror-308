class CW:
    """

    An interface to cwdaemon and PyWinkeyerSerial

    servertype: int 1=cwdaemon, 2=pywinkeyer, 3=rigctld

    """

    def __init__(self, servertype: int, host: str, port: int) -> None:
        self.servertype = servertype
        self.cat = None
        self.host = host
        self.port = port
        self.speed = 20
        self.winkeyer_functions = []

    def __check_sane_ip(self, ip: str) -> bool:
        """check if IP address look normal"""
        print(f"{type(self.host)} {self.host}")

        x = ip.split(".")

        print(f"{x=} {len(x)=}")

        if len(x) != 4:
            return False
        for y in x:
            if not y.isnumeric():
                return False
        return True

    def test(self):
        """"""
        print(f"{self.__check_sane_ip(self.host)=}")


x = CW(1, "127.0.0.1", 6789)
x.test()
