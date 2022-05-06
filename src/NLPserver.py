import os
from nltk.parse.corenlp import CoreNLPServer
from nltk.parse.corenlp import CoreNLPParser


class parser:
   def __init__(self):
      # Stanford NLP Server
      stanford_core = "stanford-corenlp-4.4.0"

      self.server = CoreNLPServer(
         os.path.join(stanford_core, "stanford-corenlp-4.4.0.jar"),
         os.path.join(stanford_core, "stanford-corenlp-4.4.0-models.jar"),    
      )

      self.running = False


   def start(self):
      if self.running:
         print("Server already running")
         return False
      else:
         print("Starting Stanford NLP Server")
         self.server.start()
         self.parser = CoreNLPParser()
         self.running = True
         #print("Server started")
         return True


   def stop(self):
      if self.running:
         # Stop the Stanford NLP Server
         print("Stopping server")
         self.server.stop()
         self.running = False
         return True
      else:
         print("Server is not running")
         return False

   # The parser - will start the server but will not stop
   def parse(self, text):
      if not self.running:
         self.start()
      
      tree = next(self.parser.raw_parse(text))
      return tree

   # cleanup
   def __del__(self):
      if self.running:
         self.stop()
