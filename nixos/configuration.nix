# Edit this configuration file to define what should be installed on
# your system. Help is available in the configuration.nix(5) man page, on
# https://search.nixos.org/options and in the NixOS manual (`nixos-help`).

# NixOS-WSL specific options are documented on the NixOS-WSL repository:
# https://github.com/nix-community/NixOS-WSL

{ config, lib, pkgs, ... }:

let
  # Opens links in the Windows default browser through WSL interop, so login
  # pages from Claude Code, gh and other CLIs open by themselves instead of
  # you copying a long URL out of the terminal.
  openInWindowsBrowser = pkgs.writeShellScript "open-in-windows-browser" ''
    /mnt/c/Windows/explorer.exe "$1"
    status=$?
    # explorer.exe exits with 1 even when the page opened; a higher code
    # means it couldn't start at all.
    if [ "$status" -le 1 ]; then exit 0; fi
    exit "$status"
  '';
in
{
  imports = [
    # include NixOS-WSL modules
    <nixos-wsl/modules>
  ];

  wsl.enable = true;
  wsl.defaultUser = "nixos";

  # This value determines the NixOS release from which the default
  # settings for stateful data, like file locations and database versions
  # on your system were taken. It's perfectly fine and recommended to leave
  # this value at the release version of the first install of this system.
  # Before changing this value read the documentation for this option
  # (e.g. man configuration.nix or on https://nixos.org/nixos/options.html).
  system.stateVersion = "26.05"; # Did you read the comment?

  environment.systemPackages = with pkgs; [
    git
    uv
    python3
    bun
    tailscale
    texlive.combined.scheme-medium
    wget
    nano
    atuin
    gpac
    exiftool
    xxd
    unzip
    tlrc
    tmux
    ripgrep # Claude Code uses this instead of its bundled copy (USE_BUILTIN_RIPGREP=0)
  ];

  # --- Claude Code -----------------------------------------------------------
  # Installed with Anthropic's native installer into ~/.local/bin, where it
  # updates itself (new models need recent versions). nix-ld lets that
  # prebuilt binary, and the one bundled in the VS Code extension, run on NixOS.
  programs.nix-ld.enable = true;
  environment.localBinInPath = true;

  programs.tmux = {
    enable = true;
    extraConfig = ''
      set -g mouse on
      set -g history-limit 50000
    '';
  };
  # Login and other links open in the Windows browser.
  environment.variables.BROWSER = "${openInWindowsBrowser}";

  # Plan B for the login, off until you create the file: when
  # ~/.config/claude-code/oauth-token exists, every new shell signs Claude Code
  # in with the one-year token that `claude setup-token` prints. Delete the
  # file to go back to the normal login. The token is read when a shell
  # starts, so it never lands in the world-readable Nix store; stray spaces or
  # Windows line endings in the file are stripped.
  environment.extraInit = ''
    if [ -r "$HOME/.config/claude-code/oauth-token" ]; then
      CLAUDE_CODE_OAUTH_TOKEN="$(tr -d '[:space:]' < "$HOME/.config/claude-code/oauth-token")"
      export CLAUDE_CODE_OAUTH_TOKEN
    fi
  '';

   environment.etc.certfile = {
     source = "/etc/ssl/certs/ca-bundle.crt";
     target = "ssl/cert.pem";
   };
  # Per-repo environments: each repo's .envrc (e.g. `use flake`) is loaded by
  # direnv, in your shell and, through hooks in ~/.claude/settings.json, in
  # Claude Code's Bash tool.
  programs.direnv.enable = true;
  programs.direnv.nix-direnv.enable = true;

  time.timeZone = "America/Mexico_City";
  virtualisation.docker.enable = true;
  users.users.nixos.extraGroups = [ "docker" ];
  nix.settings.experimental-features = [ "nix-command" "flakes" ];
}
