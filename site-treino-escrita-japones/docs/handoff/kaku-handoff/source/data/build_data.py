#!/usr/bin/env python3
"""Gera a base de caracteres do Kaku (hiragana, katakana, kanji) em JSON + bundle JS.

Fonte editável:
  - kanji.txt            (uma linha por kanji)
  - tabelas KANA_* abaixo
Saídas (pasta ./out):
  - kaku-caracteres.json (tudo), hiragana.json, katakana.json, kanji.json
  - kaku-data.js         (window.KAKU_DATA, para o site)
"""
import json, re, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ romaji
BASE = dict(zip(
    'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゔぁぃぅぇぉゃゅょゎゕゖ',
    'a i u e o ka ki ku ke ko sa shi su se so ta chi tsu te to na ni nu ne no ha hi fu he ho ma mi mu me mo ya yu yo ra ri ru re ro wa wo n ga gi gu ge go za ji zu ze zo da ji zu de do ba bi bu be bo pa pi pu pe po vu a i u e o ya yu yo wa ka ke'.split()))
SPECIAL2 = {
    'ちぇ': 'che', 'しぇ': 'she', 'じぇ': 'je', 'ふぁ': 'fa', 'ふぃ': 'fi', 'ふぇ': 'fe', 'ふぉ': 'fo',
    'てぃ': 'ti', 'でぃ': 'di', 'とぅ': 'tu', 'どぅ': 'du', 'うぃ': 'wi', 'うぇ': 'we', 'うぉ': 'wo',
    'ゔぁ': 'va', 'ゔぃ': 'vi', 'ゔぇ': 've', 'ゔぉ': 'vo', 'くぁ': 'kwa', 'くぃ': 'kwi', 'くぇ': 'kwe', 'くぉ': 'kwo',
}

def to_hira(s):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)

def to_kata(s):
    return ''.join(chr(ord(c) + 0x60) if 'ぁ' <= c <= 'ゖ' else c for c in s)

def romaji(s):
    s = to_hira(s)
    units, i = [], 0
    while i < len(s):
        two = s[i:i + 2]
        if two in SPECIAL2:
            units.append(SPECIAL2[two]); i += 2; continue
        if len(two) == 2 and two[1] in 'ゃゅょ' and two[0] in BASE and BASE[two[0]].endswith('i') and two[0] not in 'いぃ':
            b = BASE[two[0]][:-1]; y = BASE[two[1]]
            units.append(b + (y[1:] if b in ('sh', 'ch', 'j') else y)); i += 2; continue
        c = s[i]
        if c in 'っッ':
            units.append('#'); i += 1; continue
        if c == 'ー':
            units.append('-'); i += 1; continue
        if c in BASE:
            units.append(BASE[c]); i += 1; continue
        units.append(c); i += 1
    out = ''
    for k, u in enumerate(units):
        nxt = units[k + 1] if k + 1 < len(units) else ''
        if u == '#':
            if nxt and nxt[0] not in '#-' and nxt[0].isalpha():
                out += 't' if nxt.startswith('ch') else nxt[0]
            continue
        if u == '-':
            v = [ch for ch in out if ch in 'aeiou']
            out += v[-1] if v else ''
            continue
        if u == 'n' and nxt and (nxt[0] in 'aiueoy'):
            out += "n'"; continue
        out += u
    return out

# ------------------------------------------------------------------ kana tables
H_BASIC = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
H_STROKES = dict(zip(H_BASIC, [3,2,2,2,3, 3,4,1,3,2, 3,1,2,3,1, 4,2,1,1,2, 4,3,2,2,1, 3,1,4,1,4, 3,2,3,2,3, 3,2,2, 2,2,1,2,1, 2,3, 1]))
K_BASIC = to_kata(H_BASIC)
K_STROKES = dict(zip(K_BASIC, [2,2,3,3,3, 2,3,2,3,2, 3,3,2,2,2, 3,3,3,3,2, 2,2,2,4,1, 2,2,1,1,4, 2,3,2,2,3, 2,2,3, 2,2,2,1,3, 2,3, 2]))
DAKU = {'が':'か','ぎ':'き','ぐ':'く','げ':'け','ご':'こ','ざ':'さ','じ':'し','ず':'す','ぜ':'せ','ぞ':'そ','だ':'た','ぢ':'ち','づ':'つ','で':'て','ど':'と','ば':'は','び':'ひ','ぶ':'ふ','べ':'へ','ぼ':'ほ','ゔ':'う'}
HANDA = {'ぱ':'は','ぴ':'ひ','ぷ':'ふ','ぺ':'へ','ぽ':'ほ'}
SMALL = {'ぁ':'あ','ぃ':'い','ぅ':'う','ぇ':'え','ぉ':'お','ゃ':'や','ゅ':'ゆ','ょ':'よ','っ':'つ','ゎ':'わ','ゕ':'か','ゖ':'け'}

