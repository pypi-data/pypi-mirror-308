class bubblesort:
    """ Класс для работы сортировки пузырьком """
    def __init__(self, data):
        self.data = data

    def sort(self):
        if not self.validate_data():
            raise  TypeError("Ошибка: данные должны быть числовыми.")
        n = len(self.data)
        for i in range(n):
            for j in range(i + 1, n):
                if self.data[j] < self.data[i]:
                    self.data[i], self.data[j] = self.data[j], self.data[i]
        return self.data

    def validate_data(self):
        if not all(isinstance(item, (int, float)) for item in self.data):
            return False
        return True
