# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.dev@gmail.com>


"""Sophisticate Sorting Algorithms"""


from time import sleep
from pyfiglet import figlet_format
from pynput.keyboard import Key, Listener
from heep import minBinaryHeap, maxBinaryHeap
from typing import Any, List, Self, Iterable, NoReturn
from hashtbl import tabulate, hashMap, _blue, _cyan, _green, _red, _white


__all__: List = ["sortVisualizer"]


class sortVisualizer:
    def __init__(
        self: "sortVisualizer",
        data: Iterable,
        *,
        reverse: bool = False,
        speed: int = 1,
        control: bool = False,
        page_control: bool = False
    ) -> None:
        self.data: List = data
        self.reverse: bool = reverse
        self.speed: int = speed
        if (control and page_control) or (not control and page_control):
            self.control: bool = False
            self.page_control: bool = page_control
            self.running: None = None
            self.keyboard_listener: None = None
        else:
            self.control: bool = control
            self.page_control: bool = page_control

    @property
    def data(self: "sortVisualizer") -> Self:
        return self

    @data.setter
    def data(self: "sortVisualizer", data: Iterable) -> None | NoReturn:
        try:
            self._data: List = list(data)
        except TypeError as e0:
            raise ValueError("Invalid data type !") from None

    @data.deleter
    def data(self: "sortVisualizer") -> NoReturn:
        raise ValueError("read-only")

    @property
    def speed(self: "sortVisualizer") -> int:
        return self._speed

    @speed.setter
    def speed(self: "sortVisualizer", speed: int) -> None | NoReturn:
        if speed < 1:
            raise ValueError("The speed must be greater than zero !")
        self._speed: int = speed

    @speed.deleter
    def speed(self: "sortVisualizer") -> NoReturn:
        raise ValueError("read-only")

    def on_press(self: "sortVisualizer", key: Any) -> bool | None:
        if key == Key.page_down:
            self.running: bool = False
            return False
        elif key == Key.page_up:
            self.running: bool = False
            self.page_control: bool = False
            return False

    def selection_sort(self: "sortVisualizer") -> List | NoReturn | None:
        try:
            output: List = [[_blue(item) for item in self._data]]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            if len(self._data) > 1:
                if self.reverse:
                    print(_white("Max value :"), _cyan("?"))
                else:
                    print(_white("Min value :"), _cyan("?"))
                if self.control:
                    while True:
                        try:
                            response: str = input(
                                _cyan(
                                    "Press Enter to continue, Ctrl + D to exit control mode, or Ctrl + C to exit the program...\n"
                                )
                            )
                        except EOFError as e1:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    print(
                        _cyan(
                            "Press Page Down to continue, Page Up to exit page control mode, or Ctrl + C to exit the program..."
                        )
                    )
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
            for i in range(len(self._data) - 1):
                m_value_index: int = i
                output: List = [[_blue(item) for item in self._data]]
                output[0][i] = _green(self._data[i])
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                if self.reverse:
                    print(_white("Max value :"), _cyan(self._data[m_value_index]))
                else:
                    print(_white("Min value :"), _cyan(self._data[m_value_index]))
                if self.control:
                    while True:
                        try:
                            response: str = input()
                        except EOFError as e2:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
                for j in range(i + 1, len(self._data)):
                    output: List = [[_blue(item) for item in self._data]]
                    output[0][i] = _green(self._data[i])
                    output[0][j] = _green(self._data[j])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    if self.reverse:
                        try:
                            if self._data[j] > self._data[m_value_index]:
                                m_value_index: int = j
                        except TypeError as e3:
                            raise TypeError("Invalid values !") from None
                    else:
                        try:
                            if self._data[j] < self._data[m_value_index]:
                                m_value_index: int = j
                        except TypeError as e4:
                            raise TypeError("Invalid values !") from None
                    if self.reverse:
                        print(_white("Max value :"), _cyan(self._data[m_value_index]))
                    else:
                        print(_white("Min value :"), _cyan(self._data[m_value_index]))
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as e5:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
                if (
                    self._data[m_value_index] < self._data[i]
                    or self._data[m_value_index] > self._data[i]
                ):
                    if m_value_index is not j:
                        output: List = [[_blue(item) for item in self._data]]
                        output[0][i] = _red(self._data[i])
                        output[0][m_value_index] = _red(self._data[m_value_index])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"))
                        if self.reverse:
                            print(
                                _white("Max value :"), _cyan(self._data[m_value_index])
                            )
                        else:
                            print(
                                _white("Min value :"), _cyan(self._data[m_value_index])
                            )
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as e6:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        elif self.page_control:
                            self.running: bool = True
                            self.keyboard_listener: Listener = Listener(
                                on_press=self.on_press
                            )
                            self.keyboard_listener.start()
                            while self.running:
                                pass
                        else:
                            sleep(self._speed)
                    else:
                        output: List = [[_blue(item) for item in self._data]]
                        output[0][i] = _red(self._data[i])
                        output[0][m_value_index] = _red(self._data[m_value_index])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"))
                        if self.reverse:
                            print(
                                _white("Max value :"), _cyan(self._data[m_value_index])
                            )
                        else:
                            print(
                                _white("Min value :"), _cyan(self._data[m_value_index])
                            )
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as e7:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        elif self.page_control:
                            self.running: bool = True
                            self.keyboard_listener: Listener = Listener(
                                on_press=self.on_press
                            )
                            self.keyboard_listener.start()
                            while self.running:
                                pass
                        else:
                            sleep(self._speed)
                    if self.reverse:
                        if self._data[m_value_index] > self._data[i]:
                            self._data[i], self._data[m_value_index] = (
                                self._data[m_value_index],
                                self._data[i],
                            )
                    else:
                        if self._data[m_value_index] < self._data[i]:
                            self._data[i], self._data[m_value_index] = (
                                self._data[m_value_index],
                                self._data[i],
                            )
                    output: List = [[_blue(item) for item in self._data]]
                    output[0][i] = _red(self._data[i])
                    output[0][m_value_index] = _red(self._data[m_value_index])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    if self.reverse:
                        print(_white("Max value :"), _cyan(self._data[i]))
                    else:
                        print(_white("Min value :"), _cyan(self._data[i]))
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as e8:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
            output: List = [[_blue(item) for item in self._data]]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            return self._data
        except KeyboardInterrupt as e9:
            print(_cyan("\nI hope you enjoyed learning :)"))

    def bubble_sort(self: "sortVisualizer") -> List | NoReturn | None:
        try:
            output: List = [[_blue(item) for item in self._data]]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            if len(self._data) > 1:
                if self.reverse:
                    print(_white("Max value :"), _cyan("?"))
                else:
                    print(_white("Min value :"), _cyan("?"))
                if self.control:
                    while True:
                        try:
                            response: str = input(
                                _cyan(
                                    "Press Enter to continue, Ctrl + D to exit control mode, or Ctrl + C to exit the program...\n"
                                )
                            )
                        except EOFError as e10:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    print(
                        _cyan(
                            "Press Page Down to continue, Page Up to exit page control mode, or Ctrl + C to exit the program..."
                        )
                    )
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
            for i in range(1, len(self._data)):
                for j in range(len(self._data) - i):
                    output: List = [[_blue(item) for item in self._data]]
                    output[0][j] = _green(self._data[j])
                    output[0][j + 1] = _green(self._data[j + 1])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    if self.reverse:
                        try:
                            print(
                                _white("Max value :"),
                                _cyan(max(self._data[j], self._data[j + 1])),
                            )
                        except TypeError as e11:
                            raise TypeError("Invalid values !") from None
                    else:
                        try:
                            print(
                                _white("Min value :"),
                                _cyan(min(self._data[j], self._data[j + 1])),
                            )
                        except TypeError as e12:
                            raise ValueError("Invalid values !") from None
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as e13:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
                    if self.reverse:
                        if self._data[j] < self._data[j + 1]:
                            output: List = [[_blue(item) for item in self._data]]
                            output[0][j] = _red(self._data[j])
                            output[0][j + 1] = _red(self._data[j + 1])
                            print("\033c", end="")
                            print(tabulate(output, tablefmt="fancy_grid"))
                            print(_white("Max value :"), _cyan(self._data[j + 1]))
                            if self.control:
                                while True:
                                    try:
                                        response: str = input()
                                    except EOFError as e14:
                                        self.control: bool = False
                                        break
                                    if not response:
                                        break
                            elif self.page_control:
                                self.running: bool = True
                                self.keyboard_listener: Listener = Listener(
                                    on_press=self.on_press
                                )
                                self.keyboard_listener.start()
                                while self.running:
                                    pass
                            else:
                                sleep(self._speed)
                            self._data[j], self._data[j + 1] = (
                                self._data[j + 1],
                                self._data[j],
                            )
                            output: List = [[_blue(item) for item in self._data]]
                            output[0][j] = _red(self._data[j])
                            output[0][j + 1] = _red(self._data[j + 1])
                            print("\033c", end="")
                            print(tabulate(output, tablefmt="fancy_grid"))
                            print(_white("Max value :"), _cyan(self._data[j]))
                            if self.control:
                                while True:
                                    try:
                                        response: str = input()
                                    except EOFError as e15:
                                        self.control: bool = False
                                        break
                                    if not response:
                                        break
                            elif self.page_control:
                                self.running: bool = True
                                self.keyboard_listener: Listener = Listener(
                                    on_press=self.on_press
                                )
                                self.keyboard_listener.start()
                                while self.running:
                                    pass
                            else:
                                sleep(self._speed)
                    else:
                        if self._data[j] > self._data[j + 1]:
                            output: List = [[_blue(item) for item in self._data]]
                            output[0][j] = _red(self._data[j])
                            output[0][j + 1] = _red(self._data[j + 1])
                            print("\033c", end="")
                            print(tabulate(output, tablefmt="fancy_grid"))
                            print(_white("Min value :"), _cyan(self._data[j + 1]))
                            if self.control:
                                while True:
                                    try:
                                        response: str = input()
                                    except EOFError as e16:
                                        self.control: bool = False
                                        break
                                    if not response:
                                        break
                            elif self.page_control:
                                self.running: bool = True
                                self.keyboard_listener: Listener = Listener(
                                    on_press=self.on_press
                                )
                                self.keyboard_listener.start()
                                while self.running:
                                    pass
                            else:
                                sleep(self._speed)
                            self._data[j], self._data[j + 1] = (
                                self._data[j + 1],
                                self._data[j],
                            )
                            output: List = [[_blue(item) for item in self._data]]
                            output[0][j] = _red(self._data[j])
                            output[0][j + 1] = _red(self._data[j + 1])
                            print("\033c", end="")
                            print(tabulate(output, tablefmt="fancy_grid"))
                            print(_white("Min value :"), _cyan(self._data[j]))
                            if self.control:
                                while True:
                                    try:
                                        response: str = input()
                                    except EOFError as e17:
                                        self.control: bool = False
                                        break
                                    if not response:
                                        break
                            elif self.page_control:
                                self.running: bool = True
                                self.keyboard_listener: Listener = Listener(
                                    on_press=self.on_press
                                )
                                self.keyboard_listener.start()
                                while self.running:
                                    pass
                            else:
                                sleep(self._speed)
            output: List = [[_blue(item) for item in self._data]]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            return self._data
        except KeyboardInterrupt as e18:
            print(_cyan("\nI hope you enjoyed learning :)"))

    def insertion_sort(self: "sortVisualizer") -> List | NoReturn | None:
        try:
            try:
                # for shell sort last step
                if self.flag:
                    pass
            except AttributeError as e19:
                output: List = [[_blue(item) for item in self._data]]
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                if len(self._data) > 1:
                    print(_white("Current value :"), _cyan("?"))
                    if self.control:
                        while True:
                            try:
                                response: str = input(
                                    _cyan(
                                        "Press Enter to continue, Ctrl + D to exit control mode, or Ctrl + C to exit the program...\n"
                                    )
                                )
                            except EOFError as e20:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        print(
                            _cyan(
                                "Press Page Down to continue, Page Up to exit page control mode, or Ctrl + C to exit the program..."
                            )
                        )
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
            for i in range(1, len(self._data)):
                current: Any = self._data[i]
                output: List = [[_blue(item) for item in self._data]]
                output[0][i] = _cyan(self._data[i])
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                print(_white("Current value :"), _cyan(current))
                if self.control:
                    while True:
                        try:
                            response: str = input()
                        except EOFError as e21:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
                for j in range(i - 1, -1, -1):
                    output: List = [[_blue(item) for item in self._data]]
                    output[0][j] = _green(self._data[j])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    print(_white("Current value :"), _green(current))
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as e22:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
                    if self.reverse:
                        try:
                            if current > self._data[j]:
                                output[0][j] = _red(self._data[j]) + _white(" ->")
                                print("\033c", end="")
                                print(tabulate(output, tablefmt="fancy_grid"))
                                print(_white("Current value :"), _red(current))
                                if self.control:
                                    while True:
                                        try:
                                            response: str = input()
                                        except EOFError as e23:
                                            self.control: bool = False
                                            break
                                        if not response:
                                            break
                                elif self.page_control:
                                    self.running: bool = True
                                    self.keyboard_listener: Listener = Listener(
                                        on_press=self.on_press
                                    )
                                    self.keyboard_listener.start()
                                    while self.running:
                                        pass
                                else:
                                    sleep(self._speed)
                                self._data[j + 1] = self._data[j]
                                output[0][j + 1] = _red(self._data[j + 1])
                                output[0][j] = _blue(self._data[j])
                                print("\033c", end="")
                                print(tabulate(output, tablefmt="fancy_grid"))
                                print(_white("Current value :"), _cyan(current))
                                if self.control:
                                    while True:
                                        try:
                                            response: str = input()
                                        except EOFError as e24:
                                            self.control: bool = False
                                            break
                                        if not response:
                                            break
                                elif self.page_control:
                                    self.running: bool = True
                                    self.keyboard_listener: Listener = Listener(
                                        on_press=self.on_press
                                    )
                                    self.keyboard_listener.start()
                                    while self.running:
                                        pass
                                else:
                                    sleep(self._speed)
                                if j == 0:
                                    j = -1
                            else:
                                if self._data[j + 1] == self._data[j + 2]:
                                    output: List = [
                                        [_blue(item) for item in self._data]
                                    ]
                                    output[0][j + 1] = _cyan(self._data[j + 1])
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _cyan(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e25:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                    self._data[j + 1] = current
                                    output[0][j + 1] = _cyan(self._data[j + 1])
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _cyan(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e26:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                else:
                                    if self._data[j + 1] != current:
                                        self._data[j + 1] = current
                                break
                        except IndexError as e27:
                            break
                        except TypeError as e28:
                            raise TypeError("Invalid values !") from None
                    else:
                        try:
                            if current < self._data[j]:
                                output[0][j] = _red(self._data[j]) + _white(" ->")
                                print("\033c", end="")
                                print(tabulate(output, tablefmt="fancy_grid"))
                                print(_white("Current value :"), _red(current))
                                if self.control:
                                    while True:
                                        try:
                                            response: str = input()
                                        except EOFError as e29:
                                            self.control: bool = False
                                            break
                                        if not response:
                                            break
                                elif self.page_control:
                                    self.running: bool = True
                                    self.keyboard_listener: Listener = Listener(
                                        on_press=self.on_press
                                    )
                                    self.keyboard_listener.start()
                                    while self.running:
                                        pass
                                else:
                                    sleep(self._speed)
                                self._data[j + 1] = self._data[j]
                                output[0][j + 1] = _red(self._data[j + 1])
                                output[0][j] = _blue(self._data[j])
                                print("\033c", end="")
                                print(tabulate(output, tablefmt="fancy_grid"))
                                print(_white("Current value :"), _cyan(current))
                                if self.control:
                                    while True:
                                        try:
                                            response: str = input()
                                        except EOFError as e30:
                                            self.control: bool = False
                                            break
                                        if not response:
                                            break
                                elif self.page_control:
                                    self.running: bool = True
                                    self.keyboard_listener: Listener = Listener(
                                        on_press=self.on_press
                                    )
                                    self.keyboard_listener.start()
                                    while self.running:
                                        pass
                                else:
                                    sleep(self._speed)
                                if j == 0:
                                    j = -1
                            else:
                                if self._data[j + 1] == self._data[j + 2]:
                                    output: List = [
                                        [_blue(item) for item in self._data]
                                    ]
                                    output[0][j + 1] = _cyan(self._data[j + 1])
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _cyan(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e31:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                    self._data[j + 1] = current
                                    output[0][j + 1] = _cyan(self._data[j + 1])
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _cyan(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e32:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                else:
                                    if self._data[j + 1] != current:
                                        self._data[j + 1] = current
                                break
                        except IndexError as e33:
                            break
                        except TypeError as e34:
                            raise TypeError("Invalid values !") from None
                else:
                    output: List = [[_blue(item) for item in self._data]]
                    output[0][j + 1] = _cyan(self._data[j + 1])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    print(_white("Current value :"), _cyan(current))
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as e35:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
                    self._data[j + 1] = current
                    output: List = [[_blue(item) for item in self._data]]
                    output[0][j + 1] = _cyan(self._data[j + 1])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    print(_white("Current value :"), _cyan(current))
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as e36:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
            output: List = [[_blue(item) for item in self._data]]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            return self._data
        except KeyboardInterrupt as e37:
            print(_cyan("\nI hope you enjoyed learning :)"))

    def shell_sort(self: "sortVisualizer") -> List | NoReturn | None:
        try:
            gap: int = len(self._data) // 2
            output: List = [[_blue(item) for item in self._data]]
            print("\033c", end="")
            print(tabulate(output, tablefmt="fancy_grid"))
            if gap > 0:
                print(_white("Current value :"), _cyan("?"))
                if self.control:
                    while True:
                        try:
                            response: str = input(
                                _cyan(
                                    "Press Enter to continue, Ctrl + D to exit control mode, or Ctrl + C to exit the program...\n"
                                )
                            )
                        except EOFError as e38:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    print(
                        _cyan(
                            "Press Page Down to continue, Page Up to exit page control mode, or Ctrl + C to exit the program..."
                        )
                    )
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
            while gap > 1:
                for i in range(gap, len(self._data)):
                    current: Any = self._data[i]
                    output: List = [[_blue(item) for item in self._data]]
                    output[0][i] = _cyan(self._data[i])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"))
                    print(_white("Current value :"), _cyan(current))
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as e39:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
                    for j in range(i - gap, -1, -gap):
                        output: List = [[_blue(item) for item in self._data]]
                        output[0][j] = _green(self._data[j])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"))
                        print(_white("Current value :"), _green(current))
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as e40:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        elif self.page_control:
                            self.running: bool = True
                            self.keyboard_listener: Listener = Listener(
                                on_press=self.on_press
                            )
                            self.keyboard_listener.start()
                            while self.running:
                                pass
                        else:
                            sleep(self._speed)
                        if self.reverse:
                            try:
                                if current > self._data[j]:
                                    output: List = [
                                        [_blue(item) for item in self._data]
                                    ]
                                    output[0][j] = _red(self._data[j]) + _white(" ->")
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _red(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e41:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                    self._data[j + gap] = self._data[j]
                                    output: List = [
                                        [_blue(item) for item in self._data]
                                    ]
                                    output[0][j + gap] = _red(self._data[j + gap])
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _cyan(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e42:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                    if j - gap < 0:
                                        j -= gap
                                else:
                                    if self._data[j + gap] == self._data[j + (gap * 2)]:
                                        output: List = [
                                            [_blue(item) for item in self._data]
                                        ]
                                        output[0][j + gap] = _cyan(self._data[j + gap])
                                        print("\033c", end="")
                                        print(tabulate(output, tablefmt="fancy_grid"))
                                        print(_white("Current value :"), _cyan(current))
                                        if self.control:
                                            while True:
                                                try:
                                                    response: str = input()
                                                except EOFError as e43:
                                                    self.control: bool = False
                                                    break
                                                if not response:
                                                    break
                                        elif self.page_control:
                                            self.running: bool = True
                                            self.keyboard_listener: Listener = Listener(
                                                on_press=self.on_press
                                            )
                                            self.keyboard_listener.start()
                                            while self.running:
                                                pass
                                        else:
                                            sleep(self._speed)
                                        self._data[j + gap] = current
                                        output[0][j + gap] = _cyan(self._data[j + gap])
                                        print("\033c", end="")
                                        print(tabulate(output, tablefmt="fancy_grid"))
                                        print(_white("Current value :"), _cyan(current))
                                        if self.control:
                                            while True:
                                                try:
                                                    response: str = input()
                                                except EOFError as e44:
                                                    self.control: bool = False
                                                    break
                                                if not response:
                                                    break
                                        elif self.page_control:
                                            self.running: bool = True
                                            self.keyboard_listener: Listener = Listener(
                                                on_press=self.on_press
                                            )
                                            self.keyboard_listener.start()
                                            while self.running:
                                                pass
                                        else:
                                            sleep(self._speed)
                                    else:
                                        if self._data[j + gap] != current:
                                            self._data[j + gap] = current
                                    break
                            except IndexError as e45:
                                break
                            except ValueError as e46:
                                raise TypeError("Invalid values !") from None
                        else:
                            try:
                                if current < self._data[j]:
                                    output: List = [
                                        [_blue(item) for item in self._data]
                                    ]
                                    output[0][j] = _red(self._data[j]) + _white(" ->")
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _red(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e47:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                    self._data[j + gap] = self._data[j]
                                    output: List = [
                                        [_blue(item) for item in self._data]
                                    ]
                                    output[0][j + gap] = _red(self._data[j + gap])
                                    print("\033c", end="")
                                    print(tabulate(output, tablefmt="fancy_grid"))
                                    print(_white("Current value :"), _cyan(current))
                                    if self.control:
                                        while True:
                                            try:
                                                response: str = input()
                                            except EOFError as e48:
                                                self.control: bool = False
                                                break
                                            if not response:
                                                break
                                    elif self.page_control:
                                        self.running: bool = True
                                        self.keyboard_listener: Listener = Listener(
                                            on_press=self.on_press
                                        )
                                        self.keyboard_listener.start()
                                        while self.running:
                                            pass
                                    else:
                                        sleep(self._speed)
                                    if j - gap < 0:
                                        j -= gap
                                else:
                                    if self._data[j + gap] == self._data[j + (gap * 2)]:
                                        output: List = [
                                            [_blue(item) for item in self._data]
                                        ]
                                        output[0][j + gap] = _cyan(self._data[j + gap])
                                        print("\033c", end="")
                                        print(tabulate(output, tablefmt="fancy_grid"))
                                        print(_white("Current value :"), _cyan(current))
                                        if self.control:
                                            while True:
                                                try:
                                                    response: str = input()
                                                except EOFError as e49:
                                                    self.control: bool = False
                                                    break
                                                if not response:
                                                    break
                                        elif self.page_control:
                                            self.running: bool = True
                                            self.keyboard_listener: Listener = Listener(
                                                on_press=self.on_press
                                            )
                                            self.keyboard_listener.start()
                                            while self.running:
                                                pass
                                        else:
                                            sleep(self._speed)
                                        self._data[j + gap] = current
                                        output[0][j + gap] = _cyan(self._data[j + gap])
                                        print("\033c", end="")
                                        print(tabulate(output, tablefmt="fancy_grid"))
                                        print(_white("Current value :"), _cyan(current))
                                        if self.control:
                                            while True:
                                                try:
                                                    response: str = input()
                                                except EOFError as e50:
                                                    self.control: bool = False
                                                    break
                                                if not response:
                                                    break
                                        elif self.page_control:
                                            self.running: bool = True
                                            self.keyboard_listener: Listener = Listener(
                                                on_press=self.on_press
                                            )
                                            self.keyboard_listener.start()
                                            while self.running:
                                                pass
                                        else:
                                            sleep(self._speed)
                                    else:
                                        if self._data[j + gap] != current:
                                            self._data[j + gap] = current
                                    break
                            except IndexError as e51:
                                break
                            except ValueError as e52:
                                raise TypeError("Invalid values !") from None
                    else:
                        output: List = [[_blue(item) for item in self._data]]
                        output[0][j + gap] = _cyan(self._data[j + gap])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"))
                        print(_white("Current value :"), _cyan(current))
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as e53:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        elif self.page_control:
                            self.running: bool = True
                            self.keyboard_listener: Listener = Listener(
                                on_press=self.on_press
                            )
                            self.keyboard_listener.start()
                            while self.running:
                                pass
                        else:
                            sleep(self._speed)
                        self._data[j + gap] = current
                        output: List = [[_blue(item) for item in self._data]]
                        output[0][j + gap] = _cyan(self._data[j + gap])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"))
                        print(_white("Current value :"), _cyan(current))
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as e54:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        elif self.page_control:
                            self.running: bool = True
                            self.keyboard_listener: Listener = Listener(
                                on_press=self.on_press
                            )
                            self.keyboard_listener.start()
                            while self.running:
                                pass
                        else:
                            sleep(self._speed)
                gap //= 2
            self.flag: bool = True
            return self.insertion_sort()
        except KeyboardInterrupt as e55:
            print(_cyan("\nI hope you enjoyed learning :)"))

    def heap_sort(self: "sortVisualizer") -> List | NoReturn | None:
        try:
            output: List = [[_blue(item) for item in self._data]]
            print("\033c", end="")
            if len(self._data) > 1:
                returned_list: List = []
                print(tabulate(output, tablefmt="fancy_grid"), "\n", sep="")
                if self.control:
                    while True:
                        try:
                            response: str = input(
                                _cyan(
                                    "Press Enter to continue, Ctrl + D to exit control mode, or Ctrl + C to exit the program...\n"
                                )
                            )
                        except EOFError as ee:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    print(
                        _cyan(
                            "Press Page Down to continue, Page Up to exit page control mode, or Ctrl + C to exit the program..."
                        )
                    )
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
                output: List = [[_red(item) for item in self._data]]
                print("\033c", end="")
                print(tabulate(output, tablefmt="fancy_grid"))
                print(_white("Heapify"), _cyan("..."), sep="")
                if self.control:
                    while True:
                        try:
                            response: str = input()
                        except EOFError as ee:
                            self.control: bool = False
                            break
                        if not response:
                            break
                elif self.page_control:
                    self.running: bool = True
                    self.keyboard_listener: Listener = Listener(on_press=self.on_press)
                    self.keyboard_listener.start()
                    while self.running:
                        pass
                else:
                    sleep(self._speed)
                if self.reverse:
                    try:
                        x: maxBinaryHeap = minBinaryHeap(self._data)
                    except TypeError as ee:
                        raise TypeError("Invalid values !") from None
                else:
                    try:
                        x: minBinaryHeap = maxBinaryHeap(self._data)
                    except TypeError as ee:
                        raise TypeError("Invalid values !") from None
                for _ in range(len(self._data)):
                    output: List = [[_blue(item) for item in x._data]]
                    rl: List = [[_blue(item) for item in returned_list]]
                    output[0].extend(rl[0])
                    print("\033c", end="")
                    print(tabulate(output, tablefmt="fancy_grid"), "\n", sep="")
                    if self.control:
                        while True:
                            try:
                                response: str = input()
                            except EOFError as ee:
                                self.control: bool = False
                                break
                            if not response:
                                break
                    elif self.page_control:
                        self.running: bool = True
                        self.keyboard_listener: Listener = Listener(
                            on_press=self.on_press
                        )
                        self.keyboard_listener.start()
                        while self.running:
                            pass
                    else:
                        sleep(self._speed)
                    if len(returned_list) > 0:
                        for _ in range(len(returned_list)):
                            output[0].pop()
                    if len(x._data) > 1:
                        output[0][0] = _red(x._data[0])
                        output[0][-1] = _red(x._data[-1])
                        output[0].extend(rl[0])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"), "\n", sep="")
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as ee:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        elif self.page_control:
                            self.running: bool = True
                            self.keyboard_listener: Listener = Listener(
                                on_press=self.on_press
                            )
                            self.keyboard_listener.start()
                            while self.running:
                                pass
                        else:
                            sleep(self._speed)
                        if len(returned_list) > 0:
                            for _ in range(len(returned_list)):
                                output[0].pop()
                        output[0][0] = _red(x._data[-1])
                        output[0][-1] = _red(x._data[0])
                        output[0].extend(rl[0])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"), "\n", sep="")
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as ee:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        elif self.page_control:
                            self.running: bool = True
                            self.keyboard_listener: Listener = Listener(
                                on_press=self.on_press
                            )
                            self.keyboard_listener.start()
                            while self.running:
                                pass
                        else:
                            sleep(self._speed)
                    returned_list.insert(0, x._data[0])
                    if len(x._data) - 1 > 1:
                        output: List = [[_red(item) for item in x._data]]
                        output[0][0], output[0][-1] = output[0][-1], output[0][0]
                        output[0].pop()
                        rl: List = [[_blue(item) for item in returned_list]]
                        output[0].extend(rl[0])
                        print("\033c", end="")
                        print(tabulate(output, tablefmt="fancy_grid"))
                        print(_white("Heapify"), _cyan("..."), sep="")
                        if self.control:
                            while True:
                                try:
                                    response: str = input()
                                except EOFError as ee:
                                    self.control: bool = False
                                    break
                                if not response:
                                    break
                        else:
                            sleep(self._speed)
                    if self.reverse:
                        x.extract_min()
                    else:
                        x.extract_max()
                return returned_list
            else:
                print(tabulate(output, tablefmt="fancy_grid"))
                return self._data
        except KeyboardInterrupt as ee:
            print(_cyan("\nI hope you enjoyed learning :)"))


def _main() -> None:
    color_functions: hashMap = hashMap(
        [
            ["red", _red],
            ["green", _green],
            ["cyan", _cyan],
            ["blue", _blue],
            ["white", _white],
        ]
    )
    characters: List[str] = ["v", "s", "o", "r", "t"]
    colors: List[str] = ["blue", "cyan", "green", "red", "white"]
    lines: List[List[str]] = [figlet_format(char).splitlines() for char in characters]
    max_lines: int = max(len(l) for l in lines)
    lines: List[List[str]] = [l + [""] * (max_lines - len(l)) for l in lines]
    for i in range(max_lines):
        for j, color in enumerate(colors):
            print(color_functions[color](lines[j][i]), end="")
        print()


if __name__ == "__main__":
    _main()
