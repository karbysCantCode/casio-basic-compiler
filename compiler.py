from __future__ import annotations
from enum import Enum, auto
from typing import Any, Union, Optional
from pathlib import Path


class Compiler:

  class Token:
    class Type(Enum):
      LITERAL = auto()
      IDENTIFIER = auto()
      COMPARISON = auto()
      OPERATOR = auto()
      ASSIGMENT = auto()
      TYPEKEYWORD = auto()
      MODIFIER = auto()
      PRIMITIVELITERAL = auto()
      KEYWORD = auto()
      TYPEDECLKEYWORD = auto()
      DELIMITER = auto()

    class SpecificType(Enum):
      NONE = auto()
      STRINGLITERAL = auto()
      CHARLITERAL = auto()
      COMPOUNDASSIGNMENT = auto()
      EQUALS = auto()
      DECIMALNUMBER = auto()
      NUMBER = auto()
      SEMICOLON = auto()
      UNSUREIDENTIFIER = auto()
      IDENTIFIER = auto()
      LCURLYBRACE = auto()
      RCURLYBRACE = auto()



    def __init__(self, type : Compiler.Token.Type, content : Any, line : int, char : int, specificType : Compiler.Token.SpecificType = SpecificType.NONE):
      self.type : Compiler.Token.Type = type
      self.content : Any = content
      self.line : int = line
      self.char : int = char
      self.specificType : Compiler.Token.SpecificType = specificType

    def __repr__(self) -> str:
      return f"""
         Type: {self.type.name}
         Line: {self.line}
         Char: {self.char}
      Content: {self.content}
      """

  class Log:
    class Severity(Enum):
      NOTICE = auto()
      WARNING = auto()
      DEBUG = auto()
      ERROR = auto()
      CRITICAL = auto()
      FATAL = auto()

    def __init__(self, message : str, severity : Severity, author : str = 'none'):
      self.message : str = message
      self.author : str = author
      self.severity : Compiler.Log.Severity = severity

    def __str__(self):
      return f"""[{self.severity.name}] [{self.author}] {self.message}"""

  def __init__(self) -> None:
    self.logs : list[Compiler.Log] = []
    pass
  
  def dequeueLog(self)->Compiler.Log:
    log = self.logs[0]
    self.logs.pop(0)
    return log
  
  def logsEmpty(self)->bool:
    if len(self.logs) == 0:
      return True
    return False
  
  def getAllLogs(self)->list[Compiler.Log]:
    logs = self.logs.copy()
    return logs
  
  def dequeueAllLogs(self)->list[Compiler.Log]:
    logs = self.logs.copy()
    self.logs.clear()
    return logs
  
  def _logEvent(self, message : str, severity : Compiler.Log.Severity, author : str = 'none'):
    self.logs.append(Compiler.Log(message,severity,author))
  
  def _parseFileToString(self, filePath : Path) -> str:
    with open(filePath,'r') as file:
      return file.read()
    
  def _tokeniseString(self, string : str)->list[Compiler.Token]:
    def nextChar() -> str:
      nonlocal string
      nonlocal currentCharIndex

      if len(string) > currentCharIndex + 1:
        return string[currentCharIndex+1]
      return ''
    
    def lastChar() -> str:
      nonlocal string
      nonlocal currentCharIndex

      if currentCharIndex > 0:
        return string[currentCharIndex-1]
      return ''

    def eatNumber() -> tuple[str, int]:
      nonlocal currentCharIndex
      number = ''
      currentCharacter = string[currentCharIndex]
      isDecimal = False
      while currentCharacter.isdigit() or currentCharacter == '.':
        if currentChar == '.':
          if isDecimal:
            self._logEvent("PROBABLY UNEXPECTED . IN NUMBER.", Compiler.Log.Severity.WARNING, 'Number Builder')
          isDecimal = True
        number += currentCharacter
        currentCharIndex += 1
        currentCharacter = string[currentCharIndex]
      
      return number, isDecimal


    ESCAPESEQUENCES = {
      '\\\'' : '\'',
      '\\\"' : '\"',
      '\\\\' : '\\',
      '\\a' : '\a',
      '\\b' : '\b',
      '\\f' : '\f',
      '\\n' : '\n',
      '\\r' : '\r',
      '\\t' : '\t',
      '\\v' : '\v'
    }
    TYPEKEYWORDS = [
      'int'
      'float'
      'void'
      'bool'
    ]
    MODIFIERS = [
      'const'
      'constexpr'
    ]
    PRIMITIVELITERALS = [
      'true'
      'false'
    ]
    KEYWORDS = [
      'while'
      'for'
      'return'
      'if'
      'elseif'
      'else'
      'continue'
      'break'
    ]
    TYPEDECLKEYWORDS = [
      'struct'
      'class'
    ]
    DELIMITERS = [
      ';'
      ','
      '.'
      '('
      ')'
      '['
      ']'
      '{'
      '}'
    ]
    OPERATORS = [
      '-'
      '+'
      '/'
      '*'
      '%'
    ]
    ASSIGNMENT = [
      '='
      '+='
      '-='
      '/='
      '*='

    ]
    COMPARISONS = [
      '=='
      '!='
      '<'
      '>'
      '<='
      '>='
    ]
    TWOCHARSYMBOLS = [
      '='
      '!'
      '<'
      '>'
      '-'
      '+'
      '/'
      '*'      
    ]

    currentCharIndex : int = -1
    characterBuffer : str = ''
    currentTokenIsString : bool = False
    currentChar : str = ''
    stringOpener : str = ''

    tokenArray : list[Compiler.Token] = []

    def createToken(type : Compiler.Token.Type, specificType : Compiler.Token.SpecificType = Compiler.Token.SpecificType.NONE, dontClearLast : bool = False):
      nonlocal characterBuffer

      if not dontClearLast and len(characterBuffer) != 0:
        createToken(Compiler.Token.Type.IDENTIFIER, Compiler.Token.SpecificType.UNSUREIDENTIFIER, dontClearLast=True)

      token = Compiler.Token(type, characterBuffer, line, character)
      tokenArray.append(token)
      characterBuffer = ''

    line = 1
    character = 0

    while currentCharIndex + 1 < len(string):
      currentCharIndex += 1
      character += 1
      currentChar = string[currentCharIndex]

      if currentChar == '\n':
          line += 1
          character = 0

      if currentTokenIsString:
        if currentChar == stringOpener:
          currentTokenIsString = False
          stringOpener = ''
          if len(characterBuffer) != 1:
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.STRINGLITERAL)
          else:
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.CHARLITERAL)
          continue
        else:
          if currentChar == '\\':
            coupledSymbol = currentChar + nextChar()
            if coupledSymbol in ESCAPESEQUENCES:
              currentCharIndex += 1
              characterBuffer += ESCAPESEQUENCES[coupledSymbol]

        
      else:
        if currentChar in (' ', '\n'):
          continue

        elif (currentChar == "'" or currentChar == '"'):
          currentTokenIsString = True
          stringOpener = currentChar
          continue
        elif currentChar in TWOCHARSYMBOLS:
          nextCharacter = nextChar()
          coupledSymbol = currentChar + nextCharacter
          if nextCharacter == '=':
            match coupledSymbol:
              case sym if sym in COMPARISONS:
                createToken(Compiler.Token.Type.COMPARISON)
              case sym if sym in ASSIGNMENT:
                createToken(Compiler.Token.Type.ASSIGMENT)
          else:
            match currentChar:
              case char if char in COMPARISONS:
                createToken(Compiler.Token.Type.COMPARISON)
              case char if char in ASSIGNMENT:
                createToken(Compiler.Token.Type.ASSIGMENT)
              case char if char in OPERATORS:
                createToken(Compiler.Token.Type.OPERATOR)
          continue
        
        match currentChar:
          case char if char in COMPARISONS:
            createToken(Compiler.Token.Type.COMPARISON)
            continue
          case char if char in ASSIGNMENT:
            createToken(Compiler.Token.Type.ASSIGMENT)
            continue
          case char if char in OPERATORS:
            createToken(Compiler.Token.Type.OPERATOR)
            continue

        if currentChar.isdigit() and len(characterBuffer) == 0:
          characterBuffer, isDecimal = eatNumber()
          if isDecimal:
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.DECIMALNUMBER)
          else:
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.NUMBER)
          continue
        elif currentChar == '/' and nextChar() == '/':
          endOfLine = string.find('\n',currentCharIndex)
          if endOfLine != -1:
            currentCharIndex = endOfLine - 1
            continue
          else:
            self._logEvent("NO NEWLINE AFTER SINGLE LINE COMMENT, ASSUMED END OF FILE", Compiler.Log.Severity.WARNING, 'String Tokeniser')
            break
        elif currentChar == '/' and nextChar() == '*':
          endOfMultilineComment = string.find('*/',currentCharIndex)
          if endOfMultilineComment != -1:
            currentCharIndex = endOfMultilineComment + 1
            continue
          else:
            self._logEvent("NO END TO MULILINE COMMENT, ASSUMED END OF FILE", Compiler.Log.Severity.WARNING, 'String Tokeniser')
            break

        characterBuffer += currentChar
        match characterBuffer:
          case buffer if buffer in TYPEKEYWORDS:
            createToken(Compiler.Token.Type.TYPEKEYWORD)
            continue
          case buffer if buffer in MODIFIERS:
            createToken(Compiler.Token.Type.MODIFIER)
            continue
          case buffer if buffer in PRIMITIVELITERALS:
            createToken(Compiler.Token.Type.PRIMITIVELITERAL)
            continue
          case buffer if buffer in KEYWORDS:
            createToken(Compiler.Token.Type.KEYWORD)
            continue
          case buffer if buffer in TYPEDECLKEYWORDS:
            createToken(Compiler.Token.Type.TYPEDECLKEYWORD)
            continue
          case buffer if buffer in DELIMITERS:
            if buffer == ';':
              createToken(Compiler.Token.Type.DELIMITER, Compiler.Token.SpecificType.SEMICOLON)
            elif buffer == '{':
              createToken(Compiler.Token.Type.DELIMITER, Compiler.Token.SpecificType.LCURLYBRACE)
            elif buffer == '}':
              createToken(Compiler.Token.Type.DELIMITER, Compiler.Token.SpecificType.RCURLYBRACE)
            else:
              createToken(Compiler.Token.Type.DELIMITER)
    
    return tokenArray


compiler = Compiler()
fileString = compiler._parseFileToString(Path('test.cpp').absolute())
tokenArray = compiler._tokeniseString(fileString)
for token in tokenArray:
  print(token)

while not compiler.logsEmpty():
  print(compiler.dequeueLog())



              