def strokes_of(ch, kata):
    h = to_hira(ch)
    tab = K_STROKES if kata else H_STROKES
    def one(c):
        c = to_hira(c)
        if c in DAKU: return one_base(DAKU[c]) + 2
        if c in HANDA: return one_base(HANDA[c]) + 1
        if c in SMALL: return one_base(SMALL[c])
        return one_base(c)
    def one_base(c):
        return tab[to_kata(c) if kata else c]
    return sum(one(c) for c in h)

H_DAKU_LIST = 'がぎぐげござじずぜぞだぢづでどばびぶべぼ'
H_HANDA_LIST = 'ぱぴぷぺぽ'
H_SMALL_LIST = 'ぁぃぅぇぉゃゅょっゎ'
YOUON_ROWS = 'きぎしじちにひびぴみり'
H_YOUON = [r + y for r in YOUON_ROWS for y in 'ゃゅょ']
K_SMALL_LIST = 'ァィゥェォャュョッヮヵヶ'
K_EXTENDED = ['ファ','フィ','フェ','フォ','ティ','ディ','トゥ','ドゥ','チェ','シェ','ジェ','ウィ','ウェ','ウォ','ヴァ','ヴィ','ヴェ','ヴォ','クァ','クィ','クェ','クォ']

# exemplos: caractere -> (palavra, pt, en). Leitura = a própria palavra (kana).
KANA_EX = {
 'あ':('あめ','chuva','rain'),'い':('いぬ','cão','dog'),'う':('うみ','mar','sea'),'え':('えき','estação','station'),'お':('おちゃ','chá','tea'),
 'か':('かさ','guarda-chuva','umbrella'),'き':('きって','selo','stamp'),'く':('くるま','carro','car'),'け':('けむり','fumaça','smoke'),'こ':('こども','criança','child'),
 'さ':('さかな','peixe','fish'),'し':('しお','sal','salt'),'す':('すし','sushi','sushi'),'せ':('せかい','mundo','world'),'そ':('そら','céu','sky'),
 'た':('たまご','ovo','egg'),'ち':('ちず','mapa','map'),'つ':('つき','lua','moon'),'て':('て','mão','hand'),'と':('とり','pássaro','bird'),
 'な':('なつ','verão','summer'),'に':('にく','carne','meat'),'ぬ':('ぬの','tecido','cloth'),'ね':('ねこ','gato','cat'),'の':('のり','alga nori','nori seaweed'),
 'は':('はな','flor','flower'),'ひ':('ひと','pessoa','person'),'ふ':('ふね','barco','boat'),'へ':('へや','quarto','room'),'ほ':('ほし','estrela','star'),
 'ま':('まど','janela','window'),'み':('みず','água','water'),'む':('むし','inseto','insect'),'め':('め','olho','eye'),'も':('もり','floresta','forest'),
 'や':('やま','montanha','mountain'),'ゆ':('ゆき','neve','snow'),'よ':('よる','noite','night'),
 'ら':('らいねん','próximo ano','next year'),'り':('りんご','maçã','apple'),'る':('るす','ausência de casa','being away from home'),'れ':('れきし','história','history'),'ろ':('ろうか','corredor','hallway'),
 'わ':('わたし','eu','I'),'を':('ほんをよむ','ler um livro','to read a book'),'ん':('ほん','livro','book'),
 'が':('がっこう','escola','school'),'ぎ':('ぎんこう','banco','bank'),'ぐ':('ぐあい','condição (de saúde)','condition'),'げ':('げんき','bem-disposto','healthy; energetic'),'ご':('ごはん','arroz; refeição','rice; meal'),
 'ざ':('ざっし','revista','magazine'),'じ':('じかん','tempo','time'),'ず':('ずっと','o tempo todo','all the time'),'ぜ':('ぜんぶ','tudo','all'),'ぞ':('ぞう','elefante','elephant'),
 'だ':('だいがく','universidade','university'),'ぢ':('はなぢ','sangramento nasal','nosebleed'),'づ':('つづく','continuar','to continue'),'で':('でんわ','telefone','telephone'),'ど':('どうぶつ','animal','animal'),
 'ば':('ばしょ','lugar','place'),'び':('びょういん','hospital','hospital'),'ぶ':('ぶた','porco','pig'),'べ':('べんきょう','estudo','study'),'ぼ':('ぼうし','chapéu','hat'),
 'ぱ':('かんぱい','saúde! (brinde)','cheers!'),'ぴ':('えんぴつ','lápis','pencil'),'ぷ':('てんぷら','tempurá','tempura'),'ぺ':('ぺこぺこ','morrendo de fome','starving'),'ぽ':('さんぽ','passeio','walk; stroll'),
 'ぁ':('わぁ','uau!','wow!'),'ぇ':('ねぇ','ei!; né?','hey!'),'ゃ':('おちゃ','chá','tea'),'ゅ':('しゅくだい','lição de casa','homework'),'ょ':('きょう','hoje','today'),'っ':('きって','selo','stamp'),
 'きゃ':('きゃく','cliente; visita','customer; guest'),'きゅ':('きゅう','nove','nine'),'きょ':('きょう','hoje','today'),
 'ぎゃ':('ぎゃく','inverso','reverse'),'ぎゅ':('ぎゅうにゅう','leite','milk'),'ぎょ':('きんぎょ','peixinho dourado','goldfish'),
 'しゃ':('しゃしん','foto','photo'),'しゅ':('しゅくだい','lição de casa','homework'),'しょ':('しょくじ','refeição','meal'),
 'じゃ':('じゃま','estorvo','hindrance'),'じゅ':('じゅぎょう','aula','class'),'じょ':('じょうず','habilidoso','skillful'),
 'ちゃ':('おちゃ','chá','tea'),'ちゅ':('ちゅうい','atenção; cuidado','caution'),'ちょ':('ちょっと','um pouco','a little'),
 'にゃ':('にゃあ','miau','meow'),'にゅ':('にゅういん','internação','hospitalization'),'にょ':('にょろにょろ','serpenteando','wriggling'),
 'ひゃ':('ひゃく','cem','hundred'),'ひゅ':('ひゅうひゅう','assobio (do vento)','whistling (wind)'),'ひょ':('ひょうじょう','expressão facial','facial expression'),
 'びゃ':('さんびゃく','trezentos','three hundred'),'びゅ':('びゅうびゅう','uivo (do vento)','howling (wind)'),'びょ':('びょういん','hospital','hospital'),
 'ぴゃ':('はっぴゃく','oitocentos','eight hundred'),'ぴょ':('はっぴょう','apresentação','presentation'),
 'みゃ':('みゃく','pulso','pulse'),'みょ':('みょうじ','sobrenome','surname'),
 'りゃ':('りゃくご','abreviação','abbreviation'),'りゅ':('りゅうがく','estudo no exterior','study abroad'),'りょ':('りょこう','viagem','trip'),
 # katakana
 'ア':('アイス','sorvete','ice cream'),'イ':('イルカ','golfinho','dolphin'),'ウ':('ウイルス','vírus','virus'),'エ':('エレベーター','elevador','elevator'),'オ':('オレンジ','laranja','orange'),
 'カ':('カメラ','câmera','camera'),'キ':('キロ','quilo','kilo'),'ク':('クラス','turma','class'),'ケ':('ケーキ','bolo','cake'),'コ':('コーヒー','café','coffee'),
 'サ':('サラダ','salada','salad'),'シ':('シーツ','lençol','bed sheet'),'ス':('スープ','sopa','soup'),'セ':('セーター','suéter','sweater'),'ソ':('ソース','molho','sauce'),
 'タ':('タクシー','táxi','taxi'),'チ':('チーズ','queijo','cheese'),'ツ':('ツアー','excursão','tour'),'テ':('テレビ','televisão','TV'),'ト':('トマト','tomate','tomato'),
 'ナ':('ナイフ','faca','knife'),'ニ':('ニュース','notícias','news'),'ヌ':('ヌードル','macarrão','noodles'),'ネ':('ネクタイ','gravata','necktie'),'ノ':('ノート','caderno','notebook'),
 'ハ':('ハンバーガー','hambúrguer','hamburger'),'ヒ':('ヒーター','aquecedor','heater'),'フ':('フランス','França','France'),'ヘ':('ヘリコプター','helicóptero','helicopter'),'ホ':('ホテル','hotel','hotel'),
 'マ':('マスク','máscara','mask'),'ミ':('ミルク','leite','milk'),'ム':('ゲーム','jogo','game'),'メ':('メール','e-mail','e-mail'),'モ':('モデル','modelo','model'),
 'ヤ':('タイヤ','pneu','tire'),'ユ':('ユーモア','humor','humor'),'ヨ':('ヨーグルト','iogurte','yogurt'),
 'ラ':('ラジオ','rádio','radio'),'リ':('リボン','fita','ribbon'),'ル':('ルール','regra','rule'),'レ':('レストラン','restaurante','restaurant'),'ロ':('ロボット','robô','robot'),
 'ワ':('ワイン','vinho','wine'),'ン':('パン','pão','bread'),
 'ガ':('ガラス','vidro','glass'),'ギ':('ギター','violão','guitar'),'グ':('グラス','copo','glass (cup)'),'ゲ':('ゲーム','jogo','game'),'ゴ':('ゴルフ','golfe','golf'),
 'ザ':('ピザ','pizza','pizza'),'ジ':('ジーンズ','jeans','jeans'),'ズ':('ズボン','calça','trousers'),'ゼ':('ゼロ','zero','zero'),'ゾ':('ゾーン','zona','zone'),
 'ダ':('ダンス','dança','dance'),'デ':('デパート','loja de departamentos','department store'),'ド':('ドア','porta','door'),
 'バ':('バス','ônibus','bus'),'ビ':('ビル','prédio','building'),'ブ':('ブラシ','escova','brush'),'ベ':('ベッド','cama','bed'),'ボ':('ボール','bola','ball'),
 'パ':('パン','pão','bread'),'ピ':('ピアノ','piano','piano'),'プ':('プール','piscina','pool'),'ペ':('ペン','caneta','pen'),'ポ':('ポスト','caixa de correio','mailbox'),
 'ヴ':('ヴァイオリン','violino','violin'),
 'ァ':('ファン','fã','fan'),'ィ':('パーティー','festa','party'),'ェ':('カフェ','café (lugar)','café'),'ォ':('フォーク','garfo','fork'),'ゥ':('タトゥー','tatuagem','tattoo'),
 'ャ':('シャツ','camisa','shirt'),'ュ':('ジュース','suco','juice'),'ョ':('ショッピング','compras','shopping'),'ッ':('ベッド','cama','bed'),
 'ヵ':('一ヵ月','um mês','one month'),'ヶ':('三ヶ月','três meses','three months'),
 'キャ':('キャンプ','acampamento','camping'),'キュ':('バーベキュー','churrasco','barbecue'),'キョ':('キョロキョロ','olhar em volta','looking around'),
 'ギャ':('ギャラリー','galeria','gallery'),'ギュ':('レギュラー','regular; titular','regular'),'ギョ':('ギョーザ','guioza','gyoza'),
 'シャ':('シャツ','camisa','shirt'),'シュ':('シューズ','tênis; sapatos','shoes'),'ショ':('ショッピング','compras','shopping'),
 'ジャ':('ジャム','geleia','jam'),'ジュ':('ジュース','suco','juice'),'ジョ':('ジョギング','corrida (jogging)','jogging'),
 'チャ':('チャンス','chance','chance'),'チュ':('チューリップ','tulipa','tulip'),'チョ':('チョコレート','chocolate','chocolate'),
 'ニャ':('ニャー','miau','meow'),'ニュ':('ニュース','notícias','news'),'ニョ':('ニョッキ','nhoque','gnocchi'),
 'ヒュ':('ヒューズ','fusível','fuse'),'ヒョ':('ヒョウ','leopardo','leopard'),
 'ビュ':('インタビュー','entrevista','interview'),'ピュ':('コンピューター','computador','computer'),'ピョ':('ピョンピョン','saltitando','hopping'),
 'ミャ':('ミャンマー','Mianmar','Myanmar'),'ミュ':('ミュージック','música','music'),'リュ':('リュック','mochila','backpack'),
 'ファ':('ファン','fã','fan'),'フィ':('フィルム','filme (fotográfico)','film'),'フェ':('カフェ','café (lugar)','café'),'フォ':('フォーク','garfo','fork'),
 'ティ':('パーティー','festa','party'),'ディ':('ディナー','jantar','dinner'),'トゥ':('タトゥー','tatuagem','tattoo'),
 'チェ':('チェック','verificação','check'),'シェ':('シェフ','chef','chef'),'ジェ':('ジェット','jato','jet'),
 'ウィ':('ウィンドウ','janela (de computador)','window'),'ウェ':('ウェブ','web','web'),'ウォ':('ウォッカ','vodca','vodka'),
 'ヴァ':('ヴァイオリン','violino','violin'),'ヴィ':('ヴィーナス','Vênus','Venus'),'ヴェ':('ヴェネツィア','Veneza','Venice'),'ヴォ':('ヴォーカル','vocal','vocals'),
 'クァ':('クァルテット','quarteto','quartet'),'クォ':('クォーター','um quarto (1/4)','quarter'),
}
# leituras de exemplos que usam kanji
EX_READING = {'一ヵ月': 'いっかげつ', '三ヶ月': 'さんかげつ'}

