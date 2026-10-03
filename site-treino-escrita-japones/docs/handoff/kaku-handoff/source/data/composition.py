"""Composição dos kanji: radical, decomposição gráfica, formação histórica e relações.

Separação deliberada:
  - decomposition  = só o que se VÊ (componentes visuais imediatos)
  - formation      = explicação histórica/etimológica, só quando a classificação é consolidada
Tipos de componente (form):
  - kanji    : caractere independente, com leitura e uso próprios
  - radical  : forma variante de um radical (亻, 氵, 艹…) ou elemento que só existe como radical
  - grafico  : elemento visual sem significado próprio neste uso (inclui “parece X, mas não é X”)
Papéis na formação (role): semantico | fonetico
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))

# Radicais Kangxi usados: caractere padrão -> (número, significado PT, significado EN)
RADICALS = {
 '一': (1, 'um', 'one'), '丨': (2, 'traço vertical', 'line'), '丶': (3, 'ponto', 'dot'), '丿': (4, 'traço diagonal', 'slash'),
 '乙': (5, 'segundo; anzol', 'second'), '亅': (6, 'gancho', 'hook'), '二': (7, 'dois', 'two'), '亠': (8, 'tampa', 'lid'),
 '人': (9, 'pessoa', 'person'), '儿': (10, 'pernas', 'legs'), '入': (11, 'entrar', 'enter'), '八': (12, 'oito; divisão', 'eight; divide'),
 '冂': (13, 'moldura', 'upside-down box'), '冖': (14, 'cobertura', 'cover'), '冫': (15, 'gelo', 'ice'), '几': (16, 'mesa', 'table'),
 '凵': (17, 'recipiente aberto', 'open box'), '刀': (18, 'faca', 'knife'), '力': (19, 'força', 'power'), '匕': (21, 'colher', 'spoon'),
 '匚': (22, 'caixa', 'box'), '十': (24, 'dez', 'ten'), '卜': (25, 'adivinhação', 'divination'), '厶': (28, 'privado', 'private'),
 '又': (29, 'mão; de novo', 'right hand; again'), '口': (30, 'boca', 'mouth'), '囗': (31, 'cercado', 'enclosure'), '土': (32, 'terra', 'earth'),
 '士': (33, 'guerreiro; erudito', 'scholar'), '夊': (35, 'andar devagar', 'go slowly'), '夕': (36, 'entardecer', 'evening'), '大': (37, 'grande', 'big'),
 '女': (38, 'mulher', 'woman'), '子': (39, 'criança', 'child'), '宀': (40, 'telhado', 'roof'), '寸': (41, 'polegada; mão', 'inch'),
 '小': (42, 'pequeno', 'small'), '尸': (44, 'corpo', 'corpse'), '山': (46, 'montanha', 'mountain'), '巛': (47, 'rio', 'river'),
 '工': (48, 'trabalho; ferramenta', 'work'), '己': (49, 'si mesmo', 'oneself'), '巾': (50, 'pano', 'cloth'), '干': (51, 'seco; escudo', 'dry'),
 '广': (53, 'telhado inclinado', 'shelter'), '廴': (54, 'passo largo', 'long stride'), '弋': (56, 'estaca', 'shoot'), '弓': (57, 'arco', 'bow'),
 '彐': (58, 'focinho', 'snout'), '彳': (60, 'passo', 'step'), '心': (61, 'coração', 'heart'), '戈': (62, 'alabarda', 'halberd'),
 '戸': (63, 'porta', 'door'), '手': (64, 'mão', 'hand'), '支': (65, 'ramo', 'branch'), '攴': (66, 'bater; ação', 'rap'),
 '文': (67, 'escrita', 'script'), '斗': (68, 'medida', 'dipper'), '斤': (69, 'machado', 'axe'), '方': (70, 'direção', 'square'),
 '日': (72, 'sol; dia', 'sun'), '曰': (73, 'dizer', 'say'), '月': (74, 'lua; mês', 'moon'), '木': (75, 'árvore', 'tree'),
 '欠': (76, 'bocejo; faltar', 'lack'), '止': (77, 'parar; pé', 'stop'), '歹': (78, 'morte; ossos', 'death'), '殳': (79, 'lança', 'weapon'),
 '毋': (80, 'não; mãe', 'do not'), '气': (84, 'vapor', 'steam'), '水': (85, 'água', 'water'), '火': (86, 'fogo', 'fire'),
 '爪': (87, 'garra', 'claw'), '父': (88, 'pai', 'father'), '牛': (93, 'vaca', 'cow'), '犬': (94, 'cão', 'dog'), '玉': (96, 'joia', 'jade'),
 '生': (100, 'vida', 'life'), '用': (101, 'usar', 'use'), '田': (102, 'arrozal', 'field'), '疒': (104, 'doença', 'sickness'),
 '癶': (105, 'passos', 'footsteps'), '白': (106, 'branco', 'white'), '皿': (108, 'prato', 'dish'), '目': (109, 'olho', 'eye'),
 '矢': (111, 'flecha', 'arrow'), '石': (112, 'pedra', 'stone'), '示': (113, 'altar; divindade', 'altar'), '禾': (115, 'cereal', 'grain'),
 '穴': (116, 'buraco', 'cave'), '立': (117, 'ficar de pé', 'stand'), '竹': (118, 'bambu', 'bamboo'), '米': (119, 'arroz', 'rice'),
 '糸': (120, 'fio', 'thread'), '网': (122, 'rede', 'net'), '羊': (123, 'ovelha', 'sheep'), '羽': (124, 'pena; asa', 'feather'),
 '老': (125, 'velho', 'old'), '耳': (128, 'orelha', 'ear'), '聿': (129, 'pincel', 'brush'), '肉': (130, 'carne', 'meat'),
 '自': (132, 'si mesmo', 'self'), '至': (133, 'chegar', 'arrive'), '舌': (135, 'língua', 'tongue'), '艮': (138, 'parar', 'stopping'),
 '色': (139, 'cor', 'color'), '艸': (140, 'planta; grama', 'grass'), '虫': (142, 'inseto', 'insect'), '行': (144, 'ir; cruzamento', 'go'),
 '衣': (145, 'roupa', 'clothes'), '襾': (146, 'cobrir', 'cover'), '見': (147, 'ver', 'see'), '言': (149, 'palavra; dizer', 'speech'),
 '豆': (151, 'feijão', 'bean'), '豕': (152, 'porco', 'pig'), '貝': (154, 'concha; dinheiro', 'shell'), '赤': (155, 'vermelho', 'red'),
 '走': (156, 'correr', 'run'), '足': (157, 'pé', 'foot'), '車': (159, 'veículo', 'cart'), '辵': (162, 'caminhar', 'walk'),
 '邑': (163, 'vila', 'city'), '酉': (164, 'jarra de bebida', 'wine jar'), '里': (166, 'vila; légua', 'village'), '金': (167, 'metal; ouro', 'metal'),
 '長': (168, 'longo', 'long'), '門': (169, 'portão', 'gate'), '阜': (170, 'colina', 'mound'), '隹': (172, 'pássaro', 'short-tailed bird'),
 '雨': (173, 'chuva', 'rain'), '青': (174, 'azul', 'blue'), '音': (180, 'som', 'sound'), '頁': (181, 'cabeça', 'head'),
 '風': (182, 'vento', 'wind'), '食': (184, 'comer', 'eat'), '首': (185, 'cabeça; pescoço', 'head'), '馬': (187, 'cavalo', 'horse'),
 '高': (189, 'alto', 'tall'), '魚': (195, 'peixe', 'fish'), '鳥': (196, 'pássaro', 'bird'), '鹿': (198, 'cervo', 'deer'), '黒': (203, 'preto', 'black'),
}
for _l in open(os.path.join(HERE, 'radicais_kangxi.txt'), encoding='utf-8'):
    if _l.startswith('#') or not _l.strip(): continue
    _n, _c, _pt, _en = _l.rstrip('\n').split('|')
    RADICALS[_c] = (int(_n), _pt, _en)
MISSING_RAD = set()
# formas variantes -> (radical padrão, nome japonês da forma)
VARIANTS = {
 '亻': ('人', 'ninben'), '𠆢': ('人', 'hitoyane'), '刂': ('刀', 'rittou'), '氵': ('水', 'sanzui'), '扌': ('手', 'tehen'),
 '忄': ('心', 'risshinben'), '灬': ('火', 'rekka'), '艹': ('艸', 'kusakanmuri'), '辶': ('辵', 'shinnyou'), '礻': ('示', 'shimesuhen'),
 '糹': ('糸', 'itohen'), '釒': ('金', 'kanehen'), '飠': ('食', 'shokuhen'), '⺮': ('竹', 'takekanmuri'), '耂': ('老', 'oikanmuri'),
 '牜': ('牛', 'ushihen'), '攵': ('攴', 'bokunyou'), '王': ('玉', 'tamahen'), '覀': ('襾', 'nishi'), '罒': ('网', 'amigashira'),
 '爫': ('爪', 'tsumekanmuri'), '川': ('巛', 'kawa'), '⺀': ('冫', 'nisui'),
 '犭': ('犬', 'kemonohen'), '⺍': ('小', 'tsu'), '𧾷': ('足', 'ashihen'), '衤': ('衣', 'koromohen'), '⺌': ('小', 'shou'), '⺹': ('老', 'oikanmuri'),
 '氺': ('水', 'shitamizu'), '忄': ('心', 'risshinben'), '㣺': ('心', 'shitagokoro'), '⺤': ('爪', 'tsumekanmuri'),
}
# kanji usado como forma de outro radical, marcado com "~" na decomposição
RAD_FORMS = {'王': ('joia (forma de 玉)', '玉'), '月': ('carne (forma de 肉, “nikuzuki”)', '肉')}
RAD_OVERRIDE = {'郵': '邑'}   # 阝 à direita = 邑; à esquerda = 阜

# componentes que não são kanji da base: char -> (form, significado PT)
COMP = {
 # formas de radical
 '亻': ('radical', 'pessoa (forma de 人)'), '𠆢': ('radical', 'pessoa (forma de 人 no alto)'), '刂': ('radical', 'faca (forma de 刀)'),
 '氵': ('radical', 'água (forma de 水)'), '扌': ('radical', 'mão (forma de 手)'), '忄': ('radical', 'coração (forma de 心)'),
 '灬': ('radical', 'fogo (forma de 火)'), '艹': ('radical', 'planta, grama'), '辶': ('radical', 'caminhar, movimento'),
 '礻': ('radical', 'altar, divindade (forma de 示)'), '糹': ('radical', 'fio (forma de 糸)'), '釒': ('radical', 'metal (forma de 金)'),
 '飠': ('radical', 'comida (forma de 食)'), '⺮': ('radical', 'bambu (forma de 竹)'), '耂': ('radical', 'velho (forma de 老)'),
 '牜': ('radical', 'vaca (forma de 牛)'), '攵': ('radical', 'bater, ação'), '覀': ('radical', 'cobrir'), '罒': ('radical', 'rede'),
 '爫': ('radical', 'garra, mão (forma de 爪)'), '⺀': ('radical', 'gelo (forma de 冫)'), '阝': ('radical', 'colina (à esquerda) / vila (à direita)'),
 '宀': ('radical', 'telhado'), '冖': ('radical', 'cobertura'), '广': ('radical', 'edifício (telhado inclinado)'), '疒': ('radical', 'doença'),
 '彳': ('radical', 'passo, andar'), '隹': ('radical', 'pássaro'), '頁': ('radical', 'cabeça'), '冫': ('radical', 'gelo'), '癶': ('radical', 'passos'),
 '廴': ('radical', 'passo largo'), '歹': ('radical', 'ossos, morte'), '气': ('radical', 'vapor, ar'), '匚': ('radical', 'caixa'),
 '囗': ('radical', 'cercado'), '凵': ('radical', 'recipiente'), '冂': ('radical', 'moldura'), '亠': ('radical', 'tampa'),
 '厶': ('radical', 'privado; elemento “ム”'), '儿': ('radical', 'pernas'), '夂': ('radical', 'pé que segue'), '夊': ('radical', 'andar devagar'),
 '彐': ('radical', 'focinho; mão'), '⺕': ('radical', 'mão (forma de 彐)'), '丶': ('radical', 'ponto'), '丿': ('radical', 'traço diagonal'),
 '丨': ('radical', 'traço vertical'), '乙': ('radical', 'anzol'), '亅': ('radical', 'gancho'), '几': ('radical', 'mesa'), '匕': ('radical', 'colher; pessoa virada'),
 '卜': ('radical', 'adivinhação'), '毋': ('radical', 'não; mãe'), '禾': ('radical', 'cereal'), '穴': ('radical', 'buraco, caverna'),
 '酉': ('radical', 'jarra de bebida'), '豕': ('radical', 'porco'), '艮': ('radical', 'parar'), '聿': ('radical', 'pincel'), '弋': ('radical', 'estaca'),
 '殳': ('radical', 'lança; bater'), '戈': ('radical', 'alabarda'), '巾': ('radical', 'pano'), '尸': ('radical', 'corpo'), '襾': ('radical', 'cobrir'),
 '曰': ('radical', 'dizer'), '⺷': ('grafico', 'ovelha (forma de 羊)'), '⺧': ('grafico', 'forma de 牛/pé (elemento superior)'),
 # elementos gráficos
 '丷': ('grafico', 'dois pontos'), '⺍': ('grafico', 'três pontos'), '丬': ('grafico', 'elemento lateral'), '𠂇': ('grafico', 'mão (forma antiga)'),
 '⺈': ('grafico', 'elemento superior'), '龹': ('grafico', 'elemento “龹”'), '䒑': ('grafico', 'elemento superior'), '𠂉': ('grafico', 'elemento “𠂉”'),
 '丂': ('grafico', 'elemento fonético (コウ)'), '㐅': ('grafico', 'cruz'), '龶': ('grafico', 'forma de 生 no alto'), '𦰩': ('grafico', 'elemento “𦰩”'),
 '㑒': ('grafico', 'forma de 僉 (juntos)'), '开': ('grafico', 'elemento “开”'), '𠬝': ('grafico', 'elemento “𠬝”'), '㐬': ('grafico', 'elemento “㐬”'),
 '𡗗': ('grafico', 'elemento superior de 春'), '㐄': ('grafico', 'elemento “㐄”'), '罙': ('grafico', 'elemento fonético (シン)'), '夬': ('grafico', 'elemento fonético (ケツ)'),
 '戋': ('grafico', 'elemento fonético (セン)'), '宁': ('grafico', 'elemento fonético (チョ)'), '隺': ('grafico', 'elemento fonético (カク)'),
 '韱': ('grafico', 'elemento fonético (セン)'), '夆': ('grafico', 'elemento fonético (ホウ)'), '咼': ('grafico', 'elemento fonético (カ)'),
 '冘': ('grafico', 'elemento fonético (チン)'), '昜': ('grafico', 'elemento fonético (ヨウ)'), '甬': ('grafico', 'elemento fonético (ヨウ)'),
 '乍': ('grafico', 'elemento fonético (サ)'), '亲': ('grafico', 'elemento fonético (シン)'), '关': ('grafico', 'elemento “关”'), '丽': ('grafico', 'par; elemento “丽”'),
 '廿': ('grafico', 'vinte (elemento)'), '𠯑': ('grafico', 'elemento fonético (カツ)'), '𠂔': ('grafico', 'elemento fonético (シ)'), '囧': ('grafico', 'janela (forma antiga)'),
 '囟': ('grafico', 'moleira, cabeça (forma antiga)'), '昷': ('grafico', 'elemento fonético (オン)'), '枼': ('grafico', 'elemento fonético (ヨウ)'),
 '洛': ('kanji', 'Luoyang (nome próprio)'), '翟': ('grafico', 'faisão (elemento fonético)'),
 # kanji independentes que (ainda) não estão na base
 '寸': ('kanji', 'polegada; medida'), '斤': ('kanji', 'machado; medida de peso'), '丁': ('kanji', 'quarteirão; prego'), '可': ('kanji', 'possível'),
 '未': ('kanji', 'ainda não'), '央': ('kanji', 'centro'), '里': ('kanji', 'vila; légua'), '至': ('kanji', 'chegar; extremo'), '完': ('kanji', 'completo'),
 '周': ('kanji', 'volta, circunferência'), '占': ('kanji', 'ocupar; adivinhar'), '勿': ('kanji', 'não (proibição)'), '反': ('kanji', 'contra; oposto'),
 '舌': ('kanji', 'língua'), '豆': ('kanji', 'feijão'), '彦': ('kanji', 'rapaz (nomes próprios)'), '云': ('kanji', 'dizer; nuvem'), '永': ('kanji', 'eterno'),
 '巷': ('kanji', 'rua, beco'), '夭': ('kanji', 'jovem; flexível'), '各': ('kanji', 'cada'), '原': ('kanji', 'origem; campo'), '黄': ('kanji', 'amarelo'),
 '喬': ('kanji', 'alto'), '幾': ('kanji', 'quantos; alguns'), '旨': ('kanji', 'intenção; sabor'), '系': ('kanji', 'sistema; linhagem'), '列': ('kanji', 'fila'),
 '胡': ('kanji', 'estrangeiro (antigo)'), '舜': ('kanji', 'Shun (nome próprio)'), '既': ('kanji', 'já'), '務': ('kanji', 'tarefa, dever'), '将': ('kanji', 'general; futuro'),
 '丘': ('kanji', 'colina'), '垂': ('kanji', 'pender'), '奉': ('kanji', 'oferecer'), '唐': ('kanji', 'dinastia Tang'), '帛': ('kanji', 'seda'), '失': ('kanji', 'perder'),
 '灰': ('kanji', 'cinza'), '然': ('kanji', 'assim; natureza'), '尭': ('kanji', 'alto (nomes próprios)'), '召': ('kanji', 'convocar'), '迷': ('kanji', 'perder-se'),
 '直': ('kanji', 'direto; consertar'), '支': ('kanji', 'ramo; apoio'), '干': ('kanji', 'seco'), '旦': ('kanji', 'aurora'), '尺': ('kanji', 'medida (shaku)'),
 '哥': ('kanji', 'irmão mais velho (chinês)'), '欠': ('kanji', 'faltar; bocejar'), '氏': ('kanji', 'sobrenome; clã'), '与': ('kanji', 'dar'), '官': ('kanji', 'governo; oficial'),
 '丙': ('kanji', 'terceiro (da série)'), '軍': ('kanji', 'exército'), '己': ('kanji', 'si mesmo'), '矢': ('kanji', 'flecha'), '昔': ('kanji', 'antigamente'),
 '式': ('kanji', 'cerimônia; fórmula'), '是': ('kanji', 'correto; isto'), '免': ('kanji', 'dispensar'), '斗': ('kanji', 'medida de volume'), '尚': ('kanji', 'ainda; estimar'),
 '也': ('kanji', 'também (partícula clássica)'), '又': ('kanji', 'de novo; mão'), '士': ('kanji', 'guerreiro; erudito'), '良': ('kanji', 'bom'), '亜': ('kanji', 'sub-; Ásia'),
 '羽': ('kanji', 'pena; asa'), '合': ('kanji', 'juntar; combinar'), '玉': ('kanji', 'joia; bola'), '咸': ('kanji', 'todos'), '予': ('kanji', 'antecipadamente'),
 '采': ('kanji', 'colher; escolher'), '吏': ('kanji', 'funcionário'), '坐': ('kanji', 'sentar'), '袁': ('kanji', 'manto longo (nome)'), '吾': ('kanji', 'eu (arcaico)'),
 '戸': ('kanji', 'porta'), '弓': ('kanji', 'arco'), '示': ('kanji', 'mostrar'), '申': ('kanji', 'dizer (humilde); relâmpago (forma antiga)'), '才': ('kanji', 'talento; idade'),
 '帚': ('kanji', 'vassoura'), '幺': ('kanji', 'pequeno; fio fino'), '首': ('kanji', 'pescoço; cabeça'), '肖': ('kanji', 'semelhança'), '動': ('kanji', 'mover'),
 '毎': ('kanji', 'cada'), '市': ('kanji', 'cidade; mercado'), '凡': ('kanji', 'comum; em geral'), '僉': ('kanji', 'todos, juntos'), '幵': ('grafico', 'elemento fonético (ケン)'),
 '及': ('kanji', 'alcançar'), '亦': ('kanji', 'também'), '丹': ('kanji', 'vermelho; pigmento'), '專': ('kanji', 'exclusivo (forma antiga)'),
 '三': ('kanji', 'três'),
 '犭': ('radical', 'animal (forma de 犬)'), '𧾷': ('radical', 'pé (forma de 足)'), '衤': ('radical', 'roupa (forma de 衣)'), '⺌': ('radical', 'pequeno (forma de 小)'),
 '𤰇': ('grafico', 'aljava (elemento)'), '兑': ('grafico', 'elemento fonético (エツ)'), '戠': ('grafico', 'elemento fonético (ショク)'), '帀': ('grafico', 'elemento “帀”'),
 '㠯': ('grafico', 'elemento “㠯”'), '堇': ('grafico', 'elemento fonético (キン)'), '壴': ('grafico', 'tambor (elemento)'), '𠂤': ('grafico', 'monte (elemento)'),
 '乇': ('grafico', 'elemento fonético (タク)'), '甫': ('grafico', 'elemento fonético (ホ)'), '昏': ('grafico', 'crepúsculo (elemento fonético コン)'), '巽': ('grafico', 'elemento fonético (セン)'),
 '韋': ('radical', 'couro curtido'), '壬': ('grafico', 'elemento fonético (ジン)'), '尹': ('grafico', 'elemento fonético (イン)'), '朮': ('grafico', 'elemento fonético (ジュツ)'),
 '冓': ('grafico', 'elemento fonético (コウ)'), '乎': ('grafico', 'elemento fonético (コ)'), '圣': ('grafico', 'elemento “圣”'), '𠬝': ('grafico', 'elemento “𠬝”'),
 '咅': ('grafico', 'elemento fonético (ホウ)'), '龹': ('grafico', 'elemento “龹”'), '亦': ('kanji', 'também'), '卩': ('radical', 'selo; pessoa ajoelhada'), '厂': ('radical', 'penhasco'),
 '彡': ('radical', 'enfeite; pelos'), '疋': ('radical', 'pé; rolo de tecido'), '舛': ('radical', 'pés opostos'), '髟': ('radical', 'cabelo comprido'), '㐬': ('grafico', 'elemento “㐬”'),
 '鹿': ('kanji', 'cervo'),
}
for _l in open(os.path.join(HERE, 'componentes_dicionario.txt'), encoding='utf-8'):
    if _l.startswith('#') or not _l.strip(): continue
    _c, _f, _m = _l.rstrip('\n').split('|')
    COMP.setdefault(_c, (_f, _m))
EXTRA_DECOMP = {'吾': '五 口', '哥': '可 可', '可': '丁 口', '胡': '古 月', '相': None, '昔': '', '官': '宀', '唐': '', '原': '', '直': '十 目',
                '周': '口', '咸': '口', '召': '口', '各': '口', '占': '卜 口', '完': '宀 元', '軍': '冖 車', '是': '日', '迷': '辶 米', '幾': '', '将': '',
                '然': '灬', '尭': '', '失': '', '奉': '', '旨': '日', '央': '大', '昜': '日', '洛': '氵 各', '舌': '口', '豆': '口', '良': '', '合': '口',
                '玉': '王', '亜': '', '帚': '冖 巾', '吏': '口', '坐': '土', '袁': '口', '予': '', '免': '', '列': '刂', '式': '工', '肖': '月', '灰': '火',
                '采': '木', '宁': '宀', '彦': '立', '市': '亠 巾', '毎': '𠂉 毋', '厶': ''}

FTYPE = {'P': ('pictograma', 'Pictograma (象形)', 'Desenho simplificado de algo concreto.'),
         'I': ('indicativo', 'Indicativo (指事)', 'Sinal abstrato que indica uma ideia (posição, quantidade…).'),
         'C': ('ideograma-composto', 'Ideograma composto (会意)', 'Combina o significado de dois ou mais elementos.'),
         'F': ('fono-semantico', 'Fono-semântico (形声)', 'Um elemento indica o significado e outro indica o som.'),
         'K': ('kokuji', 'Kokuji (国字)', 'Kanji criado no Japão, combinando significados.')}

def load_components():
    rows = {}
    for line in open(os.path.join(HERE, 'componentes.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'): continue
        f = line.split('|')
        assert len(f) == 4, line
        k, rad, dec, form = f
        assert k not in rows, 'componente duplicado: ' + k
        rows[k] = (rad, [] if dec.strip() == '-' else dec.split(), form.strip())
    import glob
    for fn in sorted(glob.glob(os.path.join(HERE, 'kanji_extra_*.txt'))):
        for line in open(fn, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'): continue
            f = line.split('|')
            if len(f) == 14: f = f[:9] + ['', '', ''] + f[11:]
            k, rad, dec, form = f[0], f[12], f[13], f[14]
            assert k not in rows, 'componente duplicado: ' + k
            rows[k] = (rad, [] if dec.strip() in ('-', '') else dec.split(), form.strip())
    return rows

def enrich(kanji):
    rows = load_components()
    base = {e['char']: e for e in kanji}
    missing_rows = [c for c in base if c not in rows]
    assert not missing_rows, 'sem composição: ' + ''.join(missing_rows)
    unknown = set()

    def comp_info(c):
        if c.endswith('~'):
            ch = c[:-1]; mean, std = RAD_FORMS[ch]
            return {'c': ch, 'form': 'radical', 'meaning': mean, 'standard': std, 'ref': ('kanji:' + std) if std in base else None}
        look = c.endswith('!')
        ch = c[:-1] if look else c
        if look:
            return {'c': ch, 'form': 'grafico', 'lookalike': True, 'meaning': 'forma parecida com %s, mas com outra origem' % ch, 'ref': None}
        if ch in base:
            e = base[ch]
            return {'c': ch, 'form': 'kanji', 'meaning': ' / '.join(e['meaning']['pt']), 'ref': e['id']}
        if ch in COMP:
            form, mean = COMP[ch]
            std = VARIANTS.get(ch, (None,))[0]
            ref = ('kanji:' + std) if std in base else None
            return {'c': ch, 'form': form, 'meaning': mean, 'ref': ref, **({'standard': std} if std else {})}
        unknown.add(ch)
        return {'c': ch, 'form': 'grafico', 'meaning': '', 'ref': None}

    def radical(k, rad):
        std = RAD_OVERRIDE.get(k) or ('阜' if rad == '阝' else VARIANTS.get(rad, (rad,))[0])
        if std not in RADICALS:
            MISSING_RAD.add('%s(%s)' % (rad, k)); num, pt, en = 0, '', ''
        else:
            num, pt, en = RADICALS[std]
        return {'char': rad, 'standard': std, 'number': num, 'meaning': {'pt': pt, 'en': en},
                'name': VARIANTS[rad][1] if rad in VARIANTS else ({'阜': 'kozatohen', '邑': 'oozato'}.get(std) if rad == '阝' else None),
                'ref': ('kanji:' + std) if std in base else None}

    def formation(s):
        if not s: return None
        t, parts, note = (s.split(';') + ['', ''])[:3]
        key, label, desc = FTYPE[t]
        ps = []
        for p in [x for x in parts.split(',') if x]:
            c, _, role = p.partition('=')
            info = comp_info(c)
            item = {'c': c, 'role': 'semantico' if role == 's' else 'fonetico', 'meaning': info['meaning'], 'ref': info['ref'], 'form': info['form']}
            if role.startswith('f:'): item['reading'] = role[2:]
            ps.append(item)
        return {'type': key, 'label': label, 'description': desc, 'parts': ps, 'note': note or None}

    # recursive "contains" index (visual), for component search and inverse relations
    memo = {}
    def contains(c, seen=()):
        if c in memo: return memo[c]
        if c in seen: return set()
        out = set()
        parts = rows[c][1] if c in rows else (EXTRA_DECOMP.get(c) or '').split()
        for p in parts:
            if p.endswith('!'): continue
            if p.endswith('~'):
                out.add(p[:-1]); out.add(RAD_FORMS[p[:-1]][1]); continue
            out.add(p)
            if p in VARIANTS: out.add(VARIANTS[p][0])
            out |= contains(p, seen + (c,))
        memo[c] = out
        return out

    for e in kanji:
        rad, dec, form = rows[e['char']]
        e['radical'] = radical(e['char'], rad)
        e['decomposition'] = [comp_info(c) for c in dec]
        e['formation'] = formation(form)
        e['containsComponents'] = sorted(contains(e['char']))
    for e in kanji:
        for p in (e['formation'] or {}).get('parts', []):
            pass
    # inverse + related
    for e in kanji:
        ch = e['char']
        variants = {v for v, (s, _) in VARIANTS.items() if s == ch}
        used = [o['char'] for o in kanji if o is not e and (ch in o['containsComponents'] or variants & set(o['containsComponents']))]
        e['usedIn'] = used
    def norm_set(e):
        out = set()
        for d in e['decomposition']:
            if d.get('lookalike'): continue
            out.add(d.get('standard') or d['c'])
        return out
    for e in kanji:
        mine = norm_set(e)
        scored = []
        for o in kanji:
            if o is e: continue
            theirs = norm_set(o)
            s = 2 * len(mine & theirs) + (1 if o['radical']['standard'] == e['radical']['standard'] else 0)
            if e['char'] in theirs: s += 2
            if o['char'] in mine: s += 2
            if s >= 2: scored.append((-s, o['strokes'], o['char']))
        e['related'] = [c for _, _, c in sorted(scored)[:10]]
    if MISSING_RAD: print('RADICAIS DESCONHECIDOS:', ' '.join(sorted(MISSING_RAD)))
    return sorted(unknown)
