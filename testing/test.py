import pystoch
import pystoch.compile as c
import os

testfiles = [os.path.join("tests", test) for test in os.listdir("tests") \
             if test.endswith(".py") and test.startswith("compile_")]
resultfiles = [os.path.join("tests", test) for test in os.listdir("tests") \
               if test.endswith(".pystoch") and test.startswith("compile_")]

tests = {}
for testfile in testfiles:
    front = len("compile_")
    back = len(".py")
    name = os.path.basename(testfile)[front:-back]
    tests[name] = open(testfile, "r").read()

results = {}
for resultfile in resultfiles:
    front = len("compile_")
    back = len(".pystoch")
    name = os.path.basename(resultfile)[front:-back]
    results[name] = open(resultfile, "r").read()

teststorun = list(set(tests.keys()).intersection(set(results.keys())))
print "Tests: %s" % ", ".join(teststorun)
print

passed = []
failed = []
for totest in teststorun:
    print "Running '%s' test..." % totest

    test = tests[totest]
    result = c.pystoch_compile(tests[totest])
    exresult = results[totest]

    def indent(src):
        return "\n".join(["\t" + line for line in src.split("\n")])
        
    print "-----------------------------------------------"
    print "TEST"
    print indent(test)
    print "RESULT"
    print indent(result)
    print "EXPECTED RESULT"
    print indent(exresult)
        
    if result != exresult:
        failed.append(totest)
    else:
        passed.append(totest)

print "-----------------------------------------------"
print
print "Tests passed: %s/%s" % (len(passed), len(teststorun))
print "Tests failed: %s/%s" % (len(failed), len(teststorun))
print
print "Failed tests: %s" % ", ".join(failed)