KANA_NOTES = {
 'は': 'Como partícula de tópico, lê-se “wa”.', 'へ': 'Como partícula de direção, lê-se “e”.',
 'を': 'Hoje usado quase só como partícula de objeto; pronuncia-se “o”.', 'ん': 'Único som que é só consoante; soa como “n” ou “m” conforme a letra seguinte.',
 'ぢ': 'Raro: soa igual a じ. Aparece em palavras como はなぢ.', 'づ': 'Raro: soa igual a ず. Aparece em palavras como つづく.',
 'ゔ': 'Representa o som “v” de palavras estrangeiras; na prática quase sempre se usa ヴ em katakana.',
 'っ': 'Não tem som próprio: indica uma pausa curta e dobra a consoante seguinte (きって = kitte).',
 'ゎ': 'Forma arcaica, praticamente fora de uso.', 'ヲ': 'Rara; aparece em textos escritos só em katakana.',
 'ヂ': 'Rara: soa igual a ジ.', 'ヅ': 'Rara: soa igual a ズ.', 'ヴ': 'Representa o som “v” de palavras estrangeiras.',
 'ッ': 'Não tem som próprio: dobra a consoante seguinte (ベッド = beddo).', 'ヮ': 'Rara, usada em algumas transcrições.',
 'ヵ': 'Usado em contadores, como em 一ヵ月 (um mês). Lê-se “ka”.', 'ヶ': 'Usado em contadores e nomes de lugares (三ヶ月, 霞ヶ関). Lê-se “ka” ou “ga”, apesar da forma de ケ.',
 'ー': 'Traço de prolongamento de vogal.',
}

