#Embedded file name: /build/PyCLIP/android/app/mod_ply.py
import sys
sys.path.insert(0, '../..')
sys.path.insert(0, './ply')
import ply.lex as lex
import ply.yacc as yacc
import time

class Parser():
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.names = {}
        lex.lex(module=self)
        yacc.yacc(module=self)

    def calculate(self, value):
        return yacc.parse(value, debug=0)


class Calc(Parser):
    result = ''
    tokens = ('NAME', 'HEXSTR', 'NUMBER', 'HEX', 'FLOAT', 'PLUS', 'MINUS', 'BAND', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS', 'NEQ', 'LPAREN', 'RPAREN', 'LT', 'GT', 'GE', 'LE', 'AND', 'OR', 'SHIFT', 'QUEST', 'DOTS', 'STRCONST', 'HEXTOASCII', 'HEXTOSTR', 'HEXTODEC')
    t_OR = '\\|\\|'
    t_AND = '\\&\\&'
    t_BAND = '\\&'
    t_EQUALS = '=='
    t_NEQ = '\\!='
    t_PLUS = '\\+'
    t_MINUS = '-'
    t_EXP = '\\*\\*'
    t_TIMES = '\\*'
    t_DIVIDE = '/'
    t_LPAREN = '\\('
    t_RPAREN = '\\)'
    t_SHIFT = '\\#'
    t_QUEST = '\\?'
    t_DOTS = '\\:'
    t_LT = '<'
    t_GT = '>'
    t_LE = '<='
    t_GE = '>='
    t_STRCONST = '\\"([^\\\\\\n]|(\\\\.))*?\\"'
    t_ignore = ' \t'

    def t_HEXTOASCII(self, t):
        return t

    t_HEXTOASCII.func_doc = '\\$HexaToAscii\\$\\([a-fA-F0-9][a-fA-F0-9]*\\)'

    def t_HEXTOSTR(self, t):
        return t

    t_HEXTOSTR.func_doc = '\\$HexaToString\\$\\([a-fA-F0-9][a-fA-F0-9]*\\)'

    def t_HEXTODEC(self, t):
        return t

    t_HEXTODEC.func_doc = '\\$HexaToDec\\$\\([a-fA-F0-9][a-fA-F0-9]*\\)'

    def t_HEX(self, t):
        t.value = int(t.value, 0)
        return t

    t_HEX.func_doc = '0x[a-fA-F0-9][a-fA-F0-9]*'

    def t_NAME(self, t):
        return t

    t_NAME.func_doc = '[a-zA-Z_][a-zA-Z0-9_]*'

    def t_FLOAT(self, t):
        t.value = float(t.value)
        return t

    t_FLOAT.func_doc = '((\\d*\\.\\d+)(E[\\+-]?\\d+)?|([1-9]\\d*E[\\+-]?\\d+))'

    def t_HEXSTR(self, t):
        t.value = t.value
        return t

    t_HEXSTR.func_doc = '[a-fA-F0-9]*[a-fA-F][a-fA-F0-9]*'

    def t_NUMBER(self, t):
        t.value = int(t.value)
        return t

    t_NUMBER.func_doc = '\\d+'

    def t_newline(self, t):
        t.lexer.lineno += t.value.count('\n')

    t_newline.func_doc = '\\n+'

    def t_error(self, t):
        print "PLY:Parser:Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    precedence = (('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
     ('left', 'EXP'),
     ('left', 'SHIFT'),
     ('left', 'LE'),
     ('left', 'GE'),
     ('left', 'LT'),
     ('left', 'GT'),
     ('left', 'OR'),
     ('left', 'AND'),
     ('right', 'UMINUS'))

    def p_statement_expr(self, p):
        p[0] = p[1]

    p_statement_expr.func_doc = 'statement : expression'

    def p_expression_binop(self, p):
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '**':
            p[0] = p[1] ** p[3]
        elif p[2] == '&':
            p[0] = p[1] & p[3]

    p_expression_binop.func_doc = '\n        expression : expression MINUS expression\n                   | expression TIMES expression\n                   | expression DIVIDE expression\n                   | expression EXP expression\n                   | expression BAND expression\n        '

    def p_expression_plus(self, p):
        if type(p[1]) is str or type(p[3]) is str:
            p[0] = str(p[1]).replace('"', '') + str(p[3])
        else:
            p[0] = p[1] + p[3]

    p_expression_plus.func_doc = 'expression : expression PLUS expression'

    def p_expression_uminus(self, p):
        p[0] = -p[2]

    p_expression_uminus.func_doc = 'expression : MINUS expression %prec UMINUS'

    def p_expression_equals(self, p):
        if p[1] == p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_equals.func_doc = 'expression : expression EQUALS expression'

    def p_expression_notequals(self, p):
        if p[1] != p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_notequals.func_doc = 'expression : expression NEQ expression'

    def p_expression_le(self, p):
        if p[1] <= p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_le.func_doc = 'expression : expression LE expression'

    def p_expression_lt(self, p):
        if p[1] < p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_lt.func_doc = 'expression : expression LT expression'

    def p_expression_ge(self, p):
        if p[1] >= p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_ge.func_doc = 'expression : expression GE expression'

    def p_expression_gt(self, p):
        if p[1] > p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_gt.func_doc = 'expression : expression GT expression'

    def p_expression_or(self, p):
        if p[1] or p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_or.func_doc = 'expression : expression OR expression'

    def p_expression_and(self, p):
        if p[1] and p[3]:
            p[0] = 1
        else:
            p[0] = 0

    p_expression_and.func_doc = 'expression : expression AND expression'

    def p_expression_shift(self, p):
        p[0] = p[1] >> p[3] & 1

    p_expression_shift.func_doc = 'expression : expression SHIFT expression'

    def p_expression_condition(self, p):
        if p[1]:
            p[0] = p[3]
        else:
            p[0] = p[5]

    p_expression_condition.func_doc = 'expression : expression QUEST expression DOTS expression'

    def p_expression_strconst(self, p):
        p[0] = p[1]

    p_expression_strconst.func_doc = 'expression : STRCONST'

    def p_expression_HexaToDec(self, p):
        tmp = p[1]
        tmp = tmp.replace('$HexaToDec$(', '')
        tmp = tmp.replace(')', '')
        p[0] = tmp

    p_expression_HexaToDec.func_doc = 'expression : HEXTODEC'

    def p_expression_HexaToString(self, p):
        tmp = p[1]
        tmp = tmp.replace('$HexaToString$(', '')
        tmp = tmp.replace(')', '')
        p[0] = tmp

    p_expression_HexaToString.func_doc = 'expression : HEXTOSTR'

    def p_expression_HexaToAscii(self, p):
        tmp = p[1]
        tmp = tmp.replace('$HexaToAscii$(', '')
        tmp = tmp.replace(')', '')
        tmp = tmp.replace(' ', '')
        if len(tmp) % 2:
            tmp = '0' + tmp
        p[0] = tmp.decode('hex')

    p_expression_HexaToAscii.func_doc = 'expression : HEXTOASCII'

    def p_expression_group(self, p):
        p[0] = p[2]

    p_expression_group.func_doc = 'expression : LPAREN expression RPAREN'

    def p_expression_number(self, p):
        p[0] = p[1]

    p_expression_number.func_doc = 'expression : NUMBER'

    def p_expression_hex(self, p):
        p[0] = p[1]

    p_expression_hex.func_doc = 'expression : HEX'

    def p_expression_hexstr(self, p):
        p[0] = p[1]

    p_expression_hexstr.func_doc = 'expression : HEXSTR'

    def p_expression_float(self, p):
        p[0] = p[1]

    p_expression_float.func_doc = 'expression : FLOAT'

    def p_expression_name(self, p):
        try:
            p[0] = self.names[p[1]]
        except LookupError:
            print "PLY:Parser:Undefined name '%s'" % p[1]
            p[0] = 0

    p_expression_name.func_doc = 'expression : NAME'

    def p_error(self, p):
        print "PLY:Parser:Syntax error at '%s'" % p.value


