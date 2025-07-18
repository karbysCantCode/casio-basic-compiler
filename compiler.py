from enum import Enum


buildFolderPath = 'Build/'
sourceFilePath = 'D:/Python projects/casio basic compiler/test.basic'

#sourceFilePath = input("Absolute source file path: ")

class Compiler:
  LONETOKENS = [
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    '+',
    '-',
    '*',
    '/',
    '%',
    '^',
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
    '\'' = '\''
  }
  def __init__(self):
    print("compiler init")
    self.sourceFilePath = ''

  def setSourceFilePath(self, sourceFilePath : str):
    self.sourceFilePath = sourceFilePath

  def compileSourceFile(self):
    rawTokens = self._ParseFileToRawTokens(self.sourceFilePath)

  def _ParseFileToRawTokens(self, filePath):
    sourceFileLines = []

    try:
      with open(filePath, 'r') as file:
        sourceFileLines = file.readlines()

    except:
      print("Failed to read source file")

    lastCharSpace = False
    currentTokenIsString = False
    backslashing = False

    tokens = []
    currentToken = ''
    currentDoubledToken = ''

    def appendCurrentToken():
        sourceFileLines = []

    try:
      with open(filePath, 'r') as file:
        sourceFileLines = file.readlines()

    except:
      print("Failed to read source file")

    lastCharSpace = False
    currentTokenIsString = False
    backslashing = False

    tokens = []
    currentToken = ''
    currentDoubledToken = ''
    currentBackslashToken = ''

    def appendCurrentToken():
      nonlocal currentToken
      if currentToken != '':
            tokens.append(currentToken)
            currentToken = ''

    for line in sourceFileLines: 
      for char in line:
        if (char == ' ' or char == '\n') and not currentTokenIsString:
          lastCharSpace = True
          continue     

        if char == "'" or char == '"':
          appendCurrentToken()
          currentTokenIsString = not currentTokenIsString
          continue
        
        if currentTokenIsString:
          if backslashing:
            backslashing = False
            currentBackslashToken += char
            currentToken += #add the actual char of the backslash to the current token
          

          currentToken += char
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
        

        currentToken += char
    
    appendCurrentToken()

    return tokens