def kana_meaning(ch, group, ro):
    base = to_hira(ch)
    if base == 'ん': return (['som nasal “n”'], ['nasal sound “n”'])
    if base == 'を': return (['partícula de objeto “o”'], ['object particle “o”'])
    if base in 'っ': return (['tsu pequeno (consoante dobrada)'], ['small tsu (doubled consonant)'])
    if group == 'pequeno':
        if base in 'ゃゅょ': return (['“%s” pequeno (forma sílabas combinadas)' % ro], ['small “%s” (forms combined syllables)' % ro])
        if base in 'ゕゖ': return (['“%s” pequeno (contadores)' % ro], ['small “%s” (counters)' % ro])
        if base == 'ゎ': return (['“wa” pequeno'], ['small “wa”'])
        return (['vogal pequena “%s”' % ro], ['small vowel “%s”' % ro])
    return (['sílaba “%s”' % ro], ['syllable “%s”' % ro])

DIFF_KANA = {'basico': 'iniciante', 'dakuten': 'iniciante', 'handakuten': 'iniciante', 'pequeno': 'intermediario', 'combinacao': 'intermediario', 'estrangeiro': 'avancado'}
ADVANCED_KANA = set('ゔヴゎヮヵヶヂヅぢづ')

# ------------------------------------------------------------------ stroke paths (simplified, from the design)
def load_paths():
    src = open(os.path.join(HERE, '..', 'common.py'), encoding='utf-8').read()
    paths = {}
    for m in re.finditer(r"\{ c: '(.)',.*?p: \[(.*?)\] \}", src):
        paths[m.group(1)] = re.findall(r"'([^']*)'", m.group(2))
    return paths
