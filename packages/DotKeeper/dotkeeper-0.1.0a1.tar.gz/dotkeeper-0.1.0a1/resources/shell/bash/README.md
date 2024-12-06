# Quick Reference

## Directories

- `.bash_completion.d`: Directory for Bash completion scripts.

## Files

- `.bashrc`: Main configuration file for interactive Bash sessions.
- `.bash_login`: Alternative to `.bash_profile`, used if `.bash_profile` doesn't exist.
- `.bash_logout`: Executed when logging out of a Bash login shell.
- `.bash_profile`: Executed for Bash login shells.
- `.bash_completion`: File for Bash completion scripts.

---

## Default Links

### Directories

- [`completion`](./completion/) -> `$HOME/.bash_completion.d`

### Files

- [`bashrc.bash`](./bashrc.bash) -> `$HOME/.bashrc`
- [`bash_login.bash`](./bash_login.bash) -> `$HOME/.bash_login`
- [`bash_logout.bash`](./bash_logout.bash) -> `$HOME/.bash_logout`
- [`bash_profile.bash`](./bash_profile.bash) ->`$HOME/.bash_profile`
- [`bash_completion.bash`](./bash_completion.bash) -> `$HOME/.bash_completion`

### YAML

```yaml
directories:
  completion: $HOME/.bash_completion.d
files:
  bashrc.bash: $HOME/.bashrc
  bash_login.bash: $HOME/.bash_login
  bash_logout.bash: $HOME/.bash_logout
  bash_profile.bash: $HOME/.bash_profile
  bash_completion.bash: $HOME/.bash_completion
```
