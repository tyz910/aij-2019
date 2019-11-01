from lib.task import Task, Task09
from lib.solver.base import BaseSolver
from lib.util.speller import Speller
from lib.util.stress import Stress

from typing import List, Dict, Any, Optional


class Task09Solver(BaseSolver):
    VERIFABLE = [
        'анал..гичн',
        'аргум..нтиров',
        'архит..ктурн',
        'б..евик',
        'б..жа',
        'б..зирова',
        'б..режок',
        'б..снописец',
        'благосл..вен',
        'в..рона',
        'возвр..ща',
        'вопл..ти',
        'впеч..тлен',
        'вы..влен',
        'вык..си',
        'выст..вка',
        'выт..чи',
        'г..ниал',
        'г..рделив',
        'г..рева',
        'г..рист',
        'д..ревья',
        'д..ревянн',
        'д..ржа',
        'д..рование',
        'дек..ративн',
        'др..жа',
        'зад..ржа',
        'зак..снел',
        'зал..чи',
        'зам..ря',
        'зам..ча',
        'зан..сённ',
        'зап..вал',
        'запр..си',
        'зас..ва',
        'зас..дание',
        'зат..ва',
        'зат..ну',
        'затв..рдел',
        'землетр..сение',
        'изм..рительн',
        'изм..ря',
        'иск..са',
        'к..робочка',
        'к..сички',
        'к..смонавт',
        'к..сые',
        'кол..бание',
        'л..гичн',
        'л..нейка',
        'л..тательн',
        'м..крица',
        'м..лодой',
        'м..скарад',
        'м..скулатура',
        'м..тинго',
        'м..тингу',
        'многозн..чительн',
        'монт..жёр',
        'мот..вирова',
        'н..зина',
        'наперег..нки',
        'напр..вление',
        'насм..ха',
        'непозв..лительн',
        'неприм..рим',
        'об..рега',
        'обн..жи',
        'обог..щен',
        'обр..млен',
        'ог..рч',
        'од..ва',
        'од..ча',
        'одр..хл',
        'оз..ленен',
        'оз..мь',
        'озл..блен',
        'ол..нина',
        'оп..зда',
        'оп..лчение',
        'орх..дея',
        'осв..титель',
        'осл..плённ',
        'отв..ри',
        'отпл..ти',
        'отр..вление',
        'оч..рован',
        'п..стух',
        'пер..одическ',
        'передв..жение',
        'перекл..ка',
        'перефр..зирова',
        'пл..вление',
        'пл..нительн',
        'пл..чист',
        'поб..ли',
        'погл..щ',
        'под..конник',
        'подб..родок',
        'подт..ну',
        'позн..вательн',
        'пок..ра',
        'пок..ри',
        'пок..сивш',
        'пок..ти',
        'пок..яние',
        'пол..мичн',
        'пол..ска',
        'получ..сов',
        'посв..ти',
        'пот..рял',
        'пот..рять',
        'поч..ни',
        'пр..лестн',
        'предназн..чение',
        'предск..зание',
        'предст..вление',
        'препод..ва',
        'приб..ре',
        'приг..рюни',
        'приз..мли',
        'прик..рми',
        'прим..рение',
        'прим..ря',
        'прим..чат',
        'прис..га',
        'прис..гн',
        'прит..жение',
        'притв..рить',
        'прогн..зирова',
        'прогр..ммирова',
        'прогр..ссивн',
        'продв..га',
        'прож..ва',
        'прон..ка',
        'просв..ща',
        'р..брист',
        'р..скошн',
        'р..торика',
        'р..торическ',
        'разв..ва',
        'разв..твл',
        'развл..к',
        'развл..чение',
        'разг..да',
        'разд..ли',
        'разм..сти',
        'разр..ди',
        'раск..ли',
        'раск..ло',
        'раск..рми',
        'раскр..и',
        'рассвир..певш',
        'раст..ну',
        'рекл..мирова',
        'рец..нзент',
        'с..делка',
        'с..мволика',
        'сб..жавш',
        'сб..рега',
        'сбл..жение',
        'св..сток',
        'ск..птическ',
        'скр..пач',
        'см..рил',
        'сод..ржимое',
        'сож..ле',
        'созд..ва',
        'сост..за',
        'сп..собн',
        'ст..лиз',
        'ст..лист',
        'ст..лов',
        'ст..мулир',
        'ст..рожил',
        'стр..жайш',
        'сувер..нитет',
        'т..жёл',
        'т..инствен',
        'т..ргов',
        'т..рпе',
        'тв..рож',
        'тр..сти',
        'треп..та',
        'ув..дающ',
        'ув..жение',
        'увл..кательн',
        'уг..са',
        'уд..в',
        'ук..ря',
        'укр..ш',
        'укр..щ',
        'ум..ля',
        'упл..тн',
        'упр..вля',
        'упр..сти',
        'упр..щение',
        'ур..ни',
        'усм..ря',
        'ут..пическ',
        'ут..шение',
        'ф..рмат',
        'х..лодильник',
        'х..мическ',
        'хр..брец',
        'цв..ток',
        'ч..рти',
        'ч..ртёж',
        'ч..столюбие',
        'ш..повник',
        'шт..мпова',
        'щ..бета',
        'энциклоп..дич',
    ]

    UNVERIFABLE = [
        '..рнамент',
        'авиак..мпания',
        'алг..ритм',
        'ап..лляция',
        'апп..рат',
        'ар..стократ',
        'б..дон',
        'б..лагур',
        'б..рабан',
        'б..рюз',
        'б..тон',
        'б..чёвка',
        'бюлл..тень',
        'в..негрет',
        'в..нтилятор',
        'в..ртуоз',
        'в..траж',
        'в..трина',
        'в..трушка',
        'велос..пед',
        'вест..бюль',
        'вет..ринар',
        'г..мназия',
        'г..потеза',
        'г..ризонт',
        'г..строном',
        'д..агональ',
        'д..ван',
        'д..лег',
        'д..летант',
        'д..ректива',
        'д..риж',
        'д..скусс',
        'д..сциплина',
        'декл..р',
        'дел..катес',
        'дерм..тин',
        'десп..т',
        'деф..цит',
        'доск..нальн',
        'ижд..вен',
        'импр..виз',
        'инж..нер',
        'исп..щрённ',
        'к..бинет',
        'к..бура',
        'к..валерия',
        'к..вар',
        'к..вычки',
        'к..лач',
        'к..леба',
        'к..мпан',
        'к..мпонент',
        'к..мфорт',
        'к..ндидат',
        'к..питан',
        'к..рзина',
        'к..русель',
        'к..сатка',
        'к..стюм',
        'к..таклизм',
        'кульм..нац',
        'л..зур',
        'л..ле',
        'м..даль',
        'м..карон',
        'м..кет',
        'м..кулатура',
        'м..лин',
        'м..рков',
        'н..стальги',
        'н..тюрморт',
        'нав..ждение',
        'об..няние',
        'об..яние',
        'об..ятельн',
        'од..колон',
        'оз..рни',
        'ок..лдова',
        'опп..нент',
        'ор..гинал',
        'ор..ентир',
        'ор..ол',
        'орх..дея',
        'п..анино',
        'п..анист',
        'п..вильон',
        'п..лисад',
        'п..рила',
        'п..ролон',
        'п..триот',
        'пан..рама',
        'пар..докс',
        'пост..мент',
        'пр..вет',
        'пр..зидент',
        'прец..дент',
        'предв..рительн',
        'преп..рат',
        'при..ритет',
        'прив..лег',
        'прид..рожн',
        'проз..рлив',
        'проп..ганда',
        'прост..ра',
        'р..гулиров',
        'р..зультат',
        'реж..ссёр',
        'с..крет',
        'с..луэт',
        'с..рен',
        'с..рказм',
        'с..яние',
        'сп..раль',
        'ст..ллаж',
        'ст..пендия',
        'сув..ренитет',
        'сув..ренн',
        'т..бурет',
        'т..вар',
        'т..лант',
        'т..ор',
        'т..ран',
        'т..реби',
        'т..рпеда',
        'т..тальн',
        'таб..рет',
        'темп..рамент',
        'тр..дици',
        'трансп..рант',
        'ун..верситет',
        'ур..ган',
        'ф..культет',
        'фил..рмония',
        'фл..мастер',
        'хам..леон',
        'ц..клоп',
        'ц..ремони',
        'ч..шу',
        'ш..блон',
        'ш..девр',
        'ш..роховат',
        'ш..ссе',
        'шимп..нзе',
        'эксп..римент',
        'экспер..мент',
        'эл..ментарн',
        'эп..зод',
        'эп..демия',
        'ярм..р',
    ]

    def __init__(self, speller: Optional[Speller] = None, stress: Optional[Stress] = None):
        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

        if stress is None:
            stress = Stress()
        self.stress: Stress = stress

    def get_task_type(self) -> str:
        return Task.TYPE_09

    def solve(self, task: Task09) -> Any:
        if task.rule == Task09.RULE_CG:
            answer = []
            for i, line in enumerate(task.lines):
                if self.is_alternate_line(line):
                    answer.append(str(i+1))

            return answer

        if task.rule == Task09.RULE_PG:
            answer = []
            for i, line in enumerate(task.lines):
                if self.is_verifable_line(line):
                    answer.append(str(i+1))

            return answer

        if task.rule == Task09.RULE_NG:
            answer = []
            for i, line in enumerate(task.lines):
                if self.is_unverifable_line(line):
                    answer.append(str(i+1))

            return answer

        return []

    def is_unverifable_line(self, line):
        for word in line:
            if self.is_unverifiable(word):
                continue

            if self.is_alternate(word):
                return False

            if self.is_verifiable(word):
                return False

            if self.is_stress(word):
                return False

        return True

    def is_verifable_line(self, line):
        for word in line:
            if self.is_verifiable(word):
                continue

            if self.is_alternate(word):
                return False

            if self.is_unverifiable(word):
                return False

            if self.is_stress(word):
                return False

        return True

    def is_alternate_line(self, line):
        for word in line:
            if not self.is_alternate(word):
                return False

            if self.is_unverifiable(word):
                return False

            if self.is_verifiable(word):
                return False

        return True

    def is_verifiable(self, word: str):
        for start in self.VERIFABLE:
            if word.startswith(start):
                return True

        return False

    def is_unverifiable(self, word):
        for start in self.UNVERIFABLE:
            if word.startswith(start):
                return True

        for char in 'аоеи':
            word_with_char = word.replace('..', char)
            if self.speller.in_dict_words(word_with_char):
                return True

        return False

    def is_stress(self, word, chars='аоеи'):
        for char in chars:
            word_with_char = word.replace('..', char)
            if self.speller.is_known(word_with_char):
                char_pos = word.find('..')
                stress_pos = self.stress.from_vocab(word_with_char)
                if stress_pos is None:
                    stress_pos = self.stress.from_model(word_with_char)

                return stress_pos[0] == char_pos

        return False

    def is_alternate(self, word):
        if word in {
            'р..сток', 'р..стовщик', 'выр..стковый', 'р..стов', 'р..стислав', 'отр..сль', 'ск..чок', 'соч..тание',
            'ск..чу', 'утв..рь', 'з..ревать', 'пл..вец', 'пл..вчиха', 'пл..вцы', 'выг..рки', 'приг..рь', 'отр..слевой',
            'р..весник', 'ур..вень', 'сл..жа', 'прокл..ная'
        }:
            return True

        rules = {
            'р..с': 'о',
            'р..щ': 'а',
            'р..ст': 'а',
            'ск..к': 'а',
        }

        for part, char in rules.items():
            if part in word:
                word_with_char = word.replace('..', char)
                if self.speller.is_known(word_with_char):
                    return not self.is_stress(word, chars=char)

        if 'ск..ч' in word:
            for char in ['о', 'а']:
                word_with_char = word.replace('..', char)
                if self.speller.is_known(word_with_char):
                    return not self.is_stress(word, chars=char)

        rules = {
            'г..р': ('о', ('а',)),
            'з..р': ('а', ('а', 'о')),
            'кл..н': ('о', ('а', 'о')),
            'тв..р': ('о', ('а', 'о')),
            'пл..в': ('а', ('а', 'о')),
        }

        for part, chars in rules.items():
            if part in word:
                word_with_char = word.replace('..', chars[0])
                if self.speller.is_known(word_with_char):
                    return not self.is_stress(word, chars=chars[0])

        rules = {
            'б..р', 'бл..ст', 'д..р', 'ж..г', 'м..р', 'п..р', 'ст..л', 'т..р', 'ч..т',
            'ч..н', 'м..н', 'ж..м', 'н..м', 'кл..н'
        }

        for part in rules:
            if part in word:
                after = word.split(part)[1]
                if len(after) > 0 and after[0] == 'а':
                    char = 'и'
                else:
                    char = 'е'

                word_with_char = word.replace('..', char)
                if self.speller.is_known(word_with_char):
                    return not self.is_stress(word, chars=char)

        rules = {'к..с', 'л..г', 'л..ж'}

        for part in rules:
            if part in word:
                after = word.split(part)[1]
                if len(after) > 0 and after[0] == 'а':
                    char = 'а'
                else:
                    char = 'о'

                word_with_char = word.replace('..', char)
                if self.speller.is_known(word_with_char):
                    return not self.is_stress(word, chars=char)

        if 'м..к' in word or 'м..ч':
            known = False
            for char in ['а', 'о']:
                word_with_char = word.replace('..', char)
                if self.speller.is_known(word_with_char):
                    known = True
                    break

            if known:
                if 'м..кн' in word:
                    return True

                if 'м..кае' in word or 'м..кат' in word:
                    return True

                if 'м..чи' in word:
                    return True

        if 'р..вн' in word:
            return True

        return False
