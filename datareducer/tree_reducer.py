from typing import Dict, List, Any, Callable

def modifyChild(parent: Dict, key: str) -> Dict:
  child = parent.get(key, None)
  if child != None:
    child['cnt']+=1
  else:
    child = {'cnt': 1}
    parent[key] = child

  return child

def recursionOnChildren(parent: Dict, keys: List[Any]) -> None:
  if len(keys) > 0:
    k = keys.pop()
    child = modifyChild(parent, k)
    if len(keys) > 0:
      recursionOnChildren(child, keys)
    else:
      return

def traverse(data: List[Any], func: Callable[[Any], Any]) -> Dict:
  tree = {}
  for i in data:
    recursionOnChildren(tree, func(i))

  return  tree

class exports: 
  traverse = traverse
