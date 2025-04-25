import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 580, 650
WHITE = (209, 238, 238)
BLACK = (171, 178, 191)
FONT_COLOR = (0, 0, 0)
HOVER_COLOR = (128, 138, 135)
PRESS_COLOR = (128, 128, 128)
AUTO_COLOR_ON = (0, 255, 0)
AUTO_COLOR_OFF = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Калькулятор")

font = pygame.font.Font(None, 48)
background_image = pygame.image.load("i.webp")  # Замените на свой путь к изображению

input_string = ""
result_string = ""
pressed_button = None
auto_output_enabled = False


def draw_buttons(mouse_pos):
    buttons = [
        ('7', 50, 150), ('8', 150, 150), ('9', 250, 150), ('÷', 350, 150),
        ('.', 450, 150),
        ('4', 50, 250), ('5', 150, 250), ('6', 250, 250), ('×', 350, 250),
        ('<-', 450, 250),
        ('1', 50, 350), ('2', 150, 350), ('3', 250, 350), ('-', 350, 350),
        ('0', 150, 450), ('+', 250, 450),
        ('²', 50, 450), ('√', 350, 450),
        ('(', 50, 550), (')', 150, 550),
        ('C', 250, 550), ('=', 350, 550),
        ('π', 450, 350),
        ('Auto', 450, 450)
    ]

    for (text, x, y) in buttons:
        button_rect = pygame.Rect(x, y, 80, 80)
        shadow_rect = button_rect.move(5, 5)
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect)

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, WHITE, button_rect)

        if pressed_button == text:
            pygame.draw.rect(screen, PRESS_COLOR, button_rect)

        if text == 'Auto':
            color = AUTO_COLOR_ON if auto_output_enabled else AUTO_COLOR_OFF
            pygame.draw.rect(screen, color, button_rect)

        button_text = font.render(text, True, FONT_COLOR)
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)


def calculate():
    global input_string, result_string
    try:
        expression = input_string.replace('²', '**2').replace('√', 'math.sqrt(').replace('÷', '/').replace('×',
                                                                                                              '*').replace(
            '^', '**').replace('π', 'math.pi')
        if expression.count('(') > expression.count(')'):
            expression += ')' * (expression.count('(') - expression.count(')'))

        result = eval(expression)

        if isinstance(result, float):
            result_string = str(round(result, 5))  # Ограничиваем количество знаков после запятой
        else:
            result_string = str(result)

    except Exception as e:
        result_string = "Ошибка"
        print(e)


def main():
    global input_string, result_string, pressed_button, auto_output_enabled

    while True:
        screen.blit(background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
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

                def handle_button_click(button_text):
                    global input_string, pressed_button
                    pressed_button = button_text
                    operators = ('+', '-', '×', '÷', '^')

                    if button_text == '²' and input_string and input_string[-1] == '²':
                        return
                    if button_text == '√' and input_string and input_string[-1] == '√':
                        return
                    if (button_text in operators and input_string and input_string[-1] in operators) or (
                            button_text in operators and not input_string):
                        if button_text == '-' and (
                                not input_string or input_string[-1] in operators[:-1] or input_string[-1] == '('):
                            # Запрещаем два минуса подряд
                            if input_string and input_string[-1] == '-':
                                return
                            input_string += button_text
                        return
                    if button_text == '.' and input_string and input_string[-1] == '.':
                        return
                    # Разрешаем ввод точки только после операций
                    if button_text == '.' and input_string:
                        last_char_is_operator = False
                        for op in operators:
                            if input_string[-1] == op:
                                last_char_is_operator = True
                                break
                        if input_string[-1] == '(':
                            last_char_is_operator = True
                        if not any(c in input_string for c in operators) and '.' in input_string:
                            return
                    if button_text == 'π':
                        input_string += '3.14159265359'  # Более точное значение pi
                    elif button_text == '<-':
                        input_string = input_string[:-1]
                    elif button_text == 'C':
                        input_string = ""
                        result_string = ""
                    elif button_text == '=':
                        calculate()
                    elif button_text == 'Auto':
                        global auto_output_enabled
                        auto_output_enabled = not auto_output_enabled
                    elif button_text in ('+', '-', '×', '÷') and not input_string:
                        if button_text == '-':
                            input_string += button_text
                        else:
                            pass
                    else:
                        input_string += button_text

                    if auto_output_enabled:
                        calculate()

                if 50 <= mouse_x <= 130 and 150 <= mouse_y <= 230:
                    handle_button_click('7')
                elif 150 <= mouse_x <= 230 and 150 <= mouse_y <= 230:
                    handle_button_click('8')
                elif 250 <= mouse_x <= 330 and 150 <= mouse_y <= 230:
                    handle_button_click('9')
                elif 350 <= mouse_x <= 400 and 150 <= mouse_y <= 230:
                    handle_button_click('÷')
                elif 450 <= mouse_x <= 530 and 150 <= mouse_y <= 230:
                    handle_button_click('.')
                elif 50 <= mouse_x <= 130 and 250 <= mouse_y <= 330:
                    handle_button_click('4')
                elif 150 <= mouse_x <= 230 and 250 <= mouse_y <= 330:
                    handle_button_click('5')
                elif 250 <= mouse_x <= 330 and 250 <= mouse_y <= 330:
                    handle_button_click('6')
                elif 450 <= mouse_x <= 530 and 250 <= mouse_y <= 330:
                    handle_button_click('<-')
                elif 50 <= mouse_x <= 130 and 350 <= mouse_y <= 430:
                    handle_button_click('1')
                elif 150 <= mouse_x <= 230 and 350 <= mouse_y <= 430:
                    handle_button_click('2')
                elif 250 <= mouse_x <= 330 and 350 <= mouse_y <= 430:
                    handle_button_click('3')
                elif 150 <= mouse_x <= 230 and 450 <= mouse_y <= 530:
                    handle_button_click('0')
                elif 50 <= mouse_x <= 130 and 450 <= mouse_y <= 530:
                    handle_button_click('²')
                elif 350 <= mouse_x <= 400 and 450 <= mouse_y <= 530:
                    handle_button_click('√')
                elif 50 <= mouse_x <= 130 and 550 <= mouse_y <= 630:
                    handle_button_click('(')
                elif 150 <= mouse_x <= 230 and 550 <= mouse_y <= 630:
                    handle_button_click(')')
                elif 250 <= mouse_x <= 330 and 550 <= mouse_y <= 630:
                    handle_button_click('C')
                elif 250 <= mouse_x <= 330 and 450 <= mouse_y <= 530:
                    handle_button_click('+')
                elif 350 <= mouse_x <= 400 and 350 <= mouse_y <= 430:
                    handle_button_click('-')
                elif 350 <= mouse_x <= 400 and 250 <= mouse_y <= 330:
                    handle_button_click('×')
                elif 350 <= mouse_x <= 400 and 550 <= mouse_y <= 630:
                    handle_button_click('=')
                elif 450 <= mouse_x <= 530 and 550 <= mouse_y <= 630:
                    handle_button_click('^')
                elif 450 <= mouse_x <= 530 and 350 <= mouse_y <= 430:
                    handle_button_click('π')
                elif 450 <= mouse_x <= 530 and 450 <= mouse_y <= 530:
                    handle_button_click('Auto')

            if event.type == pygame.MOUSEBUTTONUP:
                pressed_button = None

        pygame.display.flip()


if __name__ == "__main__":
    main()
