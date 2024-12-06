class fibonacci:
    """ Класс для нахождения чисел Фибоначчи """
    def __init__(self, lenght):
        self.lenght = lenght

    def make(self):
        if not isinstance(self.lenght, int):
            raise TypeError("Ошибка: задаваемая длинна должна быть целым числом.")
        list = [0]
        for i in range(self.lenght - 1):
            if i == 0:
                list.append(list[i] + 1)
            else:
                list.append(list[i] + list[i - 1])
        return list

