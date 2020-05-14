# Простейший парсер арифметических выражений

## Грамматика
алфавит:

$\Sigma = \{\text{Строчние и заглавные латинские буквы}, \text{цифры от 0 до 9}, +, -, *, /, =, (, )\}$

Правила вывода (нетерминалы выделены жирным):

**S** → **Variable** = **Expr**<br>
**Expr** → **Product** **Sum'**<br>
**Sum'** → $\varepsilon$ | + **Product** **Sum'** | - **Product** **Sum'**<br>
**Product** → **Term** **Product'**<br>
**Product'** → $\varepsilon$ | * **Term** **Product'** | / **Term** **Product'**<br>
**Term** → -**Unsigned** | **Unsigned**<br>
**Unsigned** → **Number** | (**Expr**) | **Variable**<br>
**Number** → **N** | **ND**<br>
**N** → 1|2|3|4|5|6|7|8|9<br>
**D** → 0|1|2|3|4|5|6|7|8|9<br>
**D** → **DD**<br>
**Variable** → **L**|**LA**<br>
**L** → a|b|...|z|A|B|...|Z<br>
**A** → **L**|**D**<br>
**A** → **AA**

## Решение
`my_parser.py` - парсер

`test_parser.py` - тесты pytest

Файлы `correct_tests.txt`

## Запуск парсера 
```
python my_parser.py [<input_file_path> [<output_file_path>]]
```
Здесь `<input_file_path>` - входной файл, содержащий выражения для вычислений вида:
```
a = 2
b = 3
c = 2 * 5
d = c - a
```
Если `<input_file_path>` не задан, то выражения должны вводится с коммандной строки после запуска программы.

`<output_file_path>` -  файл, в который будут записываться результаты. Если не задан - результаты будут выводится в консоль.

Пример:
```
python my_parser.py correct_tests.txt
```

## Запуск тестов

```
pytest -v test_parser.py
```
