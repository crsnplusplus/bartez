from abc import ABCMeta, abstractmethod


class BartezObservable():

    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def unregister_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self, entries):
        for o in self.__observers:
            o.update(entries)

    def notify_observers_message(self, m):
        for o in self.__observers:
            o.message(m)

    def get_observers(self):
        return self.__observers


class BartezSolverObserver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, entries):
        pass

    @abstractmethod
    def message(self, message):
        pass

class BartezSolverObserverPrintCrossword(BartezSolverObserver):
    __metaclass__ = ABCMeta

    def __init__(self, crossword, times = 1):
        BartezSolverObserver.__init__(self)
        self.__crossword = crossword
        self.__count = 0
        self.__times = times

    def update(self, entries):
        self.__count = self.__count + 1

        if ((self.__count % self.__times) == 0) is False:
            return

        self.__crossword.clear_all_non_blocks()
        self.__crossword.set_entries(entries.values())
        self.__crossword.print_crossword()

    def message(self, message):
        print(message)