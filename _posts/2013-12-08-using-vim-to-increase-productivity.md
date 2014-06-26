Using Vim to increase productivity

This may seem redundant, knowing there are [many blog posts] on the subject,
but I just couldn't help myself. So I guess I'll keep it short and simple, and
enumerate the different reasons why Vim *kills*.

__IMO__ of course, unless if you're a Java user (in which case you're probably
used to using "C-space" to write your code), I believe you'll find more in Vim
what you can find in any other IDE.

Here are some IDE-like features:

### Speed

Obviously. I haven't ever been as fast as I am with Vim. Every action is
lightning-fast and non-repetitive. And if you think you're slow, you're missing
some of the good stuff.

Whenever I think *"hey, this is kinda annoying"*, I fire up a quick google
search and memorize what I should be doing to go faster.

After a while, it gets to a point where you spend more time figuring out what
to do next rather than actually typing it. Which is how it needs to be.

### Completion (insert mode)

* C-n: next matching word
* C-p: previous matching word
* C-x: enter advanced completion mode
    - omni completion: C-o
    - file names: C-f
    - whole lines: C-l
    - tags: C-]
    - vim command-line: C-v

And that's just the beginning! Checkout ":h ins-completion" for the complete
list.

### Folding

In normal mode:

* za: toggle fold, use zA to toggle recursively
* zM: close all folds
* zR: reveal all folds

Again, lookup ":h fold-commands" for the complete list. ;)

### Mappings

Not much to say on this, except that you can map keystrokes to commands, which
you can define using VimL. And since Vim has modes, you can map different
keystrokes for different modes, or all of them if you want to. Once again,
you're free to customize Vim at your desire.

Just type __:map key-combination command__.

Use "nmap" for normal mode, "imap" for insert and "vmap" for visual.

### Quickfix

This feature will especially get C/C++ users' attention. Did you know Vim has a
":make" command? Yes it does the same thing as the shell "make" command, and it
also loads errors/warnings in a special Vim buffer, called the __quickfix__.

Once this buffer is loaded, you can open/close it with ":copen" and ":cclose",
it will list all these errors, and you can hit enter to go to the error's
source. Or you can use ":cn" and ":cp" to move to the next and previous error.

### Plugins

Probably the greatest feature in Vim. I really should write a post only on
plugins, here's a few *necessary* plugins:

- [pathogen](https://github.com/tpope/vim-pathogen), a plugin-manager plugin
- [surround](https://github.com/tpope/vim-surround), the name says it all
- [fugitive](https://github.com/tpope/vim-fugitive), a git wrapper
- [nerdtree](https://github.com/scrooloose/nerdtree), a file tree explorer
- [nerdcommenter](https://github.com/scrooloose/nerdtree), orgasmic commenting
- [supertab](https://github.com/ervandew/supertab), if you don't feel like
  memorizing all the completion shortcuts

[many blog posts]: http://net.tutsplus.com/articles/web-roundups/25-vim-tutorials-screencasts-and-resources/
