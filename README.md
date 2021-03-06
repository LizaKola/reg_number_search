# reg_number_search

## Задание

У большинства правовых актов или судебных решений есть определенный регистрационный номер, по которому их просто находить. При этом номер может состоять из цифр, букв, знаков препинания, примеры:
- 00-04-05/1809
- 33-10000/10
- 003/У-МС
- А63-3110/2013
- ПНАЭ Г-5-40-97
- 23-НП
- (17135)А07-СК-1/6/2007-Г-БАА

Часто пользователи могут случайно ошибиться при вводе такого сложного номера – забыть поставить тире или пропустить нолик. В рамках данного задания требуется реализовать алгоритм, который бы, получая на вход некорректный номер, возвращал один или несколько наиболее похожих на него реальных номеров.

#### Кому может помочь решение этой задачи и каким образом?
Данное решение может использоваться в любом месте, где выполняется пользовательский ввод.

#### В каком контексте будут использованы полученные результаты?
Пользователи часто ошибаются при вводе сложных номеров, поэтому полученные результаты могут быть использованы, где выполняется пользовательский ввод и требуется точное установление номера. 

#### Какие требования встают перед решением?
Прежде всего это скорость работы. Медленный алгоритм будет с большой точностью - это врядли понравится пользователям. Во вторую очередь точностью распознавания.

#### Насколько предлагаемый мною вариант соответствует выдвинутым мною требованиям?
Предложенный алгоритм соответствует выдвинутым требованиям по скорости и точности распознавания.

#### Какие пути и перспективы развития могут быть у этого алгоритма, можно ли его улучшить?
- Обработка опечаток. Однако данная направление развития требует изучения. Количество регистрационных номеров большое, поэтому если учитывать опечатки, то возможно список значений для выбора пользователем будет слишком велико.

## Реализация

Идея реализации данного задания состоит в следующем. 

### Хранение данных
Представляем набор регистрационных номеров в виде хэш-таблицы, в которой ключом является нормализованная форма регистрационного номера, а значением набор регистрационных номеров (группа), у которых совпадает нормализованная форма. Под нормализацией понимается преобразование строки, в рамках которого выполяется перевод в нижний регистр; удаление лишних пробелов (не более одного между символами или наборами символов); удаление символов, отличных от букв и цифр.

Хэш-таблица подразумевает выполнение операция поиска за O(1), поэтому скорость получение группы регистрационных номеров будет быстрой. В Python тип данных dict реализован в виде хэш-таблицы, поэтому в качестве он используется в роли хэш-таблицы (ключ - нормализованная форма; значение - группа регистрационных номеров).

### Сравнение данных

Расстояние Левенштейна (редакционное расстояние, дистанция редактирования) — метрика, измеряющая разность между двумя последовательностями символов. Она определяется как минимальное количество односимвольных операций (а именно вставки, удаления, замены), необходимых для превращения одной последовательности символов в другую.

Методика вычисления цен вставок, делеций и замен использовалась классическая.


### Алгоритм
Подготовка:
- считывание регистрационных номеров из файлов в оперативную память
- формирование словаря

Выполнение поиска:
- Пользователь вводит регистрационный номер
- Выполняется нормализация введенного номера
- Выполнется поиск нормализованного номера в хэш-таблицы
- Если номер не найден, тогда выводится сообщение "Неизвестный номер"
- Если номер найден, тогда выполнется проверка количества номеров, которые соответствуют полученной нормализованной форме.
     - Если количество регистрационных номеров равно 1, тогда выводится сообщение "Есть такой номер!"
     - Если количество регистрационных номеров более чем 1, тогда набор регистрационных номеров сортируется по значению расстояния Левенштейна в порядке возрастания. Выполняется проверка на равенство первого элемента (с наименьшим расстоянием Левенштейна)
 из отсортированного набора и введенного значения. Если они равны, тогда выводится сообщение "Есть такой номер!". В противном случае выводится сообщение "Возможно вы имели ввиду один из:" и выполняется перечисление регистрационных номеров, отсортированных по расстоянию Левенштейна.

 ### Запуск
 
 ```console
 python main.py 
 ```
 
 ### Пример работы
 
 Входные данные - регистрационный номер
 
 Выходные данные - сообщение о наличии такого регистрационного номера или рекомендационный список регистрационных номеров
 
 ```
> Введите номер: 0817/пзн
Возможно вы имели ввиду один из:
08-17/ПЗН
08-17/ПЗ-Н
08-17/ПЗ-Н
```

```
> Введите номер: 140311/07539
Возможно вы имели ввиду один из:
14-03-11/07-539
14-03-11/07-539
```

```
> Введите номер: ЯК373/12611
Возможно вы имели ввиду один из:
ЯК-37-3/12611
ЯК-37-3/12611@
ЯК-37-3/12611@
```
P.S. Не было обработки удаления повторных значений про считывании исходных данных.
