"""
Finds path through a dict to a desired key.
"""

from    collections import deque
from    dataclasses import dataclass

def is_ordered_subset(subset: list, superset: list) -> bool:
    """
    Checks whether a sequence (list)"""
    for i in range(len(superset) - len(subset) + 1):
        if superset[i:i+len(subset)] == subset:
            return True
    return False


@dataclass
class DictPath:
    """
    Storage object for value and path through a dict.

    Attributes:
        value (any): The value stored at the end of the target sequence in the dict
        path (list): The path through the dict to arrive at the value. 
    """
    value: any
    path: list


def seek(d: dict, tgt: list, strategy="dfs") -> DictPath:
    """
    Searches dict for sequence of keys matching target

    Args:
        d (dict): Dictionary object for traversal
        tgt (list): Target sequence of dictionary keys

    Returns:
        DictPath: An object with the value corresponding to the end of the target 
            key sequence and the path through the dict that gets to that value. 
            If multiple candidate paths are possible, these values are returnes as
            None and the user is prompted to make the target sequence more specific.
            If no paths are found, the values are returned as None. 

    Examples:
        >>> d = {
        >>>     "A": {"a": 1,},
        >>>     "B": {"b": {"be": 1, "bee": 2, "beee": {"hello": 3},}, 'bb': "woah",},
        >>>     "C": 1,
        >>>     "D": {"beee": "hi"}
        >>> }
        >>> seek(d, tgt=["a"])
        DictPath(value=1, path=["A", "a"])
        >>> seek(d, tgt=["b", "beee"])
        DictPath(value={"hello": 3}, path=["B", "b", "beee"])
        >>> seek(d, tgt=["beee"])
        DictPath(value=None, path=None)
        >>> seek(d, tgt["dslkfjgdlk"])
        DictPath(value=None, path=None)
    """

    candidates = []

    def seek_dfs(d, tgt, idx=0, current_path=None) -> None:
        """
        Searches dict with DFS strategy
        """
        
        # Base case: current path is not given
        if current_path is None:
            current_path = []

        # Base case: sequence has been fully matched
        if idx == len(tgt):
            return current_path
        
        for k, v in d.items():
            new_path = current_path + [k]
            candidate = DictPath(value=v, path=new_path)
            # If key matches current part of sequence, look deeper 
            if k == tgt[idx]:
                # If it is the last key in the sequence, it's a match
                if idx == len(tgt) - 1 and candidate not in candidates:
                    candidates.append(candidate)
                # Otherwise continue deeper into the sequence
                if isinstance(v, dict):
                    result = seek_dfs(v, tgt, idx=idx + 1, current_path=new_path)
                    if result is not None and candidate not in candidates:
                        candidates.append(candidate)
            # If not, look deeper into the dict, but not the sequence
            if isinstance(v, dict):
                result = seek_dfs(v, tgt, idx=idx, current_path=new_path)
                if result is not None and candidate not in candidates:
                    candidates.append(candidate)

    def seek_bfs(d, tgt) -> None:
        """
        Searches dict with BFS strategy
        """

        queue = deque([DictPath(value=d, path=[])])

        while len(queue) > 0:
            current = queue.popleft()
            if isinstance(current.value, dict):
                for k, v in current.value.items():
                    new_path = current.path + [k]
                    new_item = DictPath(value=v, path=new_path)
                    queue.append(new_item)
                    if is_ordered_subset(tgt, new_path) and tgt[-1] == new_path[-1]:
                        candidates.append(new_item)

    executables = {
        "dfs": seek_dfs,
        "bfs": seek_bfs
    }
    executables.get(strategy, "Not a valid strategy")(d, tgt)

    try:
        assert len(candidates) == 1, f"Expected 1 path, got {len(candidates)}."
        return candidates[0]
    except AssertionError as e:
        if len(candidates) > 1:
            print("Try a more specific (longer) target. These were the paths found:")
            for candidate in candidates:
                print(candidate)
        elif len(candidates) == 1:
            print("Target not found.")
        else:
            print(e)
        return DictPath(value=None, path=None)

    