PATHS = load_paths()

def stroke_order(ch, strokes):
    p = PATHS.get(ch)
    if p and len(p) == strokes:
        return {'source': 'kaku-simplificado', 'viewBox': '0 0 100 100', 'paths': p,
                'note': 'Traçado simplificado desenhado à mão; substituir por KanjiVG em produção.'}
    return None

# ------------------------------------------------------------------ build kana
def example(word, pt, en):
    reading = EX_READING.get(word, word)
    return {'word': word, 'reading': reading, 'romaji': romaji(reading), 'pt': pt, 'en': en}

def kana_entry(ch, category, group):
    kata = category == 'katakana'
    ro = romaji(ch)
    if to_hira(ch) == 'っ': ro = '(dobra a consoante)'
    pt, en = kana_meaning(ch, group, ro)
    diff = 'avancado' if (ch in ADVANCED_KANA) else DIFF_KANA[group]
    ex = []
    if ch in KANA_EX:
        w, a, b = KANA_EX[ch]; ex.append(example(w, a, b))
    n = strokes_of(ch, kata)
    e = {
        'id': '%s:%s' % (category, ch), 'char': ch, 'category': category, 'group': group,
        'romaji': ro, 'reading': to_hira(ch),
        'meaning': {'pt': pt, 'en': en},
        'jlpt': None, 'difficulty': diff, 'strokes': n,
        'strokeOrder': stroke_order(ch, n),
        'examples': ex,
    }
    if len(ch) > 1: e['components'] = list(ch)
    note = KANA_NOTES.get(ch) or KANA_NOTES.get(to_hira(ch)) if category == 'hiragana' else KANA_NOTES.get(ch)
    if note: e['note'] = note
    return e

