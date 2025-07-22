from __future__ import annotations
from enum import Enum, auto
from typing import Any, Union, Optional
from pathlib import Path


class Compiler:

  class AST:

    class PrimitiveTypes(Enum):
      INT = auto()
      FLOAT = auto()
      CHAR = auto()
      VOID = auto()
      BOOL = auto()

    class Operators(Enum):
      ADD = auto()
      SUBTRACT = auto()
      MULTIPLY = auto()
      DIVIDE = auto()
      MODULO = auto()

    class Assigners(Enum):
      EQUALS = auto()
      ADDEQ = auto()
      SUBEQ = auto()
      MULEQ = auto()
      DIVEQ = auto()


    class ASTNode:
      pass
    
    class Literal(ASTNode): #TODO CLASS DELC AUSSPORT
      def __init__(self, value : Any, type : Union[Compiler.AST.PrimitiveTypes, Compiler.AST.StructDeclaration]):
        self.value : Any = value
        self.type : Union[Compiler.AST.PrimitiveTypes, Compiler.AST.StructDeclaration] = type

    class Expression(ASTNode):
      def __init__(self, left : Compiler.AST.ASTNode, operator : Compiler.AST.Operators, right : Compiler.AST.ASTNode):
        self.left : Compiler.AST.ASTNode = left
        self.right : Compiler.AST.ASTNode = right
        self.operator : Compiler.AST.Operators = operator

    class Scope(ASTNode):
      def __init__(self, contents : list[Compiler.AST.ASTNode]):
        self.contents : list[Compiler.AST.ASTNode] = contents

    class FunctionArgument(ASTNode):
      def __init__(self, identifier : str, defaultValue : Compiler.AST.ASTNode):
        self.identifier : str = identifier
        self.defaultValue : Compiler.AST.ASTNode = defaultValue

    class FunctionDeclaration(ASTNode):
      def __init__(self, identifier : str, arguments : Union[Compiler.AST.FunctionArgument, list[Compiler.AST.FunctionArgument]]):
        self.identifier : str = identifier
        self.arguments : Union[Compiler.AST.FunctionArgument, list[Compiler.AST.FunctionArgument]] = arguments

    class StructDeclaration(ASTNode):
      def __init__(self, identifier : str):
        raise NotImplementedError
      
    class VariableDeclaration(ASTNode):
      def __init__(self, identifier : str, value : Compiler.AST.ASTNode):
        self.identifier : str = identifier
        self.value : Compiler.AST.ASTNode = value
        
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
      DIRECTIVE = auto()

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

    SEVERITYCOLORS = {
      'FATAL' : "\033[38;5;196m",
      'CRITICAL' : "\033[38;5;201m",
      'ERROR' : "\033[38;5;202m",
      'WARNING' : "\033[38;5;220m",
      'DEBUG' : "\033[38;5;87m",
      'NOTICE' : "\033[38;5;82m"
    }

    def __init__(self, message : str, severity : Severity, author : str = 'none'):
      self.message : str = message
      self.author : str = author
      self.severity : Compiler.Log.Severity = severity

    def __str__(self):
      match self.severity:
        case Compiler.Log.Severity.FATAL:
          return f"""   {self.SEVERITYCOLORS[self.severity.name]}[{self.severity.name}]{"\033[0m"} [{self.author}] {self.message}"""
        case Compiler.Log.Severity.CRITICAL:
          return f"""{self.SEVERITYCOLORS[self.severity.name]}[{self.severity.name}]{"\033[0m"} [{self.author}] {self.message}"""
        case Compiler.Log.Severity.ERROR:
          return f"""   {self.SEVERITYCOLORS[self.severity.name]}[{self.severity.name}]{"\033[0m"} [{self.author}] {self.message}"""
        case Compiler.Log.Severity.WARNING:
          return f""" {self.SEVERITYCOLORS[self.severity.name]}[{self.severity.name}]{"\033[0m"} [{self.author}] {self.message}"""
        case Compiler.Log.Severity.DEBUG:
          return f"""   {self.SEVERITYCOLORS[self.severity.name]}[{self.severity.name}]{"\033[0m"} [{self.author}] {self.message}"""
        case Compiler.Log.Severity.NOTICE:
          return f"""  {self.SEVERITYCOLORS[self.severity.name]}[{self.severity.name}]{"\033[0m"} [{self.author}] {self.message}"""
      return "LOG HAS NO SEVERITY"

  def __init__(self) -> None:
    self.logs : list[Compiler.Log] = []
    self.debugLogs : bool = True

    self._logEvent("LOG TEST", Compiler.Log.Severity.FATAL, "COMPILER")
    self._logEvent("LOG TEST", Compiler.Log.Severity.CRITICAL, "COMPILER")
    self._logEvent("LOG TEST", Compiler.Log.Severity.ERROR, "COMPILER")
    self._logEvent("LOG TEST", Compiler.Log.Severity.WARNING, "COMPILER")
    self._logEvent("LOG TEST", Compiler.Log.Severity.DEBUG, "COMPILER")
    self._logEvent("LOG TEST", Compiler.Log.Severity.NOTICE, "COMPILER")
    while not self.logsEmpty():
      print(self.dequeueLog())
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
    if severity == Compiler.Log.Severity.DEBUG and not self.debugLogs:
      return
    self.logs.append(Compiler.Log(message,severity,author))
  
  def _considerDirectives(self, tokenArray : list[Compiler.Token],directiveTokenIndexes : list[int])->list[Compiler.Token]:
    tokenArrayToInsertByIndex : dict[int, list[Compiler.Token]] = {}
    numberOfRemovedTokens = 0
    for tokenIndex in directiveTokenIndexes:
      tokenIndex -= numberOfRemovedTokens
      token = tokenArray[tokenIndex]

      if token.content == '#include':
        targetFilePath = Path(tokenArray[tokenIndex+1].content).absolute()
        if targetFilePath.exists():
          includeTokenArray, includeDirectiveTokenIndexes = self._tokeniseString(self._parseFileToString(targetFilePath))
          tokenArrayToInsertByIndex[tokenIndex] = self._considerDirectives(includeTokenArray, includeDirectiveTokenIndexes)

        else:
          self._logEvent(f"File not found for #include at line: {token.line} column: {token.char}", Compiler.Log.Severity.ERROR, '_considerDirectives')

        tokenArray.pop(tokenIndex+1)
        tokenArray.pop(tokenIndex)
        numberOfRemovedTokens += 2

    lastInsertionIndex = 0
    originalTokenArrayWithIncludedArrays = []

    for item in tokenArrayToInsertByIndex.items():
      indexToInsert = item[0]
      arrayToInsert = item[1]
      

      includeAppendedIndexArray = tokenArray[lastInsertionIndex:indexToInsert]
      includeAppendedIndexArray.extend(arrayToInsert)

      originalTokenArrayWithIncludedArrays.extend(includeAppendedIndexArray)

      lastInsertionIndex = indexToInsert

    originalTokenArrayWithIncludedArrays.extend(tokenArray[lastInsertionIndex:len(tokenArray)])

    return originalTokenArrayWithIncludedArrays
  

  def _buildAST(self, tokenArray : list[Compiler.Token]):
    print('Nah!')

  def _parseFileToString(self, filePath : Path) -> str:
    with open(filePath,'r') as file:
      return file.read()
    
  def _tokeniseString(self, string : str)->tuple[list[Compiler.Token], list[int]]:
    def nextChar() -> str:
      nonlocal string
      nonlocal currentCharIndex

      if len(string) > currentCharIndex + 1:
        return string[currentCharIndex+1]
      return ''
    
    def lastChar() -> str: #brooo this doesnt even get used
      nonlocal string
      nonlocal currentCharIndex

      if currentCharIndex > 0:
        return string[currentCharIndex-1]
      return ''

    def eatNumber() -> tuple[str, int]:
      nonlocal currentCharIndex
      nonlocal character
      nonlocal characterBufferLength
      characterBufferLength -= 2
      number = ''
      currentCharacter = string[currentCharIndex]
      isDecimal = False
      isNegative = False
      while currentCharacter.isdigit() or currentCharacter == '.' or currentCharacter == '-':
        if currentCharacter == '.':
          if isDecimal:
            self._logEvent(f"PROBABLY UNEXPECTED '.' IN NUMBER @ LINE {line} CHAR {character}", Compiler.Log.Severity.WARNING, 'Number Builder')
          isDecimal = True
        elif currentCharacter == '-':
          if isNegative:
            self._logEvent(f"PROBABLY UNEXPECTED '-' IN NUMBER @ LINE {line} CHAR {character}", Compiler.Log.Severity.WARNING, 'Number Builder')
          isNegative = True
        number += currentCharacter
        currentCharIndex += 1
        character += 1
        characterBufferLength += 1
        currentCharacter = string[currentCharIndex]
      currentCharIndex -= 1
      character -= 1
      
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
    DIRECTIVES = [
      '#include',
      '#define,'
    ]
    TYPEKEYWORDS = [
      'int',
      'float',
      'void',
      'bool',
    ]
    MODIFIERS = [
      'const',
      'constexpr',
    ]
    PRIMITIVELITERALS = [
      'true',
      'false',
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
      'struct',
      'class',
    ]
    DELIMITERS = [
      ';',
      ',',
      '.',
      '(',
      ')',
      '[',
      ']',
      '{',
      '}',
    ]
    OPERATORS = [
      '-',
      '+',
      '/',
      '*',
      '%',
    ]
    ASSIGNMENT = [
      '=',
      '+=',
      '-=',
      '/=',
      '*=',

    ]
    COMPARISONS = [
      '==',
      '!=',
      '<',
      '>',
      '<=',
      '>=',
    ]
    TWOCHARSYMBOLS = [
      '=',
      '!',
      '<',
      '>',
      '-',
      '+',
      '/',
      '*',      
    ]

    currentCharIndex : int = -1
    characterBuffer : str = ''
    characterBufferLength : int = 0
    currentTokenIsString : bool = False
    currentChar : str = ''
    stringOpener : str = ''

    directiveTokenIndexArray : list[int] = []
    tokenArray : list[Compiler.Token] = []

    def createToken(type : Compiler.Token.Type, specificType : Compiler.Token.SpecificType = Compiler.Token.SpecificType.NONE, dontClearLast : bool = False, contentIsBuffer : bool = False):
      nonlocal characterBuffer
      nonlocal characterBufferLength

      if not contentIsBuffer and not dontClearLast and len(characterBuffer) != 0:
        createToken(Compiler.Token.Type.IDENTIFIER, Compiler.Token.SpecificType.UNSUREIDENTIFIER, dontClearLast=True, contentIsBuffer=True)

      token = None

      if contentIsBuffer: #  and len(characterBuffer) != 0
        token = Compiler.Token(type, characterBuffer, line, character-characterBufferLength)

      else:
        token = Compiler.Token(type, currentChar, line, character-characterBufferLength)

      if token.content != '':
        tokenArray.append(token)

      characterBuffer = ''
      characterBufferLength = 0
      

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
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.STRINGLITERAL, contentIsBuffer=True)
          else:
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.CHARLITERAL, contentIsBuffer=True)
          continue
        else:
          if currentChar == '\\':
            coupledSymbol = currentChar + nextChar()
            if coupledSymbol in ESCAPESEQUENCES:
              currentCharIndex += 1
              characterBuffer += ESCAPESEQUENCES[coupledSymbol]
              characterBufferLength += 1
              continue
        characterBuffer += currentChar
        characterBufferLength += 1
        continue

        
      else:
        if currentChar in (' ', '\n'):
          if currentChar == ' ':
            characterBufferLength += 1
          continue

        if currentChar == '/' and nextChar() == '/':
          endOfLine = string.find('\n',currentCharIndex)
          
          if endOfLine != -1:
            currentCharIndex = endOfLine - 1
            #line += 1
            character = 0
            continue
          else:
            self._logEvent("NO NEWLINE AFTER SINGLE LINE COMMENT, ASSUMED END OF FILE", Compiler.Log.Severity.WARNING, '_tokeniseString')
            break
        elif currentChar == '/' and nextChar() == '*':
          endOfMultilineComment = string.find('*/',currentCharIndex)
          if endOfMultilineComment != -1:
            newLineCount = string[currentCharIndex:endOfMultilineComment].count('\n')
            line += newLineCount
            if newLineCount > 0:
              lastNewline = string.rfind('\n', currentCharIndex, endOfMultilineComment) #if diff line
              character = endOfMultilineComment - lastNewline + 1
            else:
              character = endOfMultilineComment + 1 #if sameline still
            currentCharIndex = endOfMultilineComment + 1
            continue
          else:
            self._logEvent("NO END TO MULILINE COMMENT, ASSUMED END OF FILE", Compiler.Log.Severity.WARNING, '_tokeniseString')
            break

        elif (currentChar.isdigit() or (currentChar == '-' and nextChar().isdigit())) and len(characterBuffer) == 0:
          number, isDecimal = eatNumber()
          characterBuffer = number

          if isDecimal:
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.DECIMALNUMBER, dontClearLast=True, contentIsBuffer=True)
          else:
            createToken(Compiler.Token.Type.LITERAL, Compiler.Token.SpecificType.NUMBER, dontClearLast=True, contentIsBuffer=True)
          continue

        elif (currentChar == "'" or currentChar == '"'):
          currentTokenIsString = True
          stringOpener = currentChar
          createToken(Compiler.Token.Type.IDENTIFIER, Compiler.Token.SpecificType.UNSUREIDENTIFIER, dontClearLast=True, contentIsBuffer=True)
          continue
        elif currentChar in TWOCHARSYMBOLS:
          nextCharacter = nextChar()
          coupledSymbol = currentChar + nextCharacter
          if nextCharacter == '=':
            match coupledSymbol:
              case coupledSymbol if coupledSymbol in COMPARISONS:
                currentChar = coupledSymbol
                createToken(Compiler.Token.Type.COMPARISON)
              case coupledSymbol if coupledSymbol in ASSIGNMENT:
                currentChar = coupledSymbol
                createToken(Compiler.Token.Type.ASSIGMENT)
          else:
            match currentChar:
              case currentChar if currentChar in COMPARISONS:
                createToken(Compiler.Token.Type.COMPARISON)
              case currentChar if currentChar in ASSIGNMENT:
                createToken(Compiler.Token.Type.ASSIGMENT)
              case currentChar if currentChar in OPERATORS:
                createToken(Compiler.Token.Type.OPERATOR)
          continue

        match currentChar:
          case currentChar if currentChar in COMPARISONS:
            createToken(Compiler.Token.Type.COMPARISON)
            continue
          case currentChar if currentChar in ASSIGNMENT:
            createToken(Compiler.Token.Type.ASSIGMENT)
            continue
          case currentChar if currentChar in OPERATORS:
            createToken(Compiler.Token.Type.OPERATOR)
            continue
          case currentChar if currentChar in DELIMITERS:
            if currentChar == ';':
              createToken(Compiler.Token.Type.DELIMITER, Compiler.Token.SpecificType.SEMICOLON)
            elif currentChar == '{':
              createToken(Compiler.Token.Type.DELIMITER, Compiler.Token.SpecificType.LCURLYBRACE)
            elif currentChar == '}':
              createToken(Compiler.Token.Type.DELIMITER, Compiler.Token.SpecificType.RCURLYBRACE)
            else:
              createToken(Compiler.Token.Type.DELIMITER)
            continue


        match characterBuffer:
          case characterBuffer if characterBuffer in TYPEKEYWORDS:
            createToken(Compiler.Token.Type.TYPEKEYWORD, dontClearLast=True, contentIsBuffer=True)
          case characterBuffer if characterBuffer in MODIFIERS:
            createToken(Compiler.Token.Type.MODIFIER, dontClearLast=True, contentIsBuffer=True)
          case characterBuffer if characterBuffer in PRIMITIVELITERALS:
            createToken(Compiler.Token.Type.PRIMITIVELITERAL, dontClearLast=True, contentIsBuffer=True)
          case characterBuffer if characterBuffer in KEYWORDS:
            createToken(Compiler.Token.Type.KEYWORD, dontClearLast=True, contentIsBuffer=True)
          case characterBuffer if characterBuffer in TYPEDECLKEYWORDS:
            createToken(Compiler.Token.Type.TYPEDECLKEYWORD, dontClearLast=True, contentIsBuffer=True)
      characterBuffer += currentChar
      characterBufferLength += 1

      if characterBuffer in DIRECTIVES:
        self._logEvent(f'directive token at line {line}, char {character}', Compiler.Log.Severity.DEBUG, '_tokeniseString')
        directiveTokenIndexArray.append(len(tokenArray))
        createToken(Compiler.Token.Type.DIRECTIVE, dontClearLast=True, contentIsBuffer=True)
        
    
    return tokenArray, directiveTokenIndexArray


compiler = Compiler()
fileString = compiler._parseFileToString(Path('test2.cpp').absolute())
tokenArray, directiveIndexes = compiler._tokeniseString(fileString)
finalTokenArray = compiler._considerDirectives(tokenArray, directiveIndexes)
for token in finalTokenArray:
  print(token)

while not compiler.logsEmpty():
  print(compiler.dequeueLog())



              