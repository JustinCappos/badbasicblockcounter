# This python program takes a list of AST dumps (with line numbers) and
# prints out whenever a Basic Block starts and/or ends.  The output is
# a set of lines like this:
# N 1   # not a basic block.  Definitions.
# B 3   # basic block that starts on 3 and ends on 4
# B 4   # basic blocks can start / end on the same line
# B 4   # basic block starts then ends the next line
# B 5   # another BB
# N 7   # Not a basic block.  Likely a function ended...
#
# This might correspond to this test code (w/ line numbers for reference...):
# 1:// Test AST program
# 2:int foo=3, bar=2;
# 3:int main(void) {
# 4:  if (foo) if (bar) {
# 5:  return foo-bar;}
# 6:  return bar;
# 7:}
# 8:
# 9:// All things must end!



# note that the AST dump files should look like this:
# 0 TranslationUnitDecl 0xa8c6d38 <<invalid sloc>> <invalid sloc>
# 0 |-TypedefDecl 0xa8c7008 <<invalid sloc>> <invalid sloc> implicit __builtin_va_list 'char *'
# 0 | `-PointerType 0xa8c6fe0 'char *'
# 0 |   `-BuiltinType 0xa8c6d90 'char'
# 1 `-FunctionDecl 0xa8c7078 <bbtest4.c:1:1, line:12:1> line:1:5 foo 'int ()'
# 1   `-CompoundStmt 0xa8c7450 <col:11, line:12:1>
# 2     |-DeclStmt 0xa8c7238 <line:2:3, col:21>
# 2     | |-VarDecl 0xa8c7118 <col:3, col:11> col:7 used bar 'int' cinit

# for argv
import sys


# The list of nodenames that start a basicblock
bbstartnodelist = ['CompoundStmt','IfStmt','ForStmt','WhileStmt','CaseStmt','SwitchStmt','ConditionalOperator','LabelStmt', 'DefaultStmt', 'BreakStmt','GotoStmt']
# these things should always be checked for their end line nos..
bbalwaysendnodelist = ['IfStmt','ForStmt','WhileStmt','SwitchStmt','ConditionalOperator']


# Set this to true to have a lot of things like } also count as new BBs
overestimate = False


def get_new_bb_linenos(nodename, linestr):
  usefullist = []
  # I'll try something silly.  Look for ALL line statements...
  for thisbit in linestr.split():
    usefullist.append(extract_line_no(thisbit))

  # junk the 'None' items.  We would discard later anyways, but don't carry
  # them around.
  while None in usefullist:
    usefullist.remove(None)
  return usefullist
  


# get the line number from the string pointed to.  If there isn't one, return 
# None.  It should look like "line:10:3>" or "col:4" or "<line:2:4"
def extract_line_no(stringtouse):
  if not "line:" in stringtouse:
    return None

  assert(stringtouse.count(':')==2)

  return stringtouse.split(':')[1]


# count starting occurances and strip them out of the front (only)
def count_and_strip_string(chartostrip, stringtouse):
  count = 0
  while stringtouse.startswith(chartostrip):
    count += 1
    stringtouse = stringtouse[1:]
  return count, stringtouse





def main(args):
  retval = 0
  for filename in args:
  
 # bbinfo = file(filename+'.bbinfo','w')
    print filename
    # how many pipes on the prior line...
    lastpipecount = 0
    print 'N',0
    bblineset = set()
    for line in file(filename):
      actuallinenostr,purerestofline = line.split(None,1)
      
      # let's toss all of the spaces for a moment...
      restofline = purerestofline.replace(' ','')
  
      # count the starting '|' symbols
      pipecount, restofline = count_and_strip_string('|', restofline)
  
      # this is used to end the current item at this level...
      bqcount, restofline = count_and_strip_string('`', restofline)
  
      # get the part with the spaces, strip the '|' and '`' chars, then get
      # the first thing that comes next...
      nodename = purerestofline.replace('|','').replace('`',"").split()[0]
  
      if not nodename.startswith('-'):
        assert(nodename == "TranslationUnitDecl")
      else:
        dashcount,nodename = count_and_strip_string("-", nodename)
        assert(dashcount == 1)
  
  
      # I think a pipe is only removed when replaced by a bq
      assert(lastpipecount <= pipecount + bqcount)  
  
  # JAC: CHATTY OUTPUT HERE...
  #    print linenostr, pipecount, bqcount, nodename in bbstartnodelist
      # Is this a node that starts a basic block?
      if nodename in bbstartnodelist:
        # um, then this should be added to the list to print?
        # if we want to do this for all, or if this is something like a while
        # loop or if statement that a basic block always starts after...
#        if overestimate or nodename in bbalwaysendnodelist:
        if overestimate or nodename in bbalwaysendnodelist:
          newlines = get_new_bb_linenos(nodename,purerestofline)
          newlinesplusone = []
          for linenostr in newlines:
            newlinesplusone.append(str(int(linenostr)+1))
          bbnewlist = [actuallinenostr] + newlinesplusone
        else:
          bbnewlist = [actuallinenostr]
#        print 'DEBUG',nodename, actuallinenostr, bbnewlist
        
        # I could do this above, but do it here to make debug output easier.
        for thislineno in bbnewlist:
          bblineset.add(thislineno)
  
      # update this for assert purposes...
      lastpipecount = pipecount
  
    mylist = []
    for linenostr in bblineset:
      mylist.append(int(linenostr))
  
    mylist.sort()
   
    lastlineno = int(actuallinenostr)
    # print these out.  Due to them being strings, they will not be correctly
    # sorted.
    for lineno in mylist:
      if lineno <= lastlineno:
        print 'B',lineno

      
#      This will be true for code like arch_alpha_boot_main.c where the 
#      strcpy call is treated like an implicit definition.  This will result
#      in the parser getting this AST node last (after the containing function
#      definition.
#      if (lastlineno + 1 < lineno):
#        print >> sys.stderr, "ERROR linenobigger",lastlineno, lineno
#        retval = 1
  
    # end the file...
    print 'N',actuallinenostr
      
  sys.exit(retval)


if __name__ == '__main__':
  main(sys.argv[1:])
