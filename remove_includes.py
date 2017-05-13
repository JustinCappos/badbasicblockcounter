# this prepends lines that contain #include with //
import sys

if len(sys.argv) == 1:
  print "Must call this program with the .c and .h files to replace the "
  print "#includes of .c and .h files.  May pass multiple files at once."
  print "Output is for foo.c is written to foo.c.new"
  sys.exit(1)


for fn in sys.argv[1:]:
  outfo = open(fn+'.noincl','w')
  for line in open(fn):
    
    # see the README for information about why I think this is adequate
    filteredline = line.replace(' ','').replace('\t','')
    if filteredline.startswith('#include'): 
      line = '// JNOI ' + line
  
    outfo.write(line)
  outfo.close()
    