def kana_set(category):
    conv = (lambda s: s) if category == 'hiragana' else to_kata
    items = []
    for c in H_BASIC: items.append(kana_entry(conv(c), category, 'basico'))
    for c in H_DAKU_LIST: items.append(kana_entry(conv(c), category, 'dakuten'))
    for c in H_HANDA_LIST: items.append(kana_entry(conv(c), category, 'handakuten'))
    items.append(kana_entry(conv('ゔ'), category, 'dakuten'))
    if category == 'hiragana':
        for c in H_SMALL_LIST: items.append(kana_entry(c, category, 'pequeno'))
    else:
        for c in K_SMALL_LIST: items.append(kana_entry(c, category, 'pequeno'))
    for c in H_YOUON: items.append(kana_entry(conv(c), category, 'combinacao'))
    if category == 'katakana':
        for c in K_EXTENDED: items.append(kana_entry(c, category, 'estrangeiro'))
    return items

# ------------------------------------------------------------------ build kanji
USAGE = {'N5': (5, 'muito alto'), 'N4': (4, 'alto'), 'N3': (3, 'médio'), 'N2': (2, 'moderado'), 'N1': (1, 'baixo')}
DIFF_KANJI = {'N5': 'iniciante', 'N4': 'iniciante', 'N3': 'intermediario', 'N2': 'avancado', 'N1': 'avancado'}

def kun_item(k):
    stem, _, oku = k.partition('.')
    disp = stem + ('(%s)' % oku if oku else '')
    if oku:
        full = romaji(stem + oku); pre = romaji(stem.rstrip('っ'))
        ro = pre + '(' + full[len(pre):] + ')' if full.startswith(pre) else full
    else:
        ro = romaji(stem)
    return {'kana': k.replace('.', ''), 'display': disp, 'okurigana': oku or None, 'romaji': ro}

import glob
def kanji_lines():
    files = [os.path.join(HERE, 'kanji.txt')] + sorted(glob.glob(os.path.join(HERE, 'kanji_extra_*.txt')))
    for fn in files:
        for ln, line in enumerate(open(fn, encoding='utf-8'), 1):
            line = line.strip()
            if not line or line.startswith('#'): continue
            f = line.split('|')
            if len(f) == 14: f = f[:9] + ['', '', ''] + f[11:]
            assert len(f) in (12, 15), (os.path.basename(fn), ln, len(f), line)
            yield f

def jlpt_levels():
    lv = {}
    for L in ['n5', 'n4', 'n3', 'n2', 'n1']:
        for fn in sorted(glob.glob(os.path.join(HERE, 'jlpt', L + '_*'))):
            for c in open(fn, encoding='utf-8').read().strip():
                lv[c] = L.upper()
    return lv

