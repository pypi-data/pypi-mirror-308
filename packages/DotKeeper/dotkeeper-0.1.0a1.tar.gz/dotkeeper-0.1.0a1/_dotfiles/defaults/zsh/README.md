# Quick Reference

## Directories

- `.zfunc`: Directory for Zsh completion functions.

## Files/Directories

- `.zshrc`: Main configuration file for interactive Zsh sessions.
- `.zshenv`: Environment variables for all Zsh sessions (including non-interactive).
- `.zlogin`: Executed at the end of the initial progress for login shells.
- `.zlogout`: Executed when logging out of a Zsh login shell.
- `.zprofile`: Executed for login shells.

---

## Default Links

### Directories

- [`completion`](./completion/) -> `$HOME/.zfunc`

### Files

- [`zshrc.zsh`](./zshrc.zsh) -> `$HOME/.zshrc`
- [`zshenv.zsh`](./zshenv.zsh) ->`$HOME/.zshenv`
- [`zlogin.zsh`](./zlogin.zsh) -> `$HOME/.zlogin`
- [`zlogout.zsh`](./zlogout.zsh) -> `$HOME/.zlogout`
- [`zprofile.zsh`](./zprofile.zsh) -> `$HOME/.zprofile`

### YAML

```yaml
directories:
  completion: $HOME/.zfunc
files:
  zshrc.zsh: $HOME/.zshrc
  zshenv.zsh: $HOME/.zshenv
  zlogin.zsh: $HOME/.zlogin
  zlogout.zsh: $HOME/.zlogout
  zprofile.zsh: $HOME/.zprofile
```
