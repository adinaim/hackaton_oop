from mixins import JSonMixin, ParsingMixin, CreateMixin, ListingMixin, RetrieveMixin, UpdateMixin, DeleteMixin

class CRUD(JSonMixin, ParsingMixin, CreateMixin, ListingMixin, RetrieveMixin, UpdateMixin, DeleteMixin):
    _file_name = 'cars.json'


    def interface(self):
        commands = {
            'create': self.create,
            'list': self.list,
            'retrieve': self.get_car_by_id,
            'update': self.update,
            'delete': self.delete,
        }

        while True:
            try:
                command = input("""
                Введите команду: 
                create - создание объявления,
                list - получение списка авто,
                retrieve - получение авто по id,
                update - обновление объявления,
                delete - удаление объявления,
                quit - выход
                """).lower().strip()
                if command in commands:
                    commands[command]()
                elif command == 'quit':
                    print('Выход из программы')
                    break
                else:
                    print('Нет такой команды')
                    continue
            # except KeyobardInterrupt если голое исключение ловить ниже
            except ValueError:
                print('Введите данные заново')
                continue


crud = CRUD()
# crud.create()
# crud.list()
# crud.get_user_by_id()
# crud.update()
# crud.delete()
crud.interface()

# validate date