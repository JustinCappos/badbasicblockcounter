# This python program takes a list of c files and generates all of the 
# intermediate things needed for the bb file to be generated.


# for argv
import sys
import os

try:
  scriptdir = os.path.dirname(sys.argv[0])

  for filename in sys.argv[1:]:
    print 'processing:',filename
    assert(filename.endswith('.c') or filename.endswith('.h'))
  
    if os.path.exists(filename+'.bb'):
      continue

    # run clang should redirect output (I hope)
    os.system('clang -cc1 -ast-dump '+filename+' > '+filename+'.dump')
  
    assert(os.system('python '+scriptdir+'/add_lineno_to_astdump.py '+filename+'.dump') == 0)
  
    assert(os.system('python '+scriptdir+'/get_basic_blocks_from_astdump.py '+filename+'.dump.withlineno > '+filename+'.bb') == 0)
    # remove the big files...
    os.system('rm '+filename+'.dump '+filename+'.dump.withlineno')
  
except AssertionError:
  print 'Error with:'+filename
  raise
  
    
