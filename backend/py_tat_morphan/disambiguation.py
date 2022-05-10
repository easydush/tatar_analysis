# -*- coding: UTF-8 -*-
#!/usr/bin/python

import os
import json


def load_disam_rules(filename):
    """
        Loads rules from json file
    """
    if os.path.isfile(filename):
        with open(filename, 'r') as stream:
            disam_rules = json.loads(stream.read())
            return disam_rules

def is_that_chain(chain, pattern):
    """
        Checks if chain fits the pattern
        :chain string
        :pattern string
    """
    chain_set = set(chain.split('+')) | set([''])
    pattern_set = set(pattern.split('+'))
    if not len(pattern_set - chain_set):
        return True

def is_that_amtype(chains, amtype_pattern):
    """
        Checks if amtype fits the amtype_pattern
        :chains string (delimeter ';')
        :amtype_pattern string (delimeter '|')
    """
    chains = chains.strip(';').split(';')
    patterns = amtype_pattern.split('|')
    found = False
    for chain in chains:
        for pattern in patterns:
            if is_that_chain(chain, pattern):
                found = True
                patterns.remove(pattern)
                break
        if found:
            # change to False and check next chain
            found = False
        else:
            return False
    return True

def is_amtype_pattern(amtype_pattern, errors=[]):
    """
        Checks if amtype is formed in proper way
    """
    err = []
    morphemes = [u"POSS_1SG(Ым)", u"NUM_COLL(АУ)", u"PROF(чЫ)", u"LOC(ДА)", u"1SG(мЫн)", 
                 u"ATTR_LOC(ДАгЫ)", u"PREC_2(сАнА)", u"ATTR_GEN(нЫкЫ)", u"PST_DEF(ДЫ)", 
                 u"PART", u"ATTR_MUN(лЫ)", u"IMP_PL(ЫгЫз)", u"RAR_2(ЫштЫр)", u"3PL(ЛАр)", 
                 u"SIM_2(сыман)", u"POST", u"1PL(к)", u"HOR_SG(Йм)", u"FUT_DEF(АчАк)", 
                 u"EQU(чА)", u"OBL(ЙсЫ)", u"PROB(ДЫр)", u"PCP_FUT(Ыр)", u"RAR_1(ГАлА)", 
                 u"NUM_APPR(лАп)", u"INF_1(ЫргА)", u"ATTR_ABES(сЫз)", u"N", u"INTRJ", 
                 u"POSS_2SG(Ың)", u"VN_1(у/ү/в)", u"POSS_2PL(ЫгЫз)", u"PST_INDF(ГАн)", 
                 u"IMP_SG()", u"ABL(ДАн)", u"1PL(бЫз)", u"Num", u"PCP_PR(чЫ)", u"MOD", 
                 u"NMLZ(лЫк)", u"ADVV_NEG(ЙчА)", u"ADVV_ACC(Ып)", u"DIR_LIM(ГАчА)", u"Adj", 
                 u"PASS(Ыл)", u"DIM(чЫк)", u"ADVV_SUCC(ГАнчЫ)", u"JUS_PL(сЫннАр)", u"DIR(ГА)", 
                 u"HOR_PL(Йк)", u"RECP(Ыш)", u"PCP_PS(ГАн)", u"ACC(нЫ)", u"CNJ", 
                 u"FUT_INDF_NEG(мАс)", u"MSRE(лАтА)", u"NEG(мА)", u"REFL(Ын)", u"2SG(сЫң)", 
                 u"NUM_DISR(шАр)", u"COMP(рАк)", u"2PL(гЫз)", u"USIT(чАн)", u"SIM_1(ДАй)", 
                 u"GEN(нЫң)", u"DESID(мАкчЫ)", u"CAUS(ДЫр)", u"PRES(Й)", u"1SG(м)", u"AFC(кАй)", 
                 u"3SG(ДЫр)", u"Sg", u"V", u"2PL(сЫз)", u"PCP_FUT(АчАк)", u"Nom", u"INT(мЫ)", 
                 u"VN_2(Ыш)", u"ADVV_ANT(ГАч)", u"SIM_3(сымак)", u"POSS_1PL(ЫбЫз)", 
                 u"INT_MIR(мЫни)", u"PL(ЛАр)", u"POSS_3(СЫ)", u"IMIT", u"PREM(мАгАй)", 
                 u"INF_2(мАк)", u"PN", u"DISTR(лАп)", u"Adv", u"2SG(ң)", u"CAUS(т)", 
                 u"PREC_1(чЫ)", u"INF_1(скА)", u"NUM_ORD(ЫнчЫ)", u"PSBL(лЫк)", u"JUS_SG(сЫн)", 
                 u"PCP_FUT(мАс)", u"PROP", u"COND(сА)",
                 u"POSS_1SG", u"NUM_COLL", u"PROF", u"LOC", u"1SG", u"ATTR_LOC", u"PREC_2", 
                 u"ATTR_GEN", u"PST_DEF", u"PART", u"ATTR_MUN", u"IMP_PL", u"RAR_2", u"3PL", 
                 u"SIM_2", u"POST", u"1PL", u"HOR_SG", u"FUT_DEF", u"EQU", u"OBL", u"PROB", 
                 u"PCP_FUT", u"RAR_1", u"NUM_APPR", u"INF_1", u"ATTR_ABES", u"N", u"INTRJ", 
                 u"POSS_2SG", u"VN_1", u"POSS_2PL", u"PST_INDF", u"IMP_SG", u"ABL", u"1PL", 
                 u"Num", u"PCP_PR", u"MOD", u"NMLZ", u"ADVV_NEG", u"ADVV_ACC", u"DIR_LIM", 
                 u"Adj", u"PASS", u"DIM", u"ADVV_SUCC", u"JUS_PL", u"DIR", u"HOR_PL", u"RECP", 
                 u"PCP_PS", u"ACC", u"CNJ", u"FUT_INDF_NEG", u"MSRE", u"NEG", u"REFL", u"2SG", 
                 u"NUM_DISR", u"COMP", u"2PL", u"USIT", u"SIM_1", u"GEN", u"DESID", u"CAUS", 
                 u"PRES", u"1SG", u"AFC", u"3SG", u"Sg", u"V", u"2PL", u"PCP_FUT", u"Nom", u"INT", 
                 u"VN_2", u"ADVV_ANT", u"SIM_3", u"POSS_1PL", u"INT_MIR", u"PL", u"POSS_3", u"IMIT", 
                 u"PREM", u"INF_2", u"PN", u"DISTR", u"Adv", u"2SG", u"CAUS", u"PREC_1", u"INF_1", 
                 u"NUM_ORD", u"PSBL", u"JUS_SG", u"PCP_FUT", u"PROP", u"COND", u""]
    if len(amtype_pattern.split('|')) < 2:
        err.append((1, 'There must be ambiguity. To separate use "|" sign.'))
    for chain in amtype_pattern.split('|'):
        for morpheme in chain.split('+'):
            if morpheme not in morphemes:
                err.append((2, 'There is no such morpheme: "%s"' % morpheme))
    if len(err) > 0:
        errors += err[:]
        return False
    return True

