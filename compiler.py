from __future__ import annotations
from enum import Enum
import copy
from typing import Optional, Tuple, Any
from pathlib import Path


buildFolderPath = 'Build/'
sourceFilePath = 'D:/Python projects/casio basic compiler/test.cpp'

#workingDirectory = input("Absolute working directory: ")
workingDirectory = 'D:/Python projects/casio basic compiler'
class Compiler:
  NATIVEHEADERS = [
    'CASIOBASICCOMPILERHEADERS.h'
  ]
  NATIVEIDENTIFIERS = [
    'locate'
  ]
  SCOPEOWNINGKEYWORDS = [
    'if',
    'else',
    'elseif',
    'while',
    'for'
  ]
  PREPROCCESSORDIRECTIVETOKENS = [
    '#include'
  ]
  TYPEDDECLARATIONKEYWORDTOKENS = [
    #'class' #no support for class yet
    'struct'
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
    'bool',
    'list',
    'matrix'
  ]
  MODIFIERTOKENS = [
    'const',
    'constexpr'
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
    '++',
    '/*',
    '*/'
  ]
  COMMENTTOKENS = [
    '/*',
    '*/'
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
  
  class UniqueIdHandler:
    def __init__(self):
      self.allocatedIds = []
      self.freedIds = []
      self.nextNewId = 0
    
    def getId(self):
      id = -1
      if len(self.freedIds) != 0:
        id = self.freedIds[0]
        self.freedIds.pop(0)
        self.allocatedIds.append(id)
      else:
        id = self.nextNewId
        self.nextNewId += 1
      return id


    def freeId(self, id : int):
      if id in self.allocatedIds:
        self.allocatedIds.remove(id)
        self.freedIds.append(id)
  
  # class ASTNodes:
  #   class VariableDeclaration:
  #     def __init__(self, type : str, value,)

  class Scope:
    def __init__(self, startLine = -1, parentScope : Optional[Compiler.Scope] = None):
      self.tokens = []
      self.parentScope = parentScope
      self.tokensOwningChildrenScopes = {} # token : indexInSelf.Tokens
      self.startLine = startLine
      self.localIdentifiers = [] #(id, identifier)
      self.referencedExternalIdentifiers = [] #(id, identifier)

    def addToken(self, token : Compiler.Token):
      if token.type == Compiler.Token.Type.DELIMITER and token.content == '{':
        self.tokensOwningChildrenScopes[token] = len(self.tokens)
      self.tokens.append(token)

    def printTokens(self):
      scopesToPrint = []
      for token in self.tokens:
        print(token)
        if token in self.tokensOwningChildrenScopes:
          scopesToPrint.append(token.ownedScope)

      for scope in scopesToPrint:
        scope.printTokens()

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
      STRUCTIDENTIFIER = 11
      TYPEDECLARATIONKEYWORD = 12
      DIRECTIVE = 13
      MODIFIER = 14



    def __init__(self, content : str, type : Type, lineNumber : int, columnNumber : int, fileName : str):
      self.content = content
      self.type = type
      self.lineNumber = lineNumber
      self.columnNumber = columnNumber
      self.fileName = fileName
      self.identifierUId = -1
      self.parentScope : Optional[Compiler.Scope] = None
      self.ownedScope: Optional[Compiler.Scope] = None

    def __str__(self):
      return f'TYPE: {self.type.name}\nLINE: {self.lineNumber}\nCOLUMN: {self.columnNumber}\nFILE: {self.fileName}\nCONTENT: "{self.content}"\n'

  def __init__(self):
    print("compiler init")
    self.sourceDirectories : dict[Path,Tuple[str,...]]= {} #directory : [file extensions]
    self.workingDirectory = Path()
    self.filesToCompile : list[Path] = []
    self.typeDeclaredTypes : list[str] = []

  def setWorkingDirectory(self, workingDirectory : str):
    self.workingDirectory = Path(workingDirectory)
  #
  def addSourceDirectory(self, directory : str, fileExtensions : tuple = ('.cpp',)):
    directoryPath = Path(directory)

    if not directoryPath.exists():
      raise FileNotFoundError(f"Source directory does not exist: {directoryPath}")
    
    if not directoryPath.is_absolute():
      directoryPath = directoryPath.resolve()
    
    self.sourceDirectories[directoryPath] = fileExtensions

  def compile(self):
    self.filesToCompile = self._getUniqueTargetFilesAsPath()

    tokens = []

    for filePath in self.filesToCompile:
      print(filePath)
      tokens.extend(self._tokeniseFile(filePath))

    scope, unclosedScope = self._buildScopes(tokens)
    if unclosedScope:
      print(f"UNCLOSED SCOPE - CAUSE MAY BEGIN ON LINE: {unclosedScope.startLine}")

    scope.print()

    undeclaredIdentifiers = self._assessIdentifiers(scope)
    if len(undeclaredIdentifiers) > 0:
      print(f'PASS ONE: {len(undeclaredIdentifiers)} UNDECLARED VARIABLE{(len(undeclaredIdentifiers)!=1)*'S'}:')
      for token in undeclaredIdentifiers:
        print(token)

    undeclaredIdentifiers = self._assessIdentifiers(scope)
    if len(undeclaredIdentifiers) > 0:
      print(f'PASS TWO: {len(undeclaredIdentifiers)} UNDECLARED VARIABLE{(len(undeclaredIdentifiers)!=1)*'S'}:')
      for token in undeclaredIdentifiers:
        print(token)

    scope.printTokens()




    #print all tokens
    # for token in secondTaggedTokenArray:
    #   print(token)

  @staticmethod
  def _isNumber(number : str) -> bool:
      try:
        float(number)
        return True
      except:
        return False
  
  def _getUniqueTargetFilesAsPath(self) -> list:
    filePaths = []
    seenFiles = set()

    for sourcePath, fileExtensions in self.sourceDirectories.items():
      for fileExtension in fileExtensions:
        for filePath in sourcePath.rglob('*'+fileExtension):
          if filePath not in seenFiles:
            filePaths.append(filePath)
            seenFiles.add(filePath)

    return filePaths
  
  

  def _dothing(self, tokenArray : list[Compiler.Token]):
    class VariableTypes(Enum):
      INT = 1
      FLOAT = 2
      STRING = 3
      CLASS = 4
      STRUCT = 5

    class SyntaxPatternBase:
      pass

    class VariableDeclaration(SyntaxPatternBase):
      def __init__(self, type : VariableTypes, identifier : str, definingExpression : Optional[Any] = None):
        self.type = type
        self.identifier = identifier
        self.definingExpression = definingExpression
      
    class BinaryExpression(SyntaxPatternBase):
      def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

      
    class SYNTAXPATTERNTYPES(Enum):
      VARIABLEDECLARATION = 1
      BINARYEXPRESSION = 2


    #def doesSyntaxPatternRequire()

    def getVariableType(token : Compiler.Token) -> Optional[VariableTypes]:
      match token.content:
        case 'int':
          return VariableTypes.INT
        case 'float':
          return VariableTypes.FLOAT
        case 'string':
          return VariableTypes.STRING
        case 'class':
          return VariableTypes.CLASS
        case 'struct':
          return VariableTypes.STRUCT
      return None
    
    class expressionBuilder:
      def __init__(self):
        pass
      def build(self, tokenArray : list[Compiler.Token], startingIndex : int):
        topExpression : Optional[SyntaxPatternBase] = None
        currentExpression : Optional[SyntaxPatternBase] = None
        left : Optional[Any] = None
        right : Optional[Any] = None
        operator : Optional[str] = None
        index = startingIndex
        token = tokenArray[index]
        delimiterDepth = 1
        while delimiterDepth > 0:
          if token.type == Compiler.Token.Type.DELIMITER:
            match token.content:
              case ';':
                delimiterDepth = 0
              case '(':
                delimiterDepth += 1
              case ')':
                delimiterDepth -= 1
              case _:
                print("UNEXPECTED DELIMITER WITH NO KNOWN RESOLVE.")
                raise NotImplementedError
          elif token.type == Compiler.Token.Type.NUMBER:
            print('')
        
        if left and right and operator:
          

              

          index += 1
          token = tokenArray[index]

    SYNTAXPATTERNS : dict[tuple, SYNTAXPATTERNTYPES] = { #pattern : type
      (self.Token.Type.TYPEKEYWORD,self.Token.Type.IDENTIFIER) : SYNTAXPATTERNTYPES.VARIABLEDECLARATION,
      (self.Token.Type.NUMBER,self.Token.Type.OPERATOR,self.Token.Type.NUMBER) : SYNTAXPATTERNTYPES.BINARYEXPRESSION,

    }
    tokenBuffer : list[Compiler.Token] = []
    tokenTypeBuffer : list[Compiler.Token.Type] = []
    lastSyntaxPattern : Optional[SYNTAXPATTERNTYPES] = None

    syntaxPatternArray : list[SyntaxPatternBase] = []
  
    for token in tokenArray:
      tokenBuffer.append(token)
      tokenTypeBuffer.append(token.type)

      tupledTypeBuffer = tuple(tokenTypeBuffer)
      if tupledTypeBuffer in SYNTAXPATTERNS:
        currentSyntaxPattern = SYNTAXPATTERNS[tupledTypeBuffer]

        if lastSyntaxPattern:
          print("broh")
        else:
          match currentSyntaxPattern:
            case SYNTAXPATTERNTYPES.VARIABLEDECLARATION:
              varType = getVariableType(tokenBuffer[0])
              if varType:
                syntaxPatternArray.append(VariableDeclaration(varType,tokenBuffer[1].content))
                lastSyntaxPattern = currentSyntaxPattern
              else:
                raise NotImplementedError
                #TODO THROW ERROR
              tokenBuffer.clear()
              tokenTypeBuffer.clear()

              
        





      #then compare buffer with patterns to identify


  def _tokeniseFile(self, filePath : Path) -> list:
    firstPassTokenArray = self._ParseFileToRawTokens(filePath)
    taggedTokenArray = self._tagTokens(firstPassTokenArray)
    secondTaggedTokenArray = self._tagTokens(taggedTokenArray)
    unsolvedTokens = []
    for token in secondTaggedTokenArray:
      if token.type == self.Token.Type.UNSOLVED:
        unsolvedTokens.append(token)

    print(f'\nUnsolved tokens: {len(unsolvedTokens)}')
    for token in unsolvedTokens:
      print(token)

    secondTaggedTokenArray = self._considerDirectives(secondTaggedTokenArray)
    
    return secondTaggedTokenArray

  def _buildScopes(self, tokenArray : list[Compiler.Token]) -> tuple:
    globalScope = self.Scope()
    scopeStack = [globalScope]
    
    for token in tokenArray:

      if token.type == self.Token.Type.DELIMITER:
        if token.content == '{':
          scopeStack[-1].addToken(token)
          token.parentScope = scopeStack[-1]
          scopeStack.append(self.Scope(token.lineNumber,scopeStack[-1]))
          token.ownedScope = scopeStack[-1]
          continue
        elif token.content == '}':
          scopeStack.pop()

      scopeStack[-1].addToken(token)
      token.parentScope = scopeStack[-1]

      
    
    if len(scopeStack) > 1:
      print("SCOPE NOT CLOSED")
      return (globalScope,scopeStack[-1])
    
    return (globalScope,None)

  def _considerDirectives(self, tokenArray : list):
    finalTokenArray : list[Compiler.Token] = []
    pathsToTokenise : list[Path] = []
    tokensLeftToSkip = 0
    for tokenIndex, token in enumerate(tokenArray):
      if tokensLeftToSkip > 0: #allow for skipping, in cases such as include, skipping the following string token
        tokensLeftToSkip -= 1
        continue

      if token.type == self.Token.Type.DIRECTIVE:
        if token.content == '#include' and tokenIndex + 1 < len(tokenArray):
          headerPath = Path(tokenArray[tokenIndex+1].content)
          tokensLeftToSkip = 1

          if headerPath.name in self.NATIVEHEADERS: #if native header, dont tokenising it
            print(f"NATIVE HEADER SKIPPED: {headerPath.name}")
            continue
          if not headerPath.is_absolute():
            for sourceDirectory in self.sourceDirectories:
              if(sourceDirectory/headerPath).exists():
                headerPath = sourceDirectory/headerPath
                break

          if not headerPath in self.filesToCompile:
            self.filesToCompile.append(headerPath) # for loop doesnt loop through elements added while looping so i need to manually tokenise this.
          continue
      
      finalTokenArray.append(token)
    
    for headerPath in pathsToTokenise:
      finalTokenArray.extend(self._tokeniseFile(headerPath))

    return finalTokenArray

#TODO add arguments from a function to the next scope (the function def scope)
  def _assessIdentifiers(self, scope : Compiler.Scope) -> list[Compiler.Token]:
    ancestorScopes = []
    previousToken : Optional[Compiler.Token] = None
    idHandler = Compiler.UniqueIdHandler()
    undeclaredIdentifiers : list[Compiler.Token] = [] #array of tokens

    def isIdentifierInAncestorScopes(token : Compiler.Token):
      for scope in ancestorScopes:
        identifierInLocalScope, identifierUId = isIdentifierInLocalScope(token, scope)
        if identifierInLocalScope:
          return True,identifierUId
      return False,-1
    
    def isIdentifierInLocalScope(token : Compiler.Token, scope : Compiler.Scope):
      for pair in scope.localIdentifiers:
          if token.content == pair[1]: #identifiers content
            return True, pair[0] #identifiers Uid
      
      return False, -1

    def identifyIdentifier(token : Compiler.Token):
      if token.type == self.Token.Type.IDENTIFIER or token.type == self.Token.Type.STRUCTIDENTIFIER:
        if previousToken:
          if previousToken.type == self.Token.Type.TYPEKEYWORD or previousToken.type == self.Token.Type.TYPEDECLARATIONKEYWORD: #maybe have diff handing for typedec and primitive type keywords in future
            scope.localIdentifiers.insert(0,(idHandler.getId(), token.content))
            return
          
        identifierInLocalScope, identifierUIdLocal = isIdentifierInLocalScope(token, scope)
        identifierInAncestorScope, identifierUIdAncestor = isIdentifierInAncestorScopes(token)
        
        if identifierInLocalScope:
          token.identifierUId = identifierUIdLocal
        elif identifierInAncestorScope:
          token.identifierUId = identifierUIdAncestor
          
        if not(identifierInLocalScope or isIdentifierInAncestorScopes(token)):
          undeclaredIdentifiers.append(token)
   
    def identifyScope(scope : Compiler.Scope):
      nonlocal previousToken
      for token in scope.tokens:
        identifyIdentifier(token)
        previousToken = token
        if token.ownedScope != None:
          ancestorScopes.append(scope)
          identifyScope(token.ownedScope)
      if scope in ancestorScopes:
        ancestorScopes.pop()

    identifyScope(scope)

    return undeclaredIdentifiers
        
      

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

        #elif token.content in self.typeDeclaredTypes: #DONT KNOW IF THIS TAG IS APPROPRIATE - this rule aplies for structs that have already been declared
        #  token.type = self.Token.Type.STRUCTIDENTIFIER

        elif token.content in self.ASSIGNMENTTOKENS:
          token.type = self.Token.Type.ASSIGNMENT
        
        elif token.content in self.COMPARISONTOKENS:
          token.type = self.Token.Type.COMPARISON
        
        elif token.content in self.OPERATORTOKENS:
          token.type = self.Token.Type.OPERATOR

        elif token.content in self.PREPROCCESSORDIRECTIVETOKENS:
          token.type = self.Token.Type.DIRECTIVE

        elif token.content in self.MODIFIERTOKENS:
          token.type = self.Token.Type.MODIFIER

        elif token.content in self.TYPEDDECLARATIONKEYWORDTOKENS:
          token.type = self.Token.Type.TYPEDECLARATIONKEYWORD

        elif localTokenArray[tokenIndex-1].content == 'struct':
          token.type = self.Token.Type.STRUCTIDENTIFIER
          #if 

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
            
      taggedArray.append(self.Token(token.content, token.type, token.lineNumber, token.columnNumber, token.fileName))

    finalArray = []
    for tokenIndex, token in enumerate(localTokenArray):
      if tokenIndex in tokenIndexesToSkip:
        continue

      finalArray.append(token)

    return finalArray

  def _ParseFileToRawTokens(self, filePath : Path) -> list:
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
    commenting = False
    lastCharacter = ''

    currentLineNumber = -1
    currentColumnNumber = -1


    def appendToken(tokenType = self.Token.Type.UNSOLVED):
      nonlocal currentTokenFragment
      if currentTokenFragment != '':
        tokenArray.append(self.Token(currentTokenFragment, tokenType, currentLineNumber, currentColumnNumber-len(currentTokenFragment), filePath.name))
        currentTokenFragment = ''

    def checkCharacter(character, nextCharacter):
      nonlocal currentTokenFragment
      nonlocal currentTokenIsString
      nonlocal lastCharacterWasDouble
      nonlocal lastCharacterWasBackslash
      nonlocal backslashBuffer
      nonlocal lastCharacterWasSpace
      nonlocal stringOpeningCharacter
      nonlocal lastCharacter
      nonlocal commenting
      
      localLastCharWasSpace = lastCharacterWasSpace

      if commenting:
        if lastCharacter + character == '*/':
          commenting = False

        lastCharacter = character
        return

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

        if character in self.DOUBLEDLONETOKENS: # DOUBLE TOKEN DETECTION
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
              elif currentTokenFragment in self.COMMENTTOKENS:
                commenting = True 
                currentTokenFragment = ''
                return

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
          appendToken()
          currentTokenIsString = True
          stringOpeningCharacter = character
          #currentTokenFragment += character #dont add the apostrophes to the string?
        return
      
      if localLastCharWasSpace:
        appendToken()
      currentTokenFragment += character

      




    for lineNumber, line in enumerate(sourceFileLines):
      currentLineNumber = lineNumber+1 # so it can be refrenced by appendToken()
      for charIndex, character in enumerate(line):
        charIndexP1 = charIndex+1 #same as above comment!
        currentColumnNumber = charIndexP1
        if charIndexP1 < len(line) and character == '/' and line[charIndexP1] == '/' and not currentTokenIsString:
          currentTokenFragment = ''
          print(f'comment on line: {currentLineNumber}')
          break  # Skip rest of line
        
        if charIndexP1 < len(line):
          checkCharacter(character, line[charIndexP1])
        else:
          checkCharacter(character, '')
    
    appendToken()

    return tokenArray









compiler = Compiler()
compiler.setWorkingDirectory(workingDirectory)
compiler.addSourceDirectory(workingDirectory)
for dir in compiler.sourceDirectories:
  print(dir)
compiler.compile()
