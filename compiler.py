from enum import Enum


buildFolderPath = 'Build/'
sourceFilePath = 'D:/Python projects/casio basic compiler/test.basic'

#sourceFilePath = input("Absolute source file path: ")

class Compiler:
  DELIMITERTOKENS = [
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    ';',
    ',',
    '.'
  ]
  ASSIGNMENTTOKENS = [
    '=',
    '+=',
    '-=',
    '*=',
    '/=',
    '%='
  ]
  OPERATORTOKENS = [
    '+',
    '-',
    '*',
    '/',
    '%',
    '||',
    '&&',
    '!'
  ]
  COMPARISONTOKENS = [
    '&',
    '|',
    '<=',
    '>=',
    '==',
    '!=',
    '<',
    '>'
  ]
  LONETOKENS = [
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    ';',
    ',',
    '.'
  ]
  DOUBLELONETOKENS = [
    '<=',
    '>=',
    '==',
    '!=',
    '&&',
    '||'
  ]
  DOUBLEDLONETOKENS = [
    '=',
    '<',
    '>',
    '|',
    '!',
    '&'
  ]
  ESCAPECHARACTERLOOKUP = {
    '\\\'' : '\'',
    '\\\"' : '\"',
    '\\?' : '?',
    '\\\\' : '\\',
    '\\a' : '\a',
    '\\b' : '\b',
    '\\f' : '\f',
    '\\n' : '\n',
    '\\r' : '\r',
    '\\t' : '\t',
    '\\v' : '\v'

  }
 
  class Token:
    class Type(Enum):
      UNSOLVED = 0
      NUMBER = 1
      STRING = 2
      IDENTIFIER = 3
      ASSIGNMENTOPERATOR = 4
      COMPARISONOPERATOR = 5
      DELIMITER = 6



    def __init__(self, content : str, type : Type):
      self.content = content
      self.type = type

  def __init__(self):
    print("compiler init")
    self.sourceFilePath = ''

  def setSourceFilePath(self, sourceFilePath : str):
    self.sourceFilePath = sourceFilePath

  def compileSourceFile(self):
    rawTokenArray = self._ParseFileToRawTokens(self.sourceFilePath)
    taggedTokenArray = self._tagTokens(rawTokenArray)

  def _tagTokens(self, rawTokenArray : list) -> list:
    taggedArray = []
    for rawToken in rawTokenArray:

    return

  def _ParseFileToRawTokens(self, filePath) -> list:
    sourceFileLines = []

    try:
      with open(filePath, 'r') as file:
        sourceFileLines = file.readlines()

    except:
      print("Failed to read source file")

    currentTokenIsString = False
    for line in sourceFileLines:
      for character in line:



























    lastCharSpace = False
    currentTokenIsString = False
    backslashing = False

    tokens = []
    currentTokenFragment = ''
    currentDoubledToken = ''
    currentBackslashToken = ''

    def appendCurrentToken(tokenType = self.Token.Type.UNSOLVED):
      nonlocal currentTokenFragment
      if currentTokenFragment != '':
            tokens.append(self.Token(currentTokenFragment, tokenType))
            currentTokenFragment = ''

    for line in sourceFileLines: 
      for char in line:
        if (char == ' ' or char == '\n') and not currentTokenIsString:
          lastCharSpace = True
          continue     

        if char == "'" or char == '"':
          if currentTokenIsString:
            appendCurrentToken(self.Token.Type.STRING)
          else:
            appendCurrentToken()
          currentTokenIsString = not currentTokenIsString
          continue
        
        if currentTokenIsString:
          if char == '\\' and not backslashing: #if backslash
            backslashing = True
            currentBackslashToken = '\\'
            continue

          if backslashing:
            backslashing = False
            currentBackslashToken += char
            currentTokenFragment += self.ESCAPECHARACTERLOOKUP[currentBackslashToken] #add the actual char of the backslash to the current token
            currentBackslashToken = ''
            continue
          

          currentTokenFragment += char
          continue

        if lastCharSpace:
          appendCurrentToken()
          lastCharSpace = False

        if char in self.LONETOKENS:
          appendCurrentToken()
          tokens.append(char)
          continue

        if char in self.DOUBLEDLONETOKENS:
          if currentDoubledToken != '': #second of a potential double token
            temp = currentDoubledToken + char
            if temp in self.DOUBLELONETOKENS: #should be true every time
              tokens.append(temp)
            
            currentDoubledToken = ''
            currentToken = ''

          else: #first of a potential double token
            appendCurrentToken()
            currentDoubledToken = char
            currentToken = char
          
          continue

        elif currentDoubledToken != '': #non double token and last was a doubled token
          appendCurrentToken()
          currentDoubledToken = ''
        

        currentTokenFragment += char
    
    appendCurrentToken()

    return tokens


compiler = Compiler()
compiler.setSourceFilePath(sourceFilePath)
compiler.compileSourceFile()
