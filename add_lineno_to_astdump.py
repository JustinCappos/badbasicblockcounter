# This python program takes a list of AST files and adds the line number
# to the beginning of every line.  This makes later processing easier.
# The file will be called origname.withlineno

# The list of strings for which I should toss the rest of the line...
tosslastlist = ['CompoundStmt','IfStmt','ForStmt','WhileStmt','CaseStmt','SwitchStmt','BinaryOperator','ConditionalOperator','LabelStmt']


import sys

for filename in sys.argv[1:]:
  thislineno = 0
  outfo = file(filename+'.withlineno','w')
  for line in file(filename):
    # check if the string 'line:' is in and update thislineno if it is...
    # in rare cases StringLiteral will contain "line:"
    # in rare cases VerbatimBlockLineComment will too!
    if 'line:' in line and 'StringLiteral' not in line and 'Comment' not in line:
      thisline = line

      for thistosser in tosslastlist:
        if thistosser in line:
          # example: CompoundStmt 0xabc92e8 <line:6:8, line:8:3>
          # example: IfStmt 0xabc9300 <line:3:3, line:8:3>
          # example: ForStmt 0x978a370 <line:3:3, line:5:3>
          # example: WhileStmt 0xa1a0370 <line:4:3, line:8:3>
          # example: CaseStmt 0xa64a2e8 <line:5:5, line:7:8>
          # example: SwitchStmt 0xa64a2b8 <line:4:3, line:14:3>
          # example: BinaryOperator 0xa5673c0 <line:5:3, line:9:7> 'int' '='
          # example: ConditionalOperator 0xa5673a0 <col:5, line:9:7> 'int'
          # example: LabelStmt 0xb6964b8 <line:11:1, line:13:4> 'labelthis'
          # I want to toss the last line entry. it is just where this block ends
          thisline= line.split(',')[0]

      if 'FunctionDecl' in line:
        # example: FunctionDecl 0xabc9078 <bbtest1.c:1:1, line:10:1> line:1:5 foo 'int ()'
        # I want to toss the middle line entry. it is just where this block ends
        # the other two are useful though.
        thisline= line.split(',')[0] +" "+ line.split('>')[1]

      # split, but toss the first because the line doesn't start with "line:"
      linepieces = thisline.split('line:')[1:]

      for piece in linepieces:
        # this looks like it's always 'line:x:y' so I can stop at the next ':'
        newlineno = int(piece.split(':')[0])
        if newlineno < thislineno:
          print "lineno:",newlineno,"is less than",thislineno,'on',line
        thislineno = newlineno

#      print thislineno, line,
        
    outfo.write(str(thislineno)+" "+line)
  outfo.close()

