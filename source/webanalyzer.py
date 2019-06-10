import re
import os
import io

def webdelay(urlpart, minseconds, maxseconds):
    def inner(func):
        def result(url):
            if (urlpart in url):
                waitfor = random.randrange(minseconds, maxseconds)
                time.sleep(waitfor)
            return func(url)
        return result
    return inner

def filecache(basedir, encoding = 'utf-8'):
    def inner(func):
        def result(url):
           filename = url.replace(':', '_').replace('/', '_').replace('?', '_').replace('$', '_').replace('*', '_').replace('&', '_')
           fullFilename = basedir + filename
           cacheexist = False
           if (os.path.isfile(fullFilename)):
              cacheexist = True
           html = ""
           if (cacheexist):
              file = io.open(fullFilename, "r", encoding=encoding)
              html = file.read()
              file.close() 
           else:
              html = func(url)
              file = io.open(fullFilename, "w", encoding=encoding)
              file.write(html)
              file.close() 
           return html
        return result
    return inner



def html_analyze(pageContent, patternList):
   result = {}
   for pat in patternList:
      currentName = pat["name"]
      currentPattern = pat["pattern"]
      currentSaveMulti = pat["saveMulti"]
      currentValue = re.findall(currentPattern, pageContent)
      if (type(currentName) == type(['b'])):
          #defined multiplae names
          index = 0;
          for name in currentName:
              result[name] = currentValue[index]
              index = index + 1
      else:
          #defined single name
          if len(currentValue) > 0:
             if currentSaveMulti:
                currentValue = currentValue
             else:
                currentValue = currentValue[0]
          else:
             currentValue = ""
          result[currentName] = currentValue
   return result
