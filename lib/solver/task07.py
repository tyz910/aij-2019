import re
from nltk.tokenize import word_tokenize
from lib.task import Task, Task07
from lib.solver.base import BaseSolver
from lib.util.speller import Speller

from typing import List, Tuple, Optional


class Task07Solver(BaseSolver):
    SUFFIX_STRIP = ['ов', 'нул']
    NUMR_WORDS = {
        'ст': 'ста',
        'дв': 'двести',
        'тр': 'триста',
        'че': 'четыреста',
        'пя': 'пятьсот',
        'ше': 'шестьсот',
        'се': 'семьсот',
        'во': 'восемьсот',
        'девять': 'девятьсот',
        'по': 'полтораста',
        'девяно': 'девяносто',
    }

    VOCAB_WORDS = {
        'ихний': 'их',
        'ихние': 'их',
        'езжай': 'поезжай',
        'недры': 'недра',
        'тюлью': 'тюлем',
        'махает': 'машет',
        'здоровше': 'здоровее',
        'кренделя': 'крендели',
        'ездиют': 'ездят',
        'поклади': 'положи',
        'ехайте': 'поезжайте',
        'съездиет': 'съездит',
        'повидлой': 'повидлом',
        'попробоваем': 'попробуем',
        'зажгешь': 'зажжешь',
        'испекёт': 'испечёт',
    }

    PLUR_WORDS = {
        "инструктора": "инструкторы",
        "редактора": "редакторы",
        "ректора": "ректоры",
        "конструктора": "конструкторы",
        "прожектора": "прожекторы",
        "сектора": "секторы",
        "инженера": "инженеры",
        "шофёра": "шофёры",
        "бухгалтера": "бухгалтеры",
        "диспетчера": "диспетчеры",
        "договора": "договоры",
        "приговора": "приговоры",
        "плейера": "плейеры",
        "драйвера": "драйверы",
        "принтера": "принтеры",
        "возраста": "возрасты",
        "крема": "кремы",
        "супа": "супы",
        "грунта": "грунты",
        "лифта": "лифты",
        "порта": "порты",
        "склада": "склады",
        "торта": "торты",
        "флота": "флоты",
        "фронта": "фронты",
        "штаба": "штабы",
        "штурмана": "штурманы",

        "директоры": "директора",
        "профессоры": "профессора",
        "инспекторы": "инспектора",
        "докторы": "доктора",
        "катеры": "катера",
        "ордеры": "ордера",
        "теноры": "тенора",
        "фельдшеры": "фельдшера",
        "флюгеры": "флюгера",
        "хуторы": "хутора",
        "шулеры": "шулера",
        "буферы": "буфера",
        "вееры": "веера",
        "буеры": "буера",
        "повары": "повара",
        "шомполы": "шомпола",
        "колоколы": "колокола",
        "куполы": "купола",
        "адресы": "адреса",
        "борты": "борта",
        "желобы": "желоба",
        "жемчуги": "жемчуга",
        "жерновы": "жернова",
        "кузовы": "кузова",
        "окороки": "окорока",
        "округи": "округа",
        "островы": "острова",
        "отпуски": "отпуска",
        "парусы": "паруса",
        "паспорты": "паспорта",
        "погребы": "погреба",
        "потрохи": "потроха",
        "стоги": "стога",
        "сорты": "сорта",
        "сторожи": "сторожа",
        "тетеревы": "тетерева",
        "черепы": "черепа",

        "апельсин": "апельсинов",
        "банан": "бананов",
        "огурец": "огурцов",
        "томат": "томатов",
        "помидор": "помидоров",
        "гранат": "гранатов",
        "абрикос": "абрикосов",
        "ананас": "ананасов",
        "лимон": "лимонов",
        "мандарин": "мандаринов",
        "баклажан": "баклажанов",

        "казах": "казахов",
        "калмык": "калмыков",
        "киргиз": "киргизов",
        "монгол": "монголов",
        "семит": "семитов",
        "таджик": "таджиков",
        "тунгус": "тунгусов",
        "узбек": "узбеков",
        "хорват": "хорватов",
        "якут": "якутов",
        "носок": "носков",
        "гольф": "гольфов",
        "рельс": "рельсов",
        "бронх": "бронхов",
        "джинс": "джинсов",
        "кед": "кедов",

        "дебат": "дебатов",
        "заморозок": "заморозков",
        "кулуар": "кулуаров",
        "мускул": "мускулов",
        "нард": "нардов",
        "очисток": "очистков",
        "сот": "сотов",
        "чипс": "чипсов",
        "нерв": "нервов",

        "болотец": "болотцев",
        "кружевец": "кружевцев",
        "деревец": "деревцев",
        "оконецв": "оконцев",

        "блюдцев": "блюдец",
        "заркальцев": "зеркалец",
        "копытцев": "копытец",
        "одеяльцев": "одеялец",
        "полотенцев": "полотенец",
        "сердцев": "сердец",
        "солнцев": "солнц",

        "ботинков": "ботинок",
        "чулков": "чулок",
        "шароваров": "шаровар",
        "шортов": "шорт",
        "сапогов": "сапог",
        "тапков": "тапок",
        "бахилов": "бахил",
        "бутсов": "бутс",
        "валенков": "валенок",
        "манжетов": "манжет",

        "гуляньев": "гуляний",
        "застольев": "застолий",
        "кушаньев": "кушаний",
        "надгробьев": "надгробий",
        "новосельев": "новоселий",
        "ожерельев": "ожерелий",
        "раздумьев": "раздумий",
        "сидениев": "сидений",
        "снадобиев": "снадобий",
        "соленьев": "солений",
        "ущельев": "ущелий",
    }

    def __init__(self, speller: Optional[Speller] = None):
        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

    def get_task_type(self) -> str:
        return Task.TYPE_07

    def solve(self, task: Task07) -> str:
        lines = task.lines

        lines, answer = self.solve_vocab(lines)
        if answer is not None:
            return answer

        lines, answer = self.solve_ann(lines)
        if answer is not None:
            return answer

        lines, answer = self.solve_suffix_strip(lines)
        if answer is not None:
            return answer

        lines, answer = self.solve_two(lines)
        if answer is not None:
            return answer

        lines, answer = self.solve_numr(lines)
        if answer is not None:
            return answer

        lines, answer = self.solve_more(lines)
        if answer is not None:
            return answer

        lines, answer = self.solve_plur(lines)
        if answer is not None:
            return answer

        return ''

    def solve_more(self, lines: List[str]) -> Tuple[List[str], Optional[str]]:
        filtered_lines = []

        for line in lines:
            match = re.search(r'более\s([а-яё]+)ее([^а-яё]+|$)', line.lower())
            if match is not None:
                return lines, match.group(1) + 'о'

            match = re.search(r'более\s([а-яё]+(ейш|айш)[а-яё]+)', line.lower())
            if match is not None:
                return lines, match.group(1)

            if 'более' not in line:
                filtered_lines.append(line)

        return filtered_lines, None

    def solve_ann(self, lines: List[str]) -> Tuple[List[str], Optional[str]]:
        for line in lines:
            match = re.search(r'(обгрызанн[а-я]+)', line.lower())
            if match is not None:
                return lines, match.group(1).replace('обгрызанн', 'обгрызенн')

        return lines, None

    def solve_vocab(self, lines: List[str]) -> Tuple[List[str], Optional[str]]:
        for line in lines:
            for word, correct in self.VOCAB_WORDS.items():
                for line_word in word_tokenize(line.lower()):
                    if word == line_word:
                        return lines, correct

        return lines, None

    def solve_plur(self, lines: List[str]) -> Tuple[List[str], Optional[str]]:
        for line in lines:
            for word, correct in self.PLUR_WORDS.items():
                for line_word in word_tokenize(line.lower()):
                    if word == line_word:
                        return lines, correct

        return lines, None

    def solve_suffix_strip(self, lines: List[str]) -> Tuple[List[str], Optional[str]]:
        for line in lines:
            for suffix in self.SUFFIX_STRIP:
                match = re.search(r'([а-яё]+)(' + re.escape(suffix) + r')(\s|$)', line.lower())
                if match is not None:
                    word = match.group(0).strip()
                    if not self.speller.is_known(word):
                        word_no_suffix = match.group(1).strip()
                        if self.speller.is_known(word_no_suffix):
                            return lines, word_no_suffix

        return lines, None

    def solve_two(self, lines: List[str]) -> Tuple[List[str], Optional[str]]:
        filtered_lines = []

        for line in lines:
            match = re.search(r'(обоих|обеих|обоим|обеим)\s', line.lower())
            if match is not None:
                word = match.group(0).strip()
                word_morph = self.speller.parse_morph(word)

                next_word = line.lower().split(word)[1]
                next_word_morph = self.speller.parse_morph(next_word)

                if 'masc' in next_word_morph.tag and 'masc' not in word_morph.tag:
                    return filtered_lines, self.speller.parse_morph('оба').inflect({next_word_morph.tag.case}).word

                if 'femn' in next_word_morph.tag and 'femn' not in word_morph.tag:
                    return filtered_lines, self.speller.parse_morph('обе').inflect({next_word_morph.tag.case}).word
            else:
                filtered_lines.append(line)

        return filtered_lines, None

    def solve_numr(self, lines: List[str]) -> Tuple[List[str], Optional[str]]:
        filtered_lines = []

        for line in lines:
            match = re.search(r'[а-я]*(ста|стах|стами|стам|сот|сотым)\s', line.lower())
            if match is not None:
                word = match.group(0).strip()

                normal_form = ''
                for start, numr in self.NUMR_WORDS.items():
                    if word.startswith(start):
                        normal_form = numr
                        break

                if 'NUMR' not in self.speller.parse_morph(word).tag:
                    next_word = line.lower().split(word)[1]
                    next_word_case = self.speller.parse_morph(next_word).tag.case
                    correct_word = self.speller.parse_morph(normal_form).inflect({next_word_case}).word

                    return filtered_lines, correct_word
            else:
                filtered_lines.append(line)

        return filtered_lines, None