def build_kanji():
    items, seen = [], set()
    LV = jlpt_levels()
    for f in kanji_lines():
        ch, pt, en, on, kun, jlpt, grade, strokes, exs, sja, spt, sen = f[:12]
        jlpt = LV.get(ch, jlpt)
        assert ch not in seen, 'duplicado: ' + ch
        seen.add(ch)
        on_l = [] if on == '—' else on.split(',')
        kun_l = [] if kun == '—' else kun.split(',')
        examples = []
        for ex in exs.split('¦'):
            w, r, a, b = ex.split(':')
            assert ch in w, 'exemplo sem o kanji: %s %s' % (ch, w)
            examples.append({'word': w, 'reading': r, 'romaji': romaji(r), 'pt': a, 'en': b})
        assert (not sja) or ch in sja, 'frase sem o kanji: ' + ch
        ons = [{'kana': o, 'romaji': romaji(o)} for o in on_l]
        kuns = [kun_item(k) for k in kun_l]
        prim = kuns[0] if kuns else None
        n = int(strokes)
        g = int(grade)
        items.append({
            'id': 'kanji:' + ch, 'char': ch, 'category': 'kanji', 'group': 'joyo',
            'romaji': prim['romaji'] if prim else ons[0]['romaji'],
            'reading': prim['display'] if prim else ons[0]['kana'],
            'meaning': {'pt': [s.strip() for s in pt.split(';')], 'en': [s.strip() for s in en.split(';')]},
            'jlpt': jlpt, 'difficulty': DIFF_KANJI[jlpt], 'strokes': n,
            'strokeOrder': stroke_order(ch, n),
            'examples': examples,
            'readings': {'on': ons, 'kun': kuns},
            'readingsRomaji': [o['romaji'] for o in ons] + [k['romaji'] for k in kuns],
            'grade': g, 'gradeLabel': (('%dº ano (primário)' % g) if g <= 6 else 'ensino secundário') if g else '',
            'usage': {'level': USAGE[jlpt][0], 'label': USAGE[jlpt][1]},
            'sentence': {'ja': sja, 'pt': spt, 'en': sen} if sja else None,
            'detail': 'completo' if sja else 'essencial',
        })
    order = {'N5': 0, 'N4': 1, 'N3': 2, 'N2': 3, 'N1': 4}
    items.sort(key=lambda e: order[e['jlpt']])  # estável: mantém a ordem temática dentro do nível
    return items

REQUESTED = '''一 二 三 四 五 六 七 八 九 十 百 千 万 円 日 月 年 時 分 半 今 前 後 午 毎 週 曜 火 水 木 金 土 人 男 女 子 父 母 兄 弟 姉 妹 友 親
学 校 生 先 教 本 文 字 語 読 書 聞 話 言 英 数 問 答 上 下 左 右 中 外 東 西 南 北 内 近 遠 所 方 国 家 店 駅 道 町 村 市 県 京 社 寺 院 室
行 来 帰 見 聞 話 言 読 書 食 飲 買 売 会 休 入 出 立 座 歩 走 使 作 持 待 知 思 考 教 習 働 住 始 終 開 閉
大 小 高 安 新 古 長 短 多 少 早 遅 明 暗 白 黒 赤 青 好 悪 楽 難 同 強 弱 山 川 海 空 雨 雪 風 花 草 木 林 森 石 田 天 気
目 耳 口 手 足 頭 顔 心 体 力 声 車 電 駅 道 通 乗 降 自 転 食 飲 米 肉 魚 野 菜 茶 水 酒 飯 会 社 仕 事 員 働 業 金 円 物 者 場
何 私 自 名 国 本 物 事 方 間 気 電 車 力 心 世 界 理 意 味 必 要 全 無 有'''

