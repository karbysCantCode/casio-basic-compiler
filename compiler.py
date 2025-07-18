from __future__ import annotations
from enum import Enum
import copy
from typing import Optional


buildFolderPath = 'Build/'
sourceFilePath = 'D:/Python projects/casio basic compiler/test.basic'

#sourceFilePath = input("Absolute source file path: ")

class Compiler:
  SCOPEOWNINGKEYWORDS = [
    'if',
    'else',
    'elseif',
    'while',
    'for'
  ]
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
    '%=',
    '--',
    '++'
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
    '%=',
    '--',
    '++'
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
  
  class Scope:
    def __init__(self, startLine = -1, parentScope : Optional[Compiler.Scope] = None):
      self.tokens = []
      self.parentScope = parentScope
      self.tokensOwningChildrenScopes = {} # token : indexInSelf.Tokens
      self.startLine = startLine
      #self.localIdentifiers = []

    def addToken(self, token : Compiler.Token):
      if token.type == Compiler.Token.Type.DELIMITER and token.content == '{':
        self.tokensOwningChildrenScopes[token] = len(self.tokens)
      self.tokens.append(token)

    def print(self):
      print("Scope print:")
      targetString = ''
      scopesToPrint = []
      for token in self.tokens:
        targetString += token.content
        if token in self.tokensOwningChildrenScopes:
          scopesToPrint.append(token.ownedScope)
      print(targetString)

      for scope in scopesToPrint:
        scope.print()


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
      self.ownedScope: Optional[Compiler.Scope] = None

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

    scope, unclosedScope = self._buildScopes(secondTaggedTokenArray)
    if unclosedScope:
      print(f"UNCLOSED SCOPE - CAUSE MAY BEGIN ON LINE: {unclosedScope.startLine}")

    scope.print()

  @staticmethod
  def _isNumber(number : str) -> bool:
      try:
        float(number)
        return True
      except:
        return False

  def _buildScopes(self, tokenArray : list) -> tuple:
    globalScope = self.Scope()
    scopeStack = [globalScope]
    
    for token in tokenArray:

      if token.type == self.Token.Type.DELIMITER:
        if token.content == '{':
          scopeStack[-1].addToken(token)
          scopeStack.append(self.Scope(token.lineNumber,scopeStack[-1]))
          token.ownedScope = scopeStack[-1]
        elif token.content == '}':
          scopeStack.pop()
          scopeStack[-1].addToken(token)
          continue
        else:
          scopeStack[-1].addToken(token)
      else:
        scopeStack[-1].addToken(token)
    
    if len(scopeStack) > 1:
      print("SCOPE NOT CLOSED")
      return (globalScope,scopeStack[-1])
    
    return (globalScope,None)

  def _tagTokens(self, tokenArray : list) -> list:
    def tagToken(token : Compiler.Token) -> list:
      nonlocal tokensLeftToSkip
      indexesToSkip = []
      if (token.type == self.Token.Type.UNSOLVED or token.type == self.Token.Type.NUMBER) and tokenIndex + 2 < len(localTokenArray):
        if ((self._isNumber(token.content)
            or token.type == self.Token.Type.NUMBER)
            and not (tokenIndex - 2 < 0)):
          
          token.type = self.Token.Type.NUMBER
          
          if (self._isNumber(localTokenArray[tokenIndex+2].content) #if need to collapse next 2 for decimal
              and localTokenArray[tokenIndex+1].content == '.'):
            token.content += '.' + localTokenArray[tokenIndex+2].content
            indexesToSkip.append(tokenIndex+1)
            indexesToSkip.append(tokenIndex+2)

          if (localTokenArray[tokenIndex-2].type == self.Token.Type.ASSIGNMENT
              and localTokenArray[tokenIndex-1].content == '-'):
            token.content = '-' + token.content
            indexesToSkip.append(tokenIndex-1)

          

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

        elif not (tokenIndex-1 < 0):
          nextTokenType = localTokenArray[tokenIndex+1].type
          lastTokenType = localTokenArray[tokenIndex-1].type
          if (nextTokenType == self.Token.Type.ASSIGNMENT 
              or nextTokenType == self.Token.Type.DELIMITER 
              or nextTokenType == self.Token.Type.COMPARISON
              or nextTokenType == self.Token.Type.OPERATOR
              or lastTokenType == self.Token.Type.ASSIGNMENT 
              or lastTokenType == self.Token.Type.DELIMITER 
              or lastTokenType == self.Token.Type.COMPARISON
              or lastTokenType == self.Token.Type.OPERATOR): #eg identifier = 10 - solving identifier
            token.type = self.Token.Type.IDENTIFIER

      return [token, indexesToSkip]
    
    localTokenArray = tokenArray
    taggedArray = []
    tokenIndexesToSkip = set()

    tokensLeftToSkip = 0
    for tokenIndex, token in enumerate(localTokenArray):
      if tokensLeftToSkip > 0:
        tokensLeftToSkip -= 1
        continue

      token, tokensToSkip = tagToken(token)
      tokenIndexesToSkip.update(tokensToSkip)
            
      taggedArray.append(self.Token(token.content, token.type, token.lineNumber))

    finalArray = []
    for tokenIndex, token in enumerate(localTokenArray):
      if tokenIndex in tokenIndexesToSkip:
        continue

      finalArray.append(token)

    return finalArray

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
            localTokenFragement = currentTokenFragment
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
            else:
              currentTokenFragment = localTokenFragement
              appendToken()
              currentTokenFragment = character
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
        if charIndex + 1 < len(line) and character == '/' and line[charIndex + 1] == '/' and not currentTokenIsString:
          currentTokenFragment = ''
          print(f'comment on line: {currentLineNumber}')
          break  # Skip rest of line
        
        if charIndex+1 < len(line):
          checkCharacter(character, line[charIndex+1])
        else:
          checkCharacter(character, '')
    
    appendToken()

    return tokenArray









compiler = Compiler()
compiler.setSourceFilePath(sourceFilePath)
compiler.compileSourceFile()
