from enum import Enum

buildFolderPath = 'Build/'
sourceFilePath = 'D:/Python projects/casio basic compiler/test.basic'

#sourceFilePath = input("Absolute source file path: ")

class Token:
  class Type(Enum):
    STRING = 0,
    NUMBER = 1,
    FUNCTION = 2,
    

  def __init__(self, type : Type, content):
    self.type = type
    self.content = content
    
loneTokens = [
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

doubleLoneTokens = [
  '<=',
  '>=',
  '==',
  '!=',
  '&&',
  '||'
]

doubledLoneTokens = [
  '=',
  '<',
  '>',
  '|',
  '!',
  '&'
]

def parseFileToTokens(filePath):
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
        currentToken += char
        continue

      if lastCharSpace:
        appendCurrentToken()
        lastCharSpace = False

      if char in loneTokens:
        appendCurrentToken()
        tokens.append(char)
        continue

      if char == currentDoubledToken:
        appendCurrentToken()
        tokens.append(char*2)
        currentDoubledToken = ''
        continue

      if char in doubledLoneTokens:
        currentToken = char
        continue

      currentToken += char
  
  appendCurrentToken()

  return tokens

tokens = parseFileToTokens(sourceFilePath)
print(tokens)
      
    
