import os
from typing import List
import fpdf
import webbrowser
from datetime import datetime
import logging


LOGGER = logging.getLogger('__main__')


def show_as_pdf(figures: List[str]):
    """
    Формирует `pdf` документ на основе списка изображений и открывает его в
    браузере

    :param figures: Список идентификаторов изображений
    :type figures: List[int]
    """
    pdf = fpdf.FPDF('P', 'mm', (210, 100))
    images = list(map(lambda f: os.path.join('figures', f'{f}.png'), figures))
    flag_file_empty = True
    for image in images:
        if os.path.exists(image):
            pdf.add_page()
            pdf.image(image, x=0, y=0, w=210, h=100)
            flag_file_empty = False
        else:
            LOGGER.warning(f'Не найден файл: "{image}"!')

    if flag_file_empty:
        LOGGER.warning(f'Сформирован пустой файл! Ничего не будет сохранено!')
    else:
        if not os.path.exists('results'):
            LOGGER.warning(f'Не найдена директория: "./results/"!')
            os.mkdir('results')
            LOGGER.info(f'Создана директория: "./results/"!')
        path = os.path.join(
            'results',
            f'result_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pdf')
        pdf.output(path, 'F')
        LOGGER.warning(f'Сформирован .pdf файл и сохранён: "{path}".')
        webbrowser.open('file://' + os.path.join(os.getcwd(), path), new=2)