def get_chain_by_pattern(chains, pattern):
    """
        From chains set choose that fits the pattern
        :chains
    """
    chains = chains.strip(';').split(';')
    for chain in chains:
        if is_that_chain(chain, pattern):
            return chain

def apply_simple_rule(sentence, index, rule_type, searched):
    """
        Checks if this word (sentence[index]) fits the rule
    """    
    if index < 0 or index > len(sentence)-1:
        # checks for sentence's borders
        return rule_type == 4
    elif rule_type == 1:
        # checks for exact word
        if sentence[index][0] == searched:
            return True
    elif rule_type == 2:
        # checks for exact chain
        chains = sentence[index][1].strip(';').split(';')
        for chain in chains:
            if chain[-len(searched):] == searched.strip(';'):
                return True
    elif rule_type == 3:
        # checks for exact morpheme
        # print('\tWord=%s, searched=%s' % (sentence[index][1], searched))
        chains = sentence[index][1].strip(';').split(';')
        for chain in chains:
            if searched in chain.split('+'):
                return True
    elif rule_type == 5:
        # checks if first letter is upper case
        if sentence[index][0][0].isupper():
            return True
    elif rule_type == 6:
        # checks if there is searched lemma
        chains = sentence[index][1].strip(';').split(';')
        for chain in chains:
            if chain[:len(searched)] == searched.strip(';'):
                return True
    return False

def disambiguate_word(sentence, index, rules):
    """
        word disambiguation
        :sentence list of words
        :index number of word needed to disambiguate
        :rules list of rules needed to check with
    """
    if not rules:
        return None
    for (pattern, context_rules, exceptions) in rules:
        if is_that_amtype(sentence[index][1], pattern):
            # print('%s - %s' % (sentence[index][1], pattern))
            # if it is an exception, disambiguate using exceptions
            result = disambiguate_word(sentence, index, exceptions)
            if result:
                return result
            # it is not exception, so apply rules
            for (rule, result_pattern) in context_rules:
                expression = True
                for (rule_type, searched, first_index, last_index, operand) in rule:
                    result = False
                    for i in range(first_index, last_index+1):
                        result = apply_simple_rule(sentence, index+i, rule_type, searched)
                        # print('simple rule(%s): rule_type=%s, searched=%s, index=%s' % (result, rule_type, searched, index+i))
                        if result:
                            break
                    if operand == 'and':
                        expression = expression and result
                    elif operand == 'or':
                        expression = expression or result
                    elif operand == 'and not':
                        expression = expression and not result
                    elif operand == 'or not':
                        expression = expression or not result
                    else:
                        expression = False
                # if all rules fits
                if expression:
                    return get_chain_by_pattern(sentence[index][1], result_pattern)