def compact(data):
    comps, rads, ftypes = {}, {}, {}
    def ckey(d):
        if d.get('lookalike'): return d['c'] + '|!'
        k = d['c'] + '|' + d['form']
        comps.setdefault(k, [d['form'], d.get('meaning', ''), d.get('ref'), d.get('standard')])
        return k
    out = []
    for e in data['characters']:
        if e['category'] != 'kanji':
            out.append({k: v for k, v in e.items() if v not in (None, [], '')}); continue
        r = e['radical']
        rads[r['standard']] = [r['number'], r['meaning']['pt'], r['meaning']['en']]
        f = e['formation']
        fz = None
        if f:
            ftypes[f['type']] = [f['label'], f['description']]
            fz = [f['type'], f['note'] or '', [[ckey(p), p['role'][0], p.get('reading', '')] for p in f['parts']]]
        z = {'c': e['char'], 'pt': e['meaning']['pt'], 'en': e['meaning']['en'], 'j': e['jlpt'], 'n': e['strokes'],
             'on': [o['kana'] for o in e['readings']['on']], 'kun': [k['kana'] if not k['okurigana'] else k['display'].replace('(', '.').replace(')', '') for k in e['readings']['kun']],
             'ex': [[x['word'], x['reading'], x['romaji'], x['pt'], x['en']] for x in e['examples']],
             'r': [r['char'], r['standard'], r['name']], 'd': [ckey(x) for x in e['decomposition']],
             'cc': e['containsComponents'], 'u': e['usedIn'], 'rel': e['related']}
        if e['grade']: z['g'] = e['grade']
        if fz: z['f'] = fz
        if e['sentence']: z['s'] = [e['sentence']['ja'], e['sentence']['pt'], e['sentence']['en']]
        if e['strokeOrder']: z['so'] = e['strokeOrder']['paths']
        z['rj'] = [o['romaji'] for o in e['readings']['on']] + [k['romaji'] for k in e['readings']['kun']]
        out.append(z)
    return {'meta': data['meta'], 'compact': 1, 'comps': comps, 'rads': rads, 'ftypes': ftypes, 'characters': out}

def main():
    hira, kata, kanji = kana_set('hiragana'), kana_set('katakana'), build_kanji()
    from composition import enrich
    unknown = enrich(kanji)
    print('componentes sem significado:', ''.join(unknown))
    allc = hira + kata + kanji
    ids = [e['id'] for e in allc]
    assert len(ids) == len(set(ids)), 'ids duplicados'
    req = list(dict.fromkeys(REQUESTED.split()))
    have = {e['char'] for e in kanji}
    missing = [k for k in req if k not in have]
    assert not missing, 'faltando: ' + ''.join(missing)
    no_ex = [e['char'] for e in hira + kata if not e['examples']]
    meta = {
        'name': 'Kaku — base de caracteres japoneses', 'schemaVersion': 2,
        'generatedAt': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'romanization': 'Hepburn em estilo wāpuro (vogais longas escritas por extenso: kyou, koohii)',
        'categories': ['hiragana', 'katakana', 'kanji'],
        'groups': {'basico': 'Básicos', 'dakuten': 'Dakuten (゛)', 'handakuten': 'Handakuten (゜)', 'pequeno': 'Pequenos', 'combinacao': 'Combinações (yōon)', 'estrangeiro': 'Sons estrangeiros', 'joyo': 'Jōyō kanji'},
        'difficulty': {'iniciante': 'Iniciante', 'intermediario': 'Intermediário', 'avancado': 'Avançado'},
        'jlpt': ['N5', 'N4', 'N3', 'N2', 'N1'],
        'counts': {'hiragana': len(hira), 'katakana': len(kata), 'kanji': len(kanji), 'total': len(allc)},
        'caveats': [
            'Níveis JLPT são aproximados: desde 2010 o exame não publica listas oficiais de kanji; seguimos a classificação usual das listas de estudo.',
            '“usage” (nível de uso) é derivado do nível JLPT, não de uma contagem de frequência em corpus.',
            'formation (origem histórica) só é preenchida quando a classificação tradicional é consolidada; decomposition é apenas a análise visual e não implica origem.',
            'strokeOrder só está preenchido para os caracteres com traçado simplificado do protótipo; o campo foi pensado para receber dados do KanjiVG.',
        ],
    }
    data = {'meta': meta, 'characters': allc}
    dump = lambda obj, name: json.dump(obj, open(os.path.join(OUT, name), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    dump(data, 'kaku-caracteres.json')
    dump({'meta': meta, 'characters': hira}, 'hiragana.json')
    dump({'meta': meta, 'characters': kata}, 'katakana.json')
    dump({'meta': meta, 'characters': kanji}, 'kanji.json')
    js = '/* Kaku — base de caracteres (gerado por build_data.py; não editar à mão). Formato compacto: expandido no navegador. */\nwindow.KAKU_DATA = ' + json.dumps(compact(data), ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(OUT, 'kaku-data.js'), 'w', encoding='utf-8').write(js)
    print(meta['counts'], 'kanji pedidos:', len(req), '| kana sem exemplo:', ''.join(no_ex))
    print('js bytes', len(js.encode()))

if __name__ == '__main__':
    main()