if __name__ == '__main__':
    tb = time.time()
    calc = Calc()
    te = time.time()
    print 'init:' + str(te - tb)
    value = '(((_STATUSDTC&amp;0x1F)== 0x01)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?2:((((_STATUSDTC&amp;0x1F)== 0x02)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?4:((((_STATUSDTC&amp;0x1F)== 0x03)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?6:((((_STATUSDTC&amp;0x9F)== 0x9F)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?8:((((_STATUSDTC&amp;0x9F)== 0x8E)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?10:((((_STATUSDTC&amp;0x9F)== 0x89)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?14:((((_STATUSDTC&amp;0x9F)== 0x93)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?16:((((_STATUSDTC&amp;0x9F)== 0x88)&amp;&amp; ((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?12:((((_STATUSDTC&amp;0x1F)== 0x01)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?1:((((_STATUSDTC&amp;0x1F)== 0x02)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?3:((((_STATUSDTC&amp;0x1F)== 0x03)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?5:((((_STATUSDTC&amp;0x9F)== 0x9F)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?7:((((_STATUSDTC&amp;0x9F)== 0x8E)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?9:((((_STATUSDTC&amp;0x9F)== 0x89)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?13:((((_STATUSDTC&amp;0x9F)== 0x93)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?15:((((_STATUSDTC&amp;0x9F)== 0x88)&amp;&amp; ((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93))))?11:0)))))))))))))))'
    value = value.replace('&amp;', '&')
    value = value.replace('_STATUSDTC', '0x' + 'C9')
    tb = time.time()
    print calc.calculate(value)
    te = time.time()
    print 'calc:' + str(te - tb)
    value = '((_STATUSDTC#5== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93)))?1:(((_STATUSDTC#6== 0x01)&amp;&amp;(((_STATUSDTC&amp;0x1F)== 0x01)||((_STATUSDTC&amp;0x1F)== 0x02)||((_STATUSDTC&amp;0x1F)== 0x03)||((_STATUSDTC&amp;0x9F)== 0x9F)||((_STATUSDTC&amp;0x9F)== 0x8E)||((_STATUSDTC&amp;0x9F)== 0x88)||((_STATUSDTC&amp;0x9F)== 0x89)||((_STATUSDTC&amp;0x9F)== 0x93)))?2:0)'
    value = value.replace('&amp;', '&')
    value = value.replace('_STATUSDTC', '0x' + 'D3')
    tb = time.time()
    print calc.calculate(value)
    te = time.time()
    print 'calc:' + str(te - tb)
    value = '(1.0 * (100*_VXX_SPG_PWM_SP)) /256'
    value = value.replace('&amp;', '&')
    value = value.replace('_VXX_SPG_PWM_SP', '0x' + 'D3')
    tb = time.time()
    print calc.calculate(value)
    te = time.time()
    print 'calc:' + str(te - tb)
    value = '(_MODULE_ABSENT_9!= 0x00)?(((_BOOLEEN_CONTACT_EMBRAYAGE== 0x00)||(_BOOLEEN_CONTACT_EMBRAYAGE== 0x01))?((_BOOLEEN_CONTACT_EMBRAYAGE== 0x01)?1:((_BOOLEEN_CONTACT_EMBRAYAGE== 0x00)?0:1)):0):0'
    value = value.replace('&amp;', '&')
    value = value.replace('_MODULE_ABSENT_9', '0x' + '01')
    value = value.replace('_BOOLEEN_CONTACT_EMBRAYAGE', '0x' + '00')
    tb = time.time()
    print calc.calculate(value)
    te = time.time()
    print 'calc:' + str(te - tb)
    value = '_VIN'
    value = value.replace('_VIN', '11223344556677889900AABBCCDDEEFF1122')
    tb = time.time()
    print calc.calculate(value)
    te = time.time()
    print 'calc:' + str(te - tb)
