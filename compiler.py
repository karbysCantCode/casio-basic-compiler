from enum import Enum
import copy


buildFolderPath = 'Build/'
sourceFilePath = 'D:/Python projects/casio basic compiler/test.basic'

#sourceFilePath = input("Absolute source file path: ")

class Compiler:
  KEYWORDTOKENS = [
    'if',
    'else',
    'elseif',
    'while',
    'continue',
    'break',
    'return',
    'for'

  ]
  TYPETOKENS = [
    'int',
    'float',
    'char',
    'string',
    'intA',
    'floatA',
    'void',
    'bool'
  ]
  KEYWORDLITERALTOKENS = [
    'true',
    'false'
  ]
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
    '||',
    '+=',
    '-=',
    '*=',
    '/=',
    '%='
  ]
  DOUBLEDLONETOKENS = [
    '=',
    '<',
    '>',
    '|',
    '!',
    '&',
    '+',
    '-',
    '*',
    '/',
    '%'
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
      ASSIGNMENT = 4
      COMPARISON = 5
      OPERATOR = 6
      DELIMITER = 7
      KEYWORD = 8
      LITERALKEYWORD = 9
      TYPEKEYWORD = 10



    def __init__(self, content : str, type : Type, lineNumber : int):
      self.content = content
      self.type = type
      self.lineNumber = lineNumber

    def __str__(self):
      return f'TYPE: {self.type.name}\nLINE: {self.lineNumber}\nCONTENT: "{self.content}"\n'

  def __init__(self):
    print("compiler init")
    self.sourceFilePath = ''

  def setSourceFilePath(self, sourceFilePath : str):
    self.sourceFilePath = sourceFilePath

  def compileSourceFile(self):
    firstPassTokenArray = self._ParseFileToRawTokens(self.sourceFilePath)
    taggedTokenArray = self._tagTokens(firstPassTokenArray)
    secondTaggedTokenArray = self._tagTokens(taggedTokenArray)
    unsolvedTokens = []
    for token in secondTaggedTokenArray:
      if token.type == self.Token.Type.UNSOLVED:
        unsolvedTokens.append(token)

    print(f'\nUnsolved tokens: {len(unsolvedTokens)}')
    for token in unsolvedTokens:
      print(token)

    target = ''
    for token in secondTaggedTokenArray:
      target += token.content
    print(target)

  @staticmethod
  def _isNumber(number : str) -> bool:
      try:
        float(number)
        return True
      except:
        return False
      
  def _tagTokens(self, tokenArray : list) -> list:
    def tagToken(token : Compiler.Token) -> Compiler.Token:
      nonlocal tokensLeftToSkip
      if (token.type == self.Token.Type.UNSOLVED or token.type == self.Token.Type.NUMBER) and tokenIndex != len(localTokenArray)-1:
        if self._isNumber(token.content) or token.type == self.Token.Type.NUMBER and tokenIndex + 2 < len(localTokenArray):
          if (localTokenArray[tokenIndex+1].content == '.' 
              and localTokenArray[tokenIndex+2].content.isdecimal()): # eg 3.13 (. is delim and 13 would be unsolved)
            token.content += '.' + localTokenArray[tokenIndex+2].content
            tokensLeftToSkip = 2
          token.type = self.Token.Type.NUMBER

        elif token.content in self.KEYWORDLITERALTOKENS:
          token.type = self.Token.Type.LITERALKEYWORD

        elif token.content in self.KEYWORDTOKENS:
          token.type = self.Token.Type.KEYWORD

        elif token.content in self.TYPETOKENS:
          token.type = self.Token.Type.TYPEKEYWORD

        elif token.content in self.ASSIGNMENTTOKENS:
          token.type = self.Token.Type.ASSIGNMENT
        
        elif token.content in self.COMPARISONTOKENS:
          token.type = self.Token.Type.COMPARISON
        
        elif token.content in self.OPERATORTOKENS:
          token.type = self.Token.Type.OPERATOR

        elif (localTokenArray[tokenIndex+1].type == self.Token.Type.ASSIGNMENT 
              or localTokenArray[tokenIndex+1].type == self.Token.Type.DELIMITER 
              or localTokenArray[tokenIndex+1].type == self.Token.Type.COMPARISON): #eg identifier = 10 - solving identifier
          token.type = self.Token.Type.IDENTIFIER

      return token
    
    localTokenArray = tokenArray
    taggedArray = []

    tokensLeftToSkip = 0
    for tokenIndex, token in enumerate(localTokenArray):
      if tokensLeftToSkip > 0:
        tokensLeftToSkip -= 1
        continue

      token = tagToken(token)
            
      taggedArray.append(self.Token(token.content, token.type, token.lineNumber))

    return taggedArray

  def _ParseFileToRawTokens(self, filePath) -> list:
    sourceFileLines = []

    try:
      with open(filePath, 'r') as file:
        sourceFileLines = file.readlines()

    except:
      print("Failed to read source file")

    tokenArray = []
    currentTokenFragment = ''
    backslashBuffer = ''
    stringOpeningCharacter = ''
    currentTokenIsString = False
    lastCharacterWasSpace = False
    lastCharacterWasBackslash = False
    lastCharacterWasDouble = False

    currentLineNumber = -1


    def appendToken(tokenType = self.Token.Type.UNSOLVED):
      nonlocal currentTokenFragment
      if currentTokenFragment != '':
        tokenArray.append(self.Token(currentTokenFragment, tokenType, currentLineNumber))
        currentTokenFragment = ''

    def checkCharacter(character, nextCharacter):
      nonlocal currentTokenFragment
      nonlocal currentTokenIsString
      nonlocal lastCharacterWasDouble
      nonlocal lastCharacterWasBackslash
      nonlocal backslashBuffer
      nonlocal lastCharacterWasSpace
      nonlocal stringOpeningCharacter
      
      localLastCharWasSpace = lastCharacterWasSpace

      if not currentTokenIsString:

        if (character == ' ' or character == '\n'): #if char is space and not in a string
          lastCharacterWasSpace = True
          return
        else:
          lastCharacterWasSpace = False

        if character not in self.DOUBLEDLONETOKENS and lastCharacterWasDouble: #if last was a double char, but not a double, append that double
          if currentTokenFragment in self.OPERATORTOKENS:
            appendToken(self.Token.Type.OPERATOR)
          elif currentTokenFragment in self.COMPARISONTOKENS:
            appendToken(self.Token.Type.COMPARISON)
          elif currentTokenFragment in self.ASSIGNMENTTOKENS:
            appendToken(self.Token.Type.ASSIGNMENT)
          else:
            appendToken()

          lastCharacterWasDouble = False

        if character == '-' and self._isNumber(nextCharacter):
          appendToken()
          currentTokenFragment += character
          return

        if character in self.DOUBLEDLONETOKENS:
          if lastCharacterWasDouble:
            lastCharacterWasDouble = False
            currentTokenFragment += character
            if currentTokenFragment in self.DOUBLELONETOKENS:
              if currentTokenFragment in self.OPERATORTOKENS:
                appendToken(self.Token.Type.OPERATOR)
              elif currentTokenFragment in self.COMPARISONTOKENS:
                appendToken(self.Token.Type.COMPARISON)
              elif currentTokenFragment in self.ASSIGNMENTTOKENS:
                appendToken(self.Token.Type.ASSIGNMENT)
              else:
                appendToken()
              return
          else:
            appendToken()
            lastCharacterWasDouble = True
            currentTokenFragment = character
            return

        if character in self.DELIMITERTOKENS:
          appendToken()
          currentTokenFragment += character
          appendToken(self.Token.Type.DELIMITER)
          return
        
        if character in self.ASSIGNMENTTOKENS:
          appendToken()
          currentTokenFragment += character
          appendToken(self.Token.Type.ASSIGNMENT)
          return

        if character in self.OPERATORTOKENS:
          appendToken()
          currentTokenFragment += character
          appendToken(self.Token.Type.OPERATOR)
          return

        if character in self.COMPARISONTOKENS:
          appendToken()
          currentTokenFragment += character
          appendToken(self.Token.Type.COMPARISON)
          return

      if character == '\\' and not lastCharacterWasBackslash:
        lastCharacterWasBackslash = True
        backslashBuffer = '\\'
        return
      
      if lastCharacterWasBackslash:
        lastCharacterWasBackslash = False
        backslashBuffer += character
        currentTokenFragment += self.ESCAPECHARACTERLOOKUP[backslashBuffer]
        return
      
      if (character == "'" or character == '"') and (not currentTokenIsString or character == stringOpeningCharacter):
        if currentTokenIsString:
          currentTokenIsString = False
          stringOpeningCharacter = ''
          appendToken(self.Token.Type.STRING)
        else:
          currentTokenIsString = True
          stringOpeningCharacter = character
          #currentTokenFragment += character #dont add the apostrophes to the string?
        return
      
      if localLastCharWasSpace:
        appendToken()
      currentTokenFragment += character

      # if currentTokenIsString: # if string, dont proceed
      #   return
      # if len(tokenArray) == 0:
      #   return
      
      # if (lastCharacterWasSpace 
      #     or tokenArray[-1].type == self.Token.Type.DELIMITER 
      #     or tokenArray[-1].type == self.Token.Type.ASSIGNMENT
      #     or tokenArray[-1].type == self.Token.Type.COMPARISON 
      #     or tokenArray[-1].type == self.Token.Type.OPERATOR): # if at token boundary
      #   if currentTokenFragment in self.KEYWORDTOKENS:
      #     appendToken(self.Token.Type.KEYWORD)
      #   elif currentTokenFragment in self.KEYWORDLITERALTOKENS:
      #     appendToken(self.Token.Type.LITERALKEYWORD)
      #   elif currentTokenFragment in self.TYPETOKENS:
      #     appendToken(self.Token.Type.TYPEKEYWORD)

      




    for lineNumber, line in enumerate(sourceFileLines):
      currentLineNumber = lineNumber+1 # so it can be refrenced by appendToken()
      for charIndex, character in enumerate(line):
        if character == '/' and currentTokenFragment == '/' and not currentTokenIsString:
          currentTokenFragment = ''
          print(f'comment on line: {currentLineNumber}')
          break
        
        if charIndex+1 < len(line):
          checkCharacter(character, line[charIndex+1])
        else:
          checkCharacter(character, '')
    
    appendToken()

    return tokenArray









compiler = Compiler()
compiler.setSourceFilePath(sourceFilePath)
compiler.compileSourceFile()
