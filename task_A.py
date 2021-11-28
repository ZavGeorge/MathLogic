def skip_while_symbol(line, symbol , index):
    if line.startswith(symbol, index):
        index += len(symbol)
        return True, index
    else:
        return False, index

def implication(line, new_line, index):
    line, new_line, index = disjunction(line, new_line, index)
    TF, index = skip_while_symbol(line, '->', index)
    if TF:
        line, impl, index = implication(line, new_line, index)
        new_line = '(->' + new_line + ',' + impl + ')'
    return line, new_line, index

def disjunction(line, new_line, index):
    line, new_line, index = conjunction(line, new_line, index)
    TF, index = skip_while_symbol(line, '|', index)
    while TF:
        line, con, index = conjunction(line, new_line, index)
        new_line = '(|,' + new_line + ',' + con + ')'
        TF, index = skip_while_symbol(line, '|', index)
    return line, new_line, index

def conjunction(line, new_line, index):
    line, new_line, index = negative(line, new_line, index)
    TF, index = skip_while_symbol(line, '&', index)
    while TF:
        line, neg, index = negative(line, new_line, index)
        new_line = '(&,' + new_line + ',' + neg + ')'
        TF, index = skip_while_symbol(line, '&', index)  
    return line, new_line, index   

def negative(line, new_line, index):
    TF, index = skip_while_symbol(line, '(', index)
    if TF:
        line, impl, index = implication(line, new_line, index)
        TF = skip_while_symbol(line, ')', index)
        return  line, impl, index
    TF, index = skip_while_symbol(line, '!', index)
    if TF:
        line, neg, index = negative(line, new_line, index)
        new_line = '(!' + neg + ')'
        return line, new_line, index
    new_line = ''
    while (line[index].isdigit() or line[index].isalpha() or line[index] == '\'') and index != len(line)-1:
        new_line += line[index]
        index +=1
    return line, new_line, index

def parser(line):
    line = line + '#'
    new_line = '' 
    index = 0
    line, new_line, index = implication(line, new_line, index)
    return new_line

line = input()
line.replace(' ', '')
line.replace('\t', '')

print(parser(line))
