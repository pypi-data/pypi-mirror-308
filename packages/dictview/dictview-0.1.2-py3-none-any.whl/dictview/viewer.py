"""
Helps to view long nested dictionaries
"""

def view(d, length=3, return_obj=False):

    lines = []

    def view_recursive(d, lvl=0, length=length):

        assert length >= 2, "Length must be >= 2"

        tick = "\u251c" + "\u2500"*(length-1)
        elbo = "\u2514" + "\u2500"*(length-1)
        pipe = "\u2502" + " "*(length-1)
        
        for i, (k, v) in enumerate(d.items()):

            if lvl == 0:
                line = ""
            elif lvl == 1:
                line = tick

            else:
                if i + 1 == len(d.items()):
                    line = f"{pipe*(lvl-1)}{elbo}"
                else:
                    line = f"{pipe*(lvl-1)}{tick}"
            
            if isinstance(v, dict) and lvl == 0:
                lines.append(f"{line}{k}")
                view_recursive(v, lvl+1, length)
            elif isinstance(v, dict) and lvl > 0:
                lines.append(f"{line}{k}")
                view_recursive(v, lvl+1, length)
            else:
                lines.append(f"{line}{k} <{type(v).__name__}>")

    view_recursive(d, length=length)

    if return_obj:
        return lines
    else:
        print('\n'.join(lines))
        return None
