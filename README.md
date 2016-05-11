# slicetag
Parsing any text file with tags {:, :}, meaning {:CONDITIONS|CONTENT:} to generate derived texts.

## Why?
Often, we want to be able to not to have to create different files in order to share parts of files with other people.

## How?

This will combine the [Text Parsing for Sharing](https://gist.github.com/Mindey/02eff1fcec0098a1fb72) ideas with [VimWiki Share](https://github.com/Mindey/mindey.github.io/blob/master/scripts/VimwikiShare.py) script refactored.

I think, since the CONDITIONS inside {:CONDITIONS|CONTENT:} could be quite general, we could have even modules for **slicetag**. E.g., a module that implements the entities like shown [here](https://github.com/Mindey/mindey.github.io#mindeys-wiki), could be a separate module. Later, I will try to solve the generation of parse tree from nesting of the {: :} tags, but currently, will just leave the implementation that takes only the slices based on the first level bracket matching, leaving the more complex cases for the future to implement.
