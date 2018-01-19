from pymongo import MongoClient
import json
import sys

def main():
   json_file = sys.argv[1]
   print ("json path:" + json_file)

   instance = sys.argv[2]
   print ("instance:" + instance)

   print ("print debug raw:" + sys.argv[3])
   if sys.argv[3] == "false":
     _print_debug_info = False
   else:
     _print_debug_info = True
   print ("print debug:" + str(_print_debug_info))

   if _print_debug_info:
      print ("will print debug information")
   else:
      print ("will NOT print debug information")

main()
