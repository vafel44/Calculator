import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 500, 650
WHITE = (209,238,238)
BLACK = (171, 178, 191)
FONT_COLOR = (0, 0, 0)
HOVER_COLOR = (128, 138, 135)  # цвет кнопки при наведении
PRESS_COLOR = (128, 128, 128)  # цвет кнопки при нажатии

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Калькулятор")
font = pygame.font.Font(None, 48)

# Загрузка изображения фона
background_image = pygame.image.load("i.webp")  # Замените "background.jpg" на имя вашего файла

input_string = ""
result_string = ""
pressed_button = None  # Переменная для хранения нажатой кнопки

def draw_buttons(mouse_pos):
    buttons = [
        ('7', 50, 150), ('8', 150, 150), ('9', 250, 150), ('÷', 350, 150),  # Знак деления
        ('4', 50, 250), ('5', 150, 250), ('6', 250, 250), ('×', 350, 250),  # Изменено на '×'
        ('1', 50, 350), ('2', 150, 350), ('3', 250, 350), ('-', 350, 350),
        ('0', 150, 450), ('+', 250, 450),  # Кнопка сложения
        ('²', 50, 450), ('√', 350, 450),  # Кнопка возведения в квадрат и корня
        ('(', 50, 550), (')', 150, 550),  # Кнопки для скобок
        ('C', 250, 550), ('=', 350, 550)  # Кнопка "Стереть" и "="
    ]
    for (text, x, y) in buttons:
        button_rect = pygame.Rect(x, y, 80, 80)

        # Рисуем тень
        shadow_rect = button_rect.move(5, 5)  # Сдвигаем тень
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect)  # Цвет тени

        # Проверка, находится ли мышь над кнопкой
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, button_rect)  # Цвет при наведении
        else:
            pygame.draw.rect(screen, WHITE, button_rect)  # Обычный цвет

        # Изменяем цвет кнопки, если она нажата
        if pressed_button == text:
            pygame.draw.rect(screen, PRESS_COLOR, button_rect)  # Цвет при нажатии

        # Рисуем текст
        button_text = font.render(text, True, FONT_COLOR)
        screen.blit(button_text, (x + 30, y + 20))

def calculate():
    global input_string, result_string
    try:
        # Заменяем '²' на '**2', '√' на 'math.sqrt', '÷' на '/' и '×' на '*' для использования в eval
        expression = input_string.replace('²', '**2').replace('√', 'math.sqrt(').replace('÷', '/').replace('×', '*')
        
        # Закрываем все открытые скобки
        if expression.count('(') > expression.count(')'):
            expression += ')' * (expression.count('(') - expression.count(')'))

        # Используем eval для вычисления выражения
        result_string = str(eval(expression))  # Вычисляем результат
    except Exception as e:
        result_string = "Ошибка"  # Отображаем сообщение об ошибке

def main():
    global input_string, result_string, pressed_button
    while True:
        screen.blit(background_image, (0, 0))  # Отображаем изображение фона
        mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
        draw_buttons(mouse_pos)

        input_display = font.render(input_string, True, FONT_COLOR)
        screen.blit(input_display, (50, 50))

        result_display = font.render(result_string, True, FONT_COLOR)
        screen.blit(result_display, (50, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 50 <= mouse_x <= 130 and 150 <= mouse_y <= 230:
                    input_string += '7'
                    pressed_button = '7'
                elif 150 <= mouse_x <= 230 and 150 <= mouse_y <= 230:
                    input_string += '8'
                    pressed_button = '8'
                elif 250 <= mouse_x <= 330 and 150 <= mouse_y <= 230:
                    input_string += '9'
                    pressed_button = '9'
                elif 350 <= mouse_x <= 400 and 150 <= mouse_y <= 230:
                    # Проверяем, можно ли добавить деление
                    if input_string and input_string[-1] not in '+-*/(':  # Если последний символ не оператор
                        input_string += '÷'  # Изменено на '÷'
                    pressed_button = '÷'
                elif 50 <= mouse_x <= 130 and 250 <= mouse_y <= 330:
                    input_string += '4'
                    pressed_button = '4'
                elif 150 <= mouse_x <= 230 and 250 <= mouse_y <= 330:
                    input_string += '5'
                    pressed_button = '5'
                elif 250 <= mouse_x <= 330 and 250 <= mouse_y <= 330:
                    input_string += '6'  # Добавляем 6
                    pressed_button = '6'
                elif 50 <= mouse_x <= 130 and 350 <= mouse_y <= 430:
                    input_string += '1'
                    pressed_button = '1'
                elif 150 <= mouse_x <= 230 and 350 <= mouse_y <= 430:
                    input_string += '2'
                    pressed_button = '2'
                elif 250 <= mouse_x <= 330 and 350 <= mouse_y <= 430:
                    input_string += '3'  # Добавляем 3
                    pressed_button = '3'
                elif 150 <= mouse_x <= 230 and 450 <= mouse_y <= 530:
                    input_string += '0'
                    pressed_button = '0'
                elif 50 <= mouse_x <= 130 and 450 <= mouse_y <= 530:  # Кнопка ²
                    if '²' not in input_string:  # Проверяем, есть ли уже '²' в строке
                        input_string += '²'  # Добавляем только '²'
                    pressed_button = '²'
                elif 350 <= mouse_x <= 400 and 450 <= mouse_y <= 530:  # Кнопка √
                    if '√' not in input_string:  # Проверяем, есть ли уже '√' в строке
                        input_string += '√'  # Добавляем только '√' без скобок
                    pressed_button = '√'
                elif 50 <= mouse_x <= 130 and 550 <= mouse_y <= 630:  # Кнопка "("
                    input_string += '('
                    pressed_button = '('
                elif 150 <= mouse_x <= 230 and 550 <= mouse_y <= 630:  # Кнопка ")"
                    input_string += ')'
                    pressed_button = ')'
                elif 250 <= mouse_x <= 330 and 550 <= mouse_y <= 630:  # Кнопка "Стереть"
                    input_string = ""
                    pressed_button = 'C'
                elif 250 <= mouse_x <= 330 and 450 <= mouse_y <= 530:  # Кнопка "+"
                    if input_string and input_string[-1] not in '+-*/()':  # Проверка на последнюю операцию
                        input_string += '+'
                    pressed_button = '+'
                elif 350 <= mouse_x <= 400 and 350 <= mouse_y <= 430:  # Кнопка "-"
                    # Проверяем, можно ли добавить минус
                    if not input_string or input_string[-1] in '+*/(':  # Если строка пустая или последний символ оператор
                        input_string += '-'  # Добавляем минус
                    elif input_string and input_string[-1].isdigit():  # Если перед минусом стоит число
                        input_string += '-'  # Добавляем минус после числа
                    # Проверяем, чтобы не добавлять минус, если он уже есть в конце
                    elif input_string and input_string[-1] == '-':
                        pass  # Не добавляем минус, если он уже есть
                    pressed_button = '-'
                elif 350 <= mouse_x <= 400 and 250 <= mouse_y <= 330:  # Кнопка "×"
                    if input_string and input_string[-1] not in '+-÷()':  # Проверка на последнюю операцию
                        input_string += '×'  # Изменено на '×'
                    pressed_button = '×'
                elif 350 <= mouse_x <= 400 and 550 <= mouse_y <= 630:  # Кнопка "="
                    calculate()  # Вычисляем результат при нажатии на "="
                    pressed_button = '='

            if event.type == pygame.MOUSEBUTTONUP:
                pressed_button = None  # Сбрасываем нажатую кнопку

        pygame.display.flip()

if __name__ == "__main__":
    main()