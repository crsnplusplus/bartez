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

    def get_observers(self):
        return self.__observers


class BartezSolverObserver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, entries):
        pass


class BartezSolverObserverPrintCrossword(BartezSolverObserver):
    __metaclass__ = ABCMeta

    def __init__(self, crossword):
        BartezSolverObserver.__init__(self)
        self.__crossword = crossword

    def update(self, entries):
        self.__crossword.clear_all_non_blocks()
        self.__crossword.set_entries(entries.values())
        self.__crossword.print_crossword()
