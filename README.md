# badbasicblockcounter

This is a basic program that is meant to get basic block information from 
C code.  Specifically, it is intended to run on very large codebases (such as
the Linux kernel).  

This code has been done very poorly / quickly and is not meant to be used or
relied on for any purpose.  User beware!!!

## Some random notes:

I tend to use the scripts like this:
First copy all of the .c and .h files over.  For example:
for file in `find . -name \*.c`;  do cp $file ../ast-files/`echo $file | tr '/' '_'`; done
for file in `find . -name \*.h`;  do cp $file ../ast-files/`echo $file | tr '/' '_'`; done

Then rename them to remove the leading ._

I manually looked at all lines with #include that do not start with it to see 
if I need to be careful when replacing text.  I concluded I could just take 
any line that starts with #include and prepend // .  Since this string doesn't
appear in the kernel source, a python script remove_includes.py was written
that prepends "// JNOI ".  

After this, run output_bbs_for_c_file.py *.[ch] and you are